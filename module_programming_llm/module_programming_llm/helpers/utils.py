from pathlib import Path
from os import PathLike
from contextlib import contextmanager
from collections.abc import Iterator
from typing import List, Dict, Optional, Callable, Union, Tuple

from git import Repo, Remote
from langchain.document_loaders import GitLoader

def load_files_from_repo(repo: Repo, file_filter: Optional[Callable[[str], bool]] = None) -> Dict[str, Optional[str]]:
    return {
        doc.metadata['file_path']: doc.page_content
        for doc in GitLoader(repo_path=repo.working_tree_dir, file_filter=file_filter).load()
    }

def merge_repos_by_filepath(*repos: List[Repo], file_filter: Optional[Callable[[str], bool]] = None) -> Iterator[Tuple[str, List[Optional[str]]]]:
    docs = [load_files_from_repo(repo, file_filter) for repo in repos]
    files = {file for doc in docs for file in doc}

    for file in files:
        yield (file, [doc.get(file) for doc in docs])

def add_line_numbers(content: str) -> str:
    lines = content.splitlines()
    padding = len(str(len(lines)))
    return "\n".join([f"{i+1:>{padding}} {line}" for i, line in enumerate(lines)])

@contextmanager
def temporary_remote(remote_name: str, repo: Repo, remote_url: PathLike) -> Iterator[Optional[Remote]]:
    """Context manager for temporarily adding a remote to a Git repository.
    
    Args:
        remote_name (str): The name of the remote
        repo (Repo): The repository to add the remote to
        remote_url (PathLike): The URL of the remote
    """
    remote = None
    try:
        remote = repo.remote(remote_name)
    except ValueError:
        remote = repo.create_remote(remote_name, remote_url)
        remote.fetch()
        yield remote
        repo.delete_remote(remote)
    else:
        yield remote

def get_diff(src_repo: Repo, 
             dst_repo: Repo, 
             src_prefix: str = "a",
             dst_prefix: str = "b",
             file_path: Optional[Union[Path, str]] = None,
             branch: str = "main", 
             remote_name: str = "diff_target") -> str:
    """Get the diff between two branches of two Git repositories.
    
    Args:
        src_repo (Repo): The repository to get the diff from
        dst_repo (Repo): The repository to get the diff to
        src_prefix (str, optional): The prefix to use for the source files. Defaults to "a"
        dst_prefix (str, optional): The prefix to use for the destination files. Defaults to "b"
        file_path (Optional[Union[Path, str]]): The path to the file to get the diff for. Defaults to None
        branch (str, optional): The branch to get the diff for. Defaults to "main"
        remote_name (str, optional): The name of the remote to use. Defaults to "diff_target"
    """
    file_path_obj = Path(src_repo.working_tree_dir) / file_path
    if not file_path_obj.exists():
        return f"- {src_prefix}/{file_path} does not exist.\n+ {dst_prefix}/{file_path} has been added."

    with temporary_remote(remote_name, src_repo, dst_repo.working_tree_dir):
        diff = src_repo.git.diff(branch, f"{remote_name}/{branch}", f"--src-prefix={src_prefix}/", f"--dst-prefix={dst_prefix}/", file_path)
    return diff