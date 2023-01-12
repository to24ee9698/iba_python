import pytest
import file_helpers.file_helpers


def test_file_walker_nominal():
    count = 0
    file_generator = file_helpers.file_walker("../../data")
    for file_name in file_generator:
        count += 1
    assert count == 16  # Nominal Case reads 19 files in the data directory


def test_file_walker_no_directory():
    file_generator = file_helpers.file_walker("./data")
    with pytest.raises(StopIteration):  # StopIteration should be thrown on empty directory.
        next(file_generator)


def test_find_tar_gz_files_nominal():
    count = 0
    file_generator = file_helpers.find_tar_gz_files("../../data")
    for file_name in file_generator:
        count += 1
    assert count == 15  # Should be 1 file less than the file walker nominal case.


def test_find_tar_gz_files_no_directory():
    file_generator = file_helpers.find_tar_gz_files("./data")
    with pytest.raises(StopIteration):  # StopIteration should be thrown on empty directory.
        next(file_generator)


def test_find_tar_files_in_tarball_nominal():
    file_generator = file_helpers.find_tar_gz_files("../../data")           # Create a generator for the files
    tarball = next(file_generator)                                          # Get a single tarball
    tar_file_generator = file_helpers. find_tar_files_in_tarball(tarball)   # Create a generator for the tar files
    count = 0
    for file_name in tar_file_generator:                                    # Count number of tar files
        count += 1
    assert count == 1                                                       # There should be 1 tar files per tarball


def test_find_files_name_nominal():
    count = 0
    file_generator = file_helpers.find_files_named("../../data", "OUTPUT")
    for file_name in file_generator:
        count += 1
    assert count == 15  # Should be 1 file less than the file walker nominal case.
                        # Number of files with "OUTPUT" in file name.



