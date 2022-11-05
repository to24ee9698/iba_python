import os
import re
import tarfile


def file_walker(directory):
    """" Walk a directory and yield all files in the directory.

    Args:
        directory: - Path of files to be walked through.

    Returns:
        A generator object that will yield each file in the directory when iterated over in a loop or next
    """
    for dirName, subdirList, file_list in os.walk(directory):
        file_list.sort()
        for file_name in file_list:
            yield os.path.join(dirName, file_name)


def find_tar_gz_files(directory):
    """ Walks through a directory and finds all tarballs  *.tar.gz.

    Args:
        directory: - Path of files to be searched for tarballs.

    Returns:
        A generator object that will yield each tarball in a given directory structure.
    """
    normal_record = re.compile('tar.gz$')
    file_walk = file_walker(directory)
    for file in file_walk:
        if re.search(normal_record, file) is not None:
            yield file


def find_tar_files(directory):
    """ Walks through a directory and finds all tarballs  *.tar.gz.

    Args:
        directory: - Path of files to be searched for tarballs.

    Returns:
        A generator object that will yield each tarball in a given directory structure.
    """
    normal_record = re.compile('.tar$')
    file_walk = file_walker(directory)
    for file in file_walk:
        if re.search(normal_record, file) is not None:
            yield file


def find_tar_files_in_tarball(tarball):
    """ Walks through a tarball file and finds all tar files inside.

    Args:
        tarball: - A tar file

    Returns:
        A generator object that will yield each file in a given tarball.
    """
    tar_files = re.compile('.tar$')
    with tarfile.open(tarball, "r") as f:
        for item in f.getmembers():
            if re.search(tar_files, item.name) is not None:
                file = f.extractfile(item)
                yield file


def find_process_log_file_in_tarfile(tarfileobject, search_string):
    """ Goes through list of files in a tar file and finds a process log file with a name
    that matches the search_string pattern.

    Args:
        tarfileobject:  A tarfileobject that contains treatment process logs.

    Returns:
        A file of the given search string found in a tar file.
    """
    treatment_process = re.compile(search_string)
    for item in tarfileobject.getmembers():
        if re.search(treatment_process, item.name) is not None:
            log = tarfileobject.extractfile(item)
            yield log


def find_process_log_file_in_directory(directory, search_string):
    for log in file_walker(directory):
        full_path = directory +'/' + search_string
        if re.search(full_path, log) is not None:
            yield log
