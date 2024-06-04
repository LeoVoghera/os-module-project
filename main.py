import os
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def create_dir_tree(dir: dict[str, any], cwd: str = ".") -> None:
    """
    Create directory tree based on the provided dictionary structure.
    """
    for name, value in dir.items():
        if not isinstance(name, str):
            logging.error(f"Invalid directory name: {name}. Skipping...")
            continue

        path = os.path.join(cwd, name)
        if isinstance(value, dict):
            try:
                os.makedirs(path, exist_ok=True)
                logging.info(f"[Creating dir] {path}")
                create_dir_tree(value, cwd = path)
            except OSError as e:
                logging.error(f"Failed to create directory {path}: {e}")
        elif value == "file":
            try:
                logging.info(f"[Creating file] {path}")
                with open(path, "w") as f:
                    pass
            except OSError as e:
                logging.error(f"Failed to create file {path}: {e}")

def create_repo(repo: dict[str: any]) -> None:
    """
    Create a new repository based on the provided dictionary structure.
    """
    try:
        create_dir_tree(repo)
        repo_name = list(repo.keys())[0]
        os.chdir(repo_name)
        subprocess.run(["git", "init"])
        subprocess.run(["git", "status"])
        commit = input("Make initial commit? ([y]/n): ").lower()
        if commit != "n":
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "Initial commit."])
    except OSError as e:
        logging.error(e)
    except FileNotFoundError:
        logging.error("Git is not installed or not in the system's PATH.")

EXAMPLE_REPO = {
    "MY_ADVANCED_PROJECT": {
        "src": {
            "main.py": "file",
            "utils": {
                "__init__.py": "file",
                "math_utils.py": "file",
                "string_utils.py": "file",
                "data_processing.py": "file"
            },
            "models": {
                "__init__.py": "file",
                "neural_network.py": "file",
                "decision_tree.py": "file",
                "svm.py": "file"
            }
        },
        "test": {
            "test_main.py": "file",
            "test_utils": {
                "__init__.py": "file",
                "test_math_utils.py": "file",
                "test_string_utils.py": "file",
                "test_data_processing.py": "file"
            },
            "test_models": {
                "__init__.py": "file",
                "test_neural_network.py": "file",
                "test_decision_tree.py": "file",
                "test_svm.py": "file"
            }
        },
        "docs": {
            "README.md": "file",
            "CONTRIBUTING.md": "file",
            "CODE_OF_CONDUCT.md": "file"
        },
        "scripts": {
            "data_preparation.py": "file",
            "train_model.py": "file",
            "evaluate_model.py": "file"
        },
        ".gitignore": "file",
        "requirements.txt": "file",
        "setup.py": "file"
    }
}

def main() -> None:
    """
    Main function to create the repository.
    """
    create_repo(EXAMPLE_REPO)

if __name__ == '__main__':
    main()
