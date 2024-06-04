import os
import subprocess
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)


def json_to_dict(filename) -> dict:
    """
    Open a JSON file and return its contents as a dictionary.
    """
    try:
        reponame, ext = os.path.splitext(filename)
        if ext != ".json":
            logging.error(f"Invalid file extension: {ext} must be a .json extension.")
            return {}
        else:
            with open(filename, "r") as f:
                return {reponame: json.load(f)}
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except json.decoder.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON: {e}")
    except Exception as e:
        logging.error(f"Unknown error: {e}")
    return {}

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
        reponame = list(repo.keys())[0]
        os.chdir(reponame)
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
    except Exception as e:
        logging.error(f"Unknown error: {e}")


def main() -> None:
    """
    Main function to create the repository.
    """
    reponame = input("Enter the name of the repository json schema: ")
    logging.info(f"Creating repository {reponame}...")
    create_repo(json_to_dict(reponame))

if __name__ == '__main__':
    main()
