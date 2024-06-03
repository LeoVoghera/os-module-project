import os
import time
import logging
import shutil
import subprocess
import tqdm

logging.basicConfig(level=logging.INFO)

def make_files(file_num: int, file_name: str, msg: str, ext: str = "txt") -> None:
    """
    Function to create a specified number of files with a given name, message, and extension.

    Parameters:
    file_num (int): The number of files to create.
    file_name (str): The base name for the files.
    msg (str): The message to write in each file.
    ext (str): The file extension. Defaults to 'txt'.
    """
    start = time.time()
    for i in range(file_num):
        try:
            with open(f"{file_name}_{i}.{ext}", 'w') as f:
                f.write(msg)
            logging.info(f"Successfully created {file_name}_{i}.{ext} at ({os.getcwd()})")
        except Exception as e:
            logging.error(f"Failed to create {file_name}_{i}.{ext} due to {str(e)}")
    end = time.time()
    elapsed = end - start
    avg_create_time = elapsed/file_num
    logging.info(f"\nFiles created in average time: {avg_create_time}.\n")

def make_dirs(dir_num: int, dir_name: str) -> None:
    """
    Function to create a specified number of directories with a given name.

    Parameters:
    dir_num (int): The number of directories to create.
    dir_name (str): The base name for the directories.
    """
    start = time.time()
    for i in range(dir_num):
        try:
            os.makedirs(f"{dir_name}_{i}", exist_ok=True)
            logging.info(f"Successfully created {dir_name}_{i} at ({os.getcwd()})")
        except Exception as e:
            logging.error(f"Failed to create {dir_name}_{i} due to {str(e)}")
    end = time.time()
    elapsed = end - start
    avg_create_time = elapsed/dir_num
    logging.info(f"\nDirectories created in average time: {avg_create_time}.\n")

def make_nested_dirs(dir_num: int, dir_name: str, depth: int) -> None:
    """
    Function to create a specified number of nested directories with a given name.

    Parameters:
    dir_num (int): The number of directories to create.
    dir_name (str): The base name for the directories.
    depth (int): The depth of the nested directories.
    """
    start = time.time()
    for i in range(dir_num):
        nested_dir_name = os.path.join(*[f"{dir_name}_{i}" for _ in range(depth)])
        try:
            os.makedirs(nested_dir_name, exist_ok=True)
            logging.info(f"Successfully created {nested_dir_name} at ({os.getcwd()})")
        except Exception as e:
            logging.error(f"Failed to create {nested_dir_name} due to {str(e)}")
    end = time.time()
    elapsed = end - start
    avg_create_time = elapsed/dir_num
    logging.info(f"\nDirectories created in average time: {avg_create_time}.\n")


def make_repo(repo_name: str, file_num: int,dir_num: int, file_name: str = "file", msg: str = "", dir_name: str = "dir", ext: str = "txt") -> None:
    """
    Function to create a repository with a specified number of directories and files.

    Parameters:
    repo_name (str): The name of the repository.
    file_num (int): The number of files to create in each directory.
    dir_num (int): The number of directories to create.
    file_name (str): The base name for the files. Defaults to 'file'.
    msg (str): The message to write in each file. Defaults to ''.
    dir_name (str): The base name for the directories. Defaults to 'dir'.
    ext (str): The file extension. Defaults to 'txt'.
    """
    start = time.time()
    if os.path.isdir(repo_name):
        approval = input(f"a directory by the name {file_name} already exists in the working directory would you like to replace it? (y/[n]): ")
        if approval.lower() == "y":
            shutil.rmtree(repo_name)
        else:
            print("Exiting system.")
            return
    os.makedirs(repo_name)
    os.chdir(repo_name)
    subprocess.run("git init")
    logging.info(f"Making dirs in {os.getcwd()}...")
    make_dirs(dir_num, dir_name)
    logging.info("Finished making dirs.\n")
    logging.info("Making files...")
    for dir in os.listdir():
        if os.path.isdir(dir):
            os.chdir(dir)
            logging.info(f"Making files in {os.getcwd()}...")
            make_files(file_num, file_name, msg, ext)
            logging.info(f"Dir: {os.getcwd()} has files.\n")
            os.chdir("..")
    logging.info("\n\n")
    os.chdir("..")
    end = time.time()
    elapsed = end - start
    logging.info(f"Repository created in {elapsed} seconds")


def main():
    """
    Main function to create a repository with a specified structure.
    """
    msg = "print('Hello World!')"
    ext = "py"
    file_num = 10
    dir_num = 4
    repo_name = "my_repo"
    make_repo(repo_name, file_num, dir_num, msg=msg, ext=ext)
    for path, dir, file in os.walk(repo_name):
        print((path, dir, file))

if __name__ == "__main__":
    main()

