import pytest
import re
import file_helpers
import datetime
import iba_file_stucture.iba_compressed_files.iba_compressed_files


def test_parse_compressed_file_date_nominal():
    file_generator = file_helpers.file_walker("../../../data")  # Generator to walk files
    file_name = next(file_generator)  # First file found
    date = iba_file_stucture.iba_compressed_files.parse_compressed_file_date(file_name)  # Parse the Date
    target = datetime.datetime(2022, 12, 5)  # The First file should be
    assert date == target


def test_parse_compressed_file_date_exception():
    file_generator = file_helpers.file_walker("../../../data")  # Generator to walk files
    file_name = next(file_generator)
    with pytest.raises(ValueError):  # ValueError should be thrown on EmptyFile
        for file_name in file_generator:
            date = iba_file_stucture.iba_compressed_files.parse_compressed_file_date(file_name)  # Parse the Date


def test_parse_compressed_file_date_stop_iteration():
    file_generator = file_helpers.file_walker("../data")  # Generator to walk files
    with pytest.raises(StopIteration):
        file_name = next(file_generator)


def test_find_compressed_logs_dated_nominal_case():
    start = datetime.datetime(2022, 12, 7)  # Create a Start date
    stop = datetime.datetime(2022, 12, 8)  # Create a Stop date

    file_generator = iba_file_stucture.iba_compressed_files.find_compressed_logs_dated("../../../data", start, stop)
    count = 0
    for item in file_generator:
        count += 1
    assert count == 2


def test_find_compressed_logs_dated_stop_iteration():
    start = datetime.datetime(2022, 12, 7)  # Create a Start date
    stop = datetime.datetime(2022, 12, 10)  # Create a Stop date

    files = iba_file_stucture.iba_compressed_files.find_compressed_logs_dated("../../data", start, stop)
    with pytest.raises(StopIteration):
        file_name = next(files)


def test_find_compressed_logs_dated_missing_date():
    start = datetime.datetime(2022, 12, 7)  # Create a Start date

    with pytest.raises(TypeError):
        file_generator = iba_file_stucture.iba_compressed_files.find_compressed_logs_dated("../../../data", start, None)
        item = next(file_generator)


def test_find_room_log_file_in_compressed_tarball_nominal():

    start = datetime.datetime(2022, 12, 9)  # Create a Start date
    stop = datetime.datetime(2022, 12, 9)  # Create a Stop date

    compressed_logs_generator = iba_file_stucture.iba_compressed_files.find_compressed_logs_dated(
        "../../../data",
        start,
        stop)

    for item in compressed_logs_generator:
        try:
            file_generator = iba_file_stucture.iba_compressed_files.find_room_log_file_in_compressed_tarball(
                item,
                "pts-treat-proc",
                2)
            config_line = re.compile('pts-treat-proc-2')
            for logfile in file_generator:
                assert re.search(config_line, logfile[0])

        except StopIteration:
            print("No Log found")


def test_find_room_log_file_in_compressed_tarball_nominal_no_room():

    start = datetime.datetime(2022, 12, 9)  # Create a Start date
    stop = datetime.datetime(2022, 12, 9)  # Create a Stop date

    compressed_logs_generator = iba_file_stucture.iba_compressed_files.find_compressed_logs_dated(
        "../../../data",
        start,
        stop)

    for item in compressed_logs_generator:
        try:
            file_generator = iba_file_stucture.iba_compressed_files.find_room_log_file_in_compressed_tarball(
                item,
                "mcrhci",
                2)
            config_line = re.compile('mcr')
            for logfile in file_generator:
                assert re.search(config_line, logfile[0])

        except StopIteration:
            print("No Log found")


def test_find_room_log_file_in_compressed_tarball_no_file():

    start = datetime.datetime(2022, 12, 9)  # Create a Start date
    stop = datetime.datetime(2022, 12, 9)  # Create a Stop date

    compressed_logs_generator = iba_file_stucture.iba_compressed_files.find_compressed_logs_dated(
        "../../../data",
        start,
        stop)

    for item in compressed_logs_generator:
        file_generator = iba_file_stucture.iba_compressed_files.find_room_log_file_in_compressed_tarball(
            item,
            "pts-trick-proc",  # No such file found in IBA TCS logs.
            2)
        with pytest.raises(StopIteration):
            ghost_file = next(file_generator)


def test_find_named_dated_files_in_compressed_logs_nominal():
    test_date = datetime.datetime(2022, 12, 5)  # Create a Start date

    file_generator = iba_file_stucture.iba_compressed_files.find_named_dated_files_in_compressed_logs(
        "../../../data",
        "pts-treat-proc",
        2,
        test_date)

    for item in file_generator:
        try:
            config_line = re.compile('pts-treat-proc')
            for logfile in file_generator:
                assert re.search(config_line, logfile[0])

        except StopIteration:
            print("No Log found")