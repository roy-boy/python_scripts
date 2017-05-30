#!C:\Python27\
"""File_getter.py copies xml or csv file from share-drive to local test_output_data folder"""

import shutil
import os
import treeth_logger as tl
from testProperty import TEST_BIN_DIR


def copy_output_file(src_file_name, dst_path):
    """Copy the file from share drive to local test dir for assertion."""
    try:
        shutil.copy2(src_file_name, dst_path)
        tl.test_logger.info('File copied successfully.')
        return True
    except IOError as err:
        tl.test_logger.debug(err)
        return False


def sftp_get_file(host_name, remote_file_path, file_name, target_location):
    """get the file from test Linux server to local test dir for assertion."""
    sftp_string = TEST_BIN_DIR + 'WinSCP.com /command "open sftp://user_name:pwd@' + host_name + '" ' + '"get ' \
                  + remote_file_path + file_name + ' ' + target_location + '" ' + '"exit"'
    try:
        file_download_process = os.system(sftp_string)
        if file_download_process == 0:
            tl.test_logger.info('File downloaded successfully from test server.')
            return True
        else:
            tl.test_logger.debug('File downloaded failed from test server, check your server file path!!!')
            return False
    except OSError as err:
        tl.test_logger.debug(err)
        return False


def sftp_put_file(host_name, local_file_path, file_name, target_location):
    """get the file from test Linux server to local test dir for assertion."""
    sftp_string = TEST_BIN_DIR + 'WinSCP.com /command "open sftp://user_name:pwd@' + host_name + '" ' + '"gut ' \
                  + local_file_path + file_name + ' ' + target_location + '" ' + '"exit"'
    try:
        file_upload_process = os.system(sftp_string)
        if file_upload_process == 0:
            tl.test_logger.info('File uploaded successfully to test server.')
            return True
        else:
            tl.test_logger.debug('File uploaded failed to test server.')
            return False
    except OSError as err:
        tl.test_logger.debug(err)
        return False


# sftp_get_file('unix_server', '/data/out/', 'test.xml', '..\\test_output_data\\xml\\')
