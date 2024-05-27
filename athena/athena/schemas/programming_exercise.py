from pydantic import Field, AnyUrl
from zipfile import ZipFile
from git.repo import Repo

from athena.helpers.programming.code_repository import get_repository_zip, get_repository
from .exercise_type import ExerciseType
from .exercise import Exercise


class ProgrammingExercise(Exercise):
    """A programming exercise that can be solved by students, enhanced with metadata."""

    type: ExerciseType = Field(ExerciseType.programming, const=True)

    programming_language: str = Field(description="The programming language that is used for this exercise.", example="java")
    solution_repository_uri: AnyUrl = Field(description="URL to the solution git repository, which contains the "
                                                        "reference solution.",
                                            example="http://localhost:3000/api/example-solutions/1")
    template_repository_uri: AnyUrl = Field(description="URL to the template git repository, which is the starting "
                                                        "point for students.",
                                            example="http://localhost:3000/api/example-template/1")
    tests_repository_uri: AnyUrl = Field(description="URL to the tests git repository, which contains the tests that "
                                                     "are used to automatically grade the exercise.",
                                         example="http://localhost:3000/api/example-tests/1")


    def get_solution_zip(self) -> ZipFile:
        """Return the solution repository as a ZipFile object."""
        return get_repository_zip(self.solution_repository_uri)


    def get_solution_repository(self) -> Repo:
        """Return the solution repository as a Repo object."""
        return get_repository(self.solution_repository_uri)


    def get_template_zip(self) -> ZipFile:
        """Return the template repository as a ZipFile object."""
        return get_repository_zip(self.template_repository_uri)


    def get_template_repository(self) -> Repo:
        """Return the template repository as a Repo object."""
        return get_repository(self.template_repository_uri)


    def get_tests_zip(self) -> ZipFile:
        """Return the tests repository as a ZipFile object."""
        return get_repository_zip(self.tests_repository_uri)


    def get_tests_repository(self) -> Repo:
        """Return the tests repository as a Repo object."""
        return get_repository(self.tests_repository_uri)