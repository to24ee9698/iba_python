import os
import re
import tarfile
import ParseTreatmentProcess
import ParseBeamCommonProcess
import ParsePMSProcess
import ParsePositionProcess
import ParsePbsRecorder
import ParseBeamAccessPointProcess

room = 1


def file_walker(directory):
    """ Walk a directory and yield all files in the directory. """
    for dirName, subdirList, file_list in os.walk(directory):
        for file_name in file_list:
            yield os.path.join(dirName, file_name)


def find_tar_gz_files(directory):
    """ Find all log files for the treatments in the system. """
    normal_record = re.compile('tar.gz$')
    file_walk = file_walker(directory)
    for file in file_walk:
        if re.search(normal_record, file) is not None:
            yield file


def find_tar_files_in_tarball(tarball):
   tarfiles = re.compile('.tar$')
   with tarfile.open(tarball,"r") as f:
            for item in f.getmembers():
                if re.search(tarfiles, item.name) is not None:
                    file = f.extractfile(item)
                    yield file


def convert_list_to_line(lst):
    return '{} - {} - {}'.format(lst[0],lst[1],lst[2])


def main(patient_id, directory):

    modified_directory = directory
    patient_list = []
    for zipped_tarballs in find_tar_gz_files(modified_directory):
        for tarball in find_tar_files_in_tarball(zipped_tarballs):
            with tarfile.open(fileobj=tarball) as f:
                ParseTreatmentProcess.find_treatment_process(f, patient_id, room, patient_list)
                for patient in patient_list:
                    ParseBeamCommonProcess.find_bcp_process(f, patient[0], patient[1])
                    ParseBeamAccessPointProcess.find_bap_process(f, patient[0], patient[1])
                    ParsePMSProcess.find_pms_process(f, patient[0], patient[1], room)
                    ParsePositionProcess.find_positioning_process(f, patient[0], patient[1])
                    ParsePbsRecorder.find_pbsdr_process(f, patient[0], patient[1])
                    filename = patient[0].create_file_name_from_id_start_time()
                    if patient[1] is not None and len(patient[1]) >= 1:
                        patient[1].sort(key=lambda x: x[0])
                        with open(filename, "a") as w:
                            for line_list in patient[1]:
                                w.write(convert_list_to_line(line_list))
                patient_list = []

#if __name__ == '__main__':
    #if len(sys.argv) != 3 and len(sys.argv[1]) != 6 and len(sys.argv[2]) > 0:
    #    print("Usage: python3 PatientLogWindow xxxxxx /TCS/runtimeStore"
    #          ", where xxxxxx is the Patient ID and"
    #          " /TCS/runtimeStore/log is the directory to search. ")
    #else:
 #   patientID = sys.argv[1]
 #   folder = sys.argv[2]

main('220875', '/p1/runtimeStore/log/Archive/Output')

