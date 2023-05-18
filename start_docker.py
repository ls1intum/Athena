#!/usr/bin/env python3
"""
Helper script to start all docker-compose files
for the assessment module manager and all assessment modules.
"""

import argparse
import os
import subprocess
import glob

def get_docker_compose_files(production_mode, modules):
    # Get the docker files for the main and the modules
    compose_files = []

    # add assessment module manager + module docker-compose files
    for folder in ["assessment_module_manager"] + modules:
        module_files = [f'./{folder}/docker-compose.yml']
        if not production_mode:
            module_files.append(f'./{folder}/docker-compose.override.yml')
        else:
            module_files.append(f'./{folder}/docker-compose.prod.yml')
        compose_files.append(module_files)

    # Return compose files
    return compose_files

def build_and_start_docker_compose_files(compose_files, env_file_path, production_mode):
    # Start docker-compose for each set of files
    for files in compose_files:
        # Change to directory of the compose files
        directory = os.path.dirname(files[0])

        # Set env-file path
        env_file = os.path.join(env_file_path, directory, '.env')

        # Build docker-compose command
        cmd = ['docker-compose'] + ['-f ' + file for file in files]

        # Run the build command in non-production mode
        if not production_mode:
            build_cmd = cmd + ['build']
            subprocess.run(' '.join(build_cmd), shell=True)

        # Run the up command
        up_cmd = cmd + ['--env-file', env_file, 'up']

        subprocess.run(' '.join(up_cmd), shell=True)

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--production', action='store_true', help='Run in production mode')
    parser.add_argument('--env_file_path', default='.', help='Path to .env file dir')
    parser.add_argument('--modules', nargs='*', default=glob.glob('module_*'), help='Modules to run')

    # Parse arguments
    args = parser.parse_args()

    # Get docker compose files
    compose_files = get_docker_compose_files(args.production, args.modules)

    # Build and start docker compose files
    build_and_start_docker_compose_files(compose_files, args.env_file_path, args.production)

if __name__ == '__main__':
    main()
