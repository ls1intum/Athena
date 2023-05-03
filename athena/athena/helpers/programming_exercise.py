import os
import zipfile
from tempfile import NamedTemporaryFile, TemporaryDirectory
import contextlib
from typing import List
from collections.abc import Iterator

import httpx
import git

@contextlib.contextmanager
def get_repository_zip(url: str) -> Iterator[zipfile.ZipFile]:
    """
    Download a zip file of a code repository from the given URL and yield a
    ZipFile object for further processing. Clean up the temporary file after use.
    """
    with httpx.stream("GET", url) as response:
        response.raise_for_status()
        with NamedTemporaryFile() as temp_file:
            for chunk in response.iter_bytes():
                temp_file.write(chunk)
            temp_file.seek(0)
            yield zipfile.ZipFile(temp_file)

@contextlib.contextmanager
def get_repository_zips(urls: List[str]) -> Iterator[List[zipfile.ZipFile]]:
    """
    Download zip files of code repositories from the given URLs and yield a
    list of ZipFile objects for further processing. Clean up the temporary
    files after use.
    """
    with contextlib.ExitStack() as stack:
        yield [stack.enter_context(get_repository_zip(url)) for url in urls]

@contextlib.contextmanager
def extract_zip_to_temp_dir(zip_file: zipfile.ZipFile) -> Iterator[str]:
    """
    Extract the contents of a zip file to a temporary directory and return
    the path to the temporary directory.
    """
    with TemporaryDirectory() as temp_dir:
        zip_file.extractall(temp_dir)
        yield temp_dir

@contextlib.contextmanager
def get_repository(url: str) -> Iterator[git.Repo]:
    """
    Download a zip file of a code repository from the given URL, extract it to
    a temporary directory, and yield a git.Repo object for further processing.
    """
    with get_repository_zip(url) as zip_file:
        with extract_zip_to_temp_dir(zip_file) as temp_dir:
            if not os.path.exists(os.path.join(temp_dir, ".git")):
                git.Repo.init(temp_dir)
            yield git.Repo(temp_dir)

@contextlib.contextmanager
def get_repositories(urls: List[str]) -> Iterator[List[git.Repo]]:
    """
    Download zip files of code repositories from the given URLs, extract them
    to temporary directories, and yield a list of git.Repo objects for further
    processing.
    """
    with contextlib.ExitStack() as stack:
        yield [stack.enter_context(get_repository(url)) for url in urls]
