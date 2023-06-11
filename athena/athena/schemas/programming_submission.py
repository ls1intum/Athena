from typing import Optional
from pydantic import Field
from zipfile import ZipFile
from git.repo import Repo

from athena.helpers.programming.code_repository import get_repository_zip, get_repository
from athena.schemas.submission import Submission


class ProgrammingSubmission(Submission):
    """Submission on a programming exercise."""
    repository_url: str = Field(example="https://lms.example.com/assignments/1/submissions/1/download")


    def get_zip(self) -> ZipFile:
        """Return the submission repository as a ZipFile object."""
        return get_repository_zip(self.repository_url)


    def get_repository(self) -> Repo:
        """Return the submission repository as a Repo object."""
        return get_repository(self.repository_url)
    
    def get_code(self, file_path: str):
        """
        Fetches the code from the submission repository.
        Might be quite an expensive operation! If you need to fetch multiple files, consider using get_zip() instead.
        """
        repo_zip = self.get_zip()
        with repo_zip.open(file_path, "r") as f:
            return f.read().decode("utf-8")
