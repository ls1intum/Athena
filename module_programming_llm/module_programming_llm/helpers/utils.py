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
    line_number_max_length = len(str(len(lines)))
    return "\n".join(
        f"{str(line_number).rjust(line_number_max_length)} {line}" 
        for line_number, line 
        in enumerate(lines, start=1)
    )


def get_file_extension(programming_language: str) -> str | None:
    # JAVA, C, OCAML, HASKELL, PYTHON, SWIFT, VHDL, ASSEMBLER, EMPTY, KOTLIN
    file_extensions = {
        "JAVA": ".java",
        "C": ".c",
        "OCAML": ".ml",
        "HASKELL": ".hs",
        "PYTHON": ".py",
        "SWIFT": ".swift",
        "VHDL": ".vhd",
        "ASSEMBLER": ".asm",
        "KOTLIN": ".kt",
    }
    return file_extensions.get(programming_language.upper())


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
        repo.delete_remote(remote)
    yield remote

def get_diff(src_repo: Repo, 
             dst_repo: Repo, 
             src_prefix: str = "a",
             dst_prefix: str = "b",
             file_path: Optional[str] = None,
             name_only: bool = False,
             branch: str = "main", 
             remote_name: str = "diff_target") -> str:
    """Get the diff between two branches of two Git repositories.

    Args:
        src_repo (Repo): Repository to diff from
        dst_repo (Repo): Repository to diff to
        src_prefix (str, optional): Prefix for the source files. Defaults to "a".
        dst_prefix (str, optional): Prefix for the destination files. Defaults to "b".
        file_path (Optional[str], optional): Path to the file(s), supports glob patterns. Defaults to None.
        name_only (bool, optional): Only show names of changed files. Defaults to False.
        branch (str, optional): Branch to diff. Defaults to "main".
        remote_name (str, optional): Name of the remote to use. Defaults to "diff_target".

    Returns:
        str: The diff between the two branches
    """    
    if file_path is not None and "*" not in file_path:
        file_path_obj = Path(src_repo.working_tree_dir) / file_path
        if not file_path_obj.exists():
            return f"- {src_prefix}/{file_path} does not exist.\n+ {dst_prefix}/{file_path} has been added."

    with temporary_remote(remote_name, src_repo, dst_repo.working_tree_dir):
        diff = src_repo.git.diff(branch, f"{remote_name}/{branch}", f"--src-prefix={src_prefix}/", f"--dst-prefix={dst_prefix}/", file_path, name_only=name_only)
    return diff