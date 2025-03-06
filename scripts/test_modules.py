import subprocess
import os
import sys
import shutil


def main():
    poetry_path = shutil.which("poetry")
    if poetry_path is None:
        print("Could not find poetry.")
        sys.exit(1)
    os.environ["POETRY_PATH"] = poetry_path

    test_modules = ["tests/integration_tests"]

    success = True
    original_env = os.environ["PATH"]

    for module in test_modules:
        path_to_module_environment = os.path.join(os.getcwd(), module, ".venv")
        os.environ["VIRTUAL_ENV"] = path_to_module_environment
        os.environ["PATH"] = os.path.join(path_to_module_environment, "bin") + os.pathsep + original_env
        subprocess.run([sys.executable, "-m", "venv", path_to_module_environment])

        result = subprocess.run(["poetry", "run", "pytest"])
        if result.returncode != 0:
            success = False

    sys.exit(0 if success else -1)


if __name__ == "__main__":
    main()
