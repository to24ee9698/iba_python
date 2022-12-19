import os
import re
import tarfile


def file_walker(directory):
    """" Walk a directory and yield all files in the directory.

    Args:
        directory: - Path of files to be walked through.

    Returns:
        A generator object that will yield each file in the directory when iterated over in a loop or next

    Raises:
        StopIteration: - If the directory does not exist
    """
    for dirName, subdirList, file_list in os.walk(directory):
        for file_name in file_list:
            yield os.path.join(dirName, file_name)


def find_tar_gz_files(directory):
    """ Walks through a directory and finds all tarballs  *.tar.gz.

    Args:
        directory: - Path of files to be searched for tarballs.

    Returns:
        A generator object that will yield each tarball in a given directory structure.

    Raises:
        StopIteration: - If the directory does not exist or at end of file list.
    """
    normal_record = re.compile('tar.gz$')
    file_walk = file_walker(directory)
    for file in file_walk:
        if re.search(normal_record, file) is not None:
            yield file


def find_tar_files_in_tarball(tarball):
    """ Walks through a tarball file and finds all tar files inside.

    Args:
        tarball: - A tar file

    Returns:
        A generator object that will yield a tar file in a given tarball.

    Raises:
        StopIteration: - If there are no or no more tarballs found.

    """
    tar_files = re.compile('.tar$')
    with tarfile.open(tarball, "r") as f:
        for item in f.getmembers():
            if re.search(tar_files, item.name) is not None:
                file = f.extractfile(item)
                yield file


def find_files_named(path, name):

    """ Given a path and name create a generator for all files that contain that name.

         Args:
             path: The directory where the files are stored.
             name: The name of the file used to search for files of a type.

         Returns:

             A generator that yields all files which contain a given name.

         Raises:

            StopIteration: if no file found.
    """
    file_generator = file_walker(path)
    for file_name in file_generator:
        match = re.search(name, file_name)
        if match is not None:
            yield file_name






