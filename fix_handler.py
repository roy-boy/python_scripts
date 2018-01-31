import sys
import datetime
import rope_logger as tl
sys.path.insert(0, '../lib/simplefix/')
from message import FixMessage
from testProperty import TEST_OUTPUT_PATH


def log_test_output(text_to_log):
    test_log_file = TEST_OUTPUT_PATH + '/fix_diff_log.txt'
    with open(test_log_file, 'ab') as log_file:
        log_file.write(str(datetime.datetime.now()) + '>>>> ' + text_to_log + '\n')


def read_fix_msg(input_fix_file):
    """read and parse the input FIX message file and get the field value based on filed number
    :param input_fix_file: FIX message in flat file format
    :return:
        a FixMessage object
    """
    new_fix_msg = FixMessage()  # instantiate the FixMessage class
    try:
        with open(input_fix_file, 'rb') as input_fix:
            fix_msg_string = input_fix.readline()
        fix_msg_string = fix_msg_string.strip('"')  # trim the undesired double quote character
        fix_delimiter = chr(1)  # Get the 'SOH' character given by an ASCII number
        new_fix_msg_string = fix_msg_string.rstrip(fix_delimiter)  # trim the trailing delimiter
        log_test_output('input baseline FIX string: [' + new_fix_msg_string + ']')
        fix_string_list = new_fix_msg_string.split(fix_delimiter)  # split the input string into a list
        for fix_string in fix_string_list:
            new_fix_msg.append_string(fix_string)  # add the FIX field pair value into the new_fix_msg object
        return new_fix_msg
    except Exception:
        print('Baseline FIX is missing, check log for details!!!!')
        tl.test_logger.exception('FIX checked did NOT run as: ')


def read_fix_string(input_fix_string, fix_file_name):
    """read and parse the input FIX byte message file and save the message in text format
    :param input_fix_string: FIX message in byte format
    :param fix_file_name: FIX message file to be written
    :return:
        a FixMessage object
    """
    new_fix_msg = FixMessage()  # instantiate the FixMessage class
    try:
        with open(fix_file_name, 'wb') as input_fix:
            input_fix.write(input_fix_string)
        fix_delimiter = chr(1)  # Get the 'SOH' character given by an ASCII number
        new_fix_msg_string = input_fix_string.rstrip(fix_delimiter)  # trim the trailing delimiter
        log_test_output('input target FIX string: [' + new_fix_msg_string + ']')
        fix_string_list = new_fix_msg_string.split(fix_delimiter)  # split the input string into a list
        for fix_string in fix_string_list:
            new_fix_msg.append_string(fix_string)  # add the FIX field pair value into the new_fix_msg object
        return new_fix_msg
    except Exception:
        print('Target FIX is missing, check log for details!!!!')
        tl.test_logger.exception('FIX checked did NOT run as: ')


def compare_fix_msg(fix_msg_1, fix_msg_2, ignore_fields):
    """does smart fix message diff
    :param fix_msg_1: a instance of FixMessage as baseline FIX message
    :param fix_msg_2: a instance of FixMessage as target FIX message
    :param ignore_fields: a list of FIX tag number to be ignored when doing comparison
    :return:
        a string value as pass or fail
    """
    fix_diff_result = []
    overall_fix_diff_result = True
    zipped_fix_msg = zip(fix_msg_1, fix_msg_2)  # python builtin function zip() to align two lists for comparison
    fix_tag_count_1 = fix_msg_1.count()
    fix_tag_count_2 = fix_msg_2.count()
    baseline_fix_tag_list = []
    target_fix_tag_list = []
    for x in fix_msg_1:  # adding the tags to a list
        baseline_fix_tag_list.append(x[0])
    for y in fix_msg_2:  # adding the tags to a list
        target_fix_tag_list.append(y[0])
    target_fix_missing_tag = set(baseline_fix_tag_list) - set(target_fix_tag_list)  # Check if tag missing in target
    baseline_fix_missing_tag = set(target_fix_tag_list) - set(baseline_fix_tag_list)  # Check if tag missing in baseline
    if target_fix_missing_tag or baseline_fix_missing_tag:
        print('Test failed as FIX message tags does not match!!!')
        log_test_output('Test failed as FIX message tags does not match!!!')
        log_test_output('Baseline FIX message missing: ' + str(baseline_fix_missing_tag))
        log_test_output('Target FIX message missing: ' + str(target_fix_missing_tag))
        overall_fix_diff_result = False
    if fix_tag_count_1 != fix_tag_count_2:
        log_test_output('Baseline FIX tag count = ' + str(fix_tag_count_1))
        log_test_output('Target FIX tag count = ' + str(fix_tag_count_2))
        log_test_output('Test failed as FIX message fields counts does not match!!!')
        overall_fix_diff_result = False
        for fix_pair_1, fix_pair_2 in zipped_fix_msg:
            if fix_pair_1[0] not in ignore_fields:  # check if the tag should be ignored
                if fix_pair_1 != fix_pair_2:
                    log_test_output('FIX field value not matching, baseline: ' + str(fix_pair_1[0]) + '='
                                    + fix_pair_1[1] + ' target: ' + str(fix_pair_2[0]) + '=' + fix_pair_2[1])
    else:
        log_test_output('FIX message fields counts matches, moving on to check each fields value...')
        for fix_pair_1, fix_pair_2 in zipped_fix_msg:
            if fix_pair_1[0] not in ignore_fields:  # check if the tag should be ignored
                if fix_pair_1 != fix_pair_2:
                    log_test_output('FIX field value not matching, baseline: ' + str(fix_pair_1[0]) + '='
                                    + fix_pair_1[1] + ' target: ' + str(fix_pair_2[0]) + '=' + fix_pair_2[1])
                    fix_diff_result.append('Failed')
        if 'Failed' in fix_diff_result:
            overall_fix_diff_result = False
            log_test_output('FIX message comparison test failed.')
            print('FIX message comparison test failed.')
        else:
            log_test_output('FIX message comparison test passed.')
            print('FIX message comparison test passed.')
    log_test_output('Ignored FIX tags: ' + str(ignore_fields))
    return overall_fix_diff_result
