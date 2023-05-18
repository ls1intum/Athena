#!/usr/bin/env python3
"""
Helper script to start all docker-compose files
for the assessment module manager and all assessment modules.
"""

import subprocess
import argparse
import logging
from pathlib import Path
from typing import Tuple, List


class DockerComposeManager:
    """
    Class to manage docker compose files for modules.
    """

    MODULE_PATTERN = 'module_'

    def __init__(self, production, env_files_dir):
        self.production = production
        self.env_files_dir = Path(env_files_dir)
        self.logger = self._setup_logger()
        self.modules = []
        self.valid_modules = []

    @staticmethod
    def _setup_logger():
        """
        Setup logger for this script.
        """
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def get_module_folders(self):
        """
        Get all module folders in the current directory.
        """
        self.modules = [
            dir_path
            for dir_path in Path('.').iterdir()
            if dir_path.is_dir() and dir_path.name.startswith(self.MODULE_PATTERN)
        ]

    def filter_valid_modules(self):
        """
        Filter out all modules that are not valid.
        """
        for module in self.modules:
            if (module / "docker-compose.yml").exists():
                self.valid_modules.append(module)
            else:
                self.logger.warning(f"Skipping module '{module}' because it is not a valid module folder")

    def build_docker_compose(self, compose_files: Tuple[Path, ...]):
        """
        Build all the docker-compose files.
        """
        self.logger.info("Building docker-compose files...")
        self.logger.info(f"Building docker-compose.yml for '{compose_files}'...")
        command = ["docker-compose"]
        for compose_file in compose_files:
            command += ["-f", str(compose_file)]
        command += ["build"]
        subprocess.run(command, check=True)

    def start_docker_compose_files(self, compose_files: List[Tuple[Path, ...]], env_files: List[Path]):
        """
        Start all the docker-compose files.
        """
        processes = []
        for compose_file_pack, env_file in zip(compose_files, env_files):
            command = ["docker-compose"]
            for compose_file in compose_file_pack:
                command += ["-f", str(compose_file)]
            command += ["--env-file", str(env_file), "up"]
            self.logger.info("Starting docker-compose files... %s", command)
            processes.append(subprocess.Popen(command))

        # Wait for all processes to complete
        for process in processes:
            process.wait()

    def main(self):
        """
        Main entry point of the script.
        """
        self.get_module_folders()
        self.filter_valid_modules()

        # gather compose files
        if self.production:
            override_filename = "docker-compose.prod.yml"
        else:
            override_filename = "docker-compose.override.yml"
        compose_files: List[Tuple[Path, ...]] = []  # list of compose files which should be run together
        # assessment module manager
        assessment_module_manager_compose_files: Tuple[Path, Path] = (Path("docker-compose.yml"), Path(override_filename))
        if not self.production:
            self.build_docker_compose(assessment_module_manager_compose_files)
        compose_files.append(assessment_module_manager_compose_files)
        # modules
        for module in self.valid_modules:
            module_compose_files: Tuple[Path, Path] = (module / "docker-compose.yml", module / override_filename)
            if not self.production:
                self.build_docker_compose(module_compose_files)
            compose_files.append(module_compose_files)

        # gather env files
        env_files = [self.env_files_dir / "assessment_module_manager" / ".env"]
        env_files += [self.env_files_dir / module / ".env" for module in self.valid_modules]

        self.start_docker_compose_files(compose_files, env_files)


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--production', action='store_true', help='Specify if the environment is production')
    parser.add_argument('--env_files_dir', default='.', help='Specify the directory of environment files')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    manager = DockerComposeManager(args.production, args.env_files_dir)
    manager.main()
