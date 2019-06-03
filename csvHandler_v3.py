"""csv_handler.py reads test cases from test_suite.csv and write test result into test_result.csv."""
import csv
import os
import logger as tl
from test_config import TEST_OUTPUT_PATH, TEST_INPUT_DATA, TEST_RESULT_CSV


# load csv file into a list

def load_csv(input_csv_file):
    tl.test_logger.info('AXLE Integration Test started...')
    try:
        with open(input_csv_file) as input_data:
            test_suite = csv.DictReader(input_data)
            csv_header = test_suite.fieldnames
            tc_list = [row for row in test_suite]  # list comprehension
            if not test_suite:
                print('list is empty')
        return csv_header, tc_list
    except OSError as err:
        print('Failed to open the file as ', err)


def write_csv(test_result_csv, test_list, header):

    if not os.path.exists(TEST_OUTPUT_PATH):
        os.makedirs(TEST_OUTPUT_PATH)
    try:
        with open(test_result_csv, 'w', newline='') as output_file:
            f_writer = csv.DictWriter(output_file, header)
            f_writer.writeheader()
            for tc_row in test_list:
                # print(tc_row)
                tc_flag = tc_row['TEST_FLAG'].strip()
                tc_id = tc_row['TEST_CASE_ID'].strip()
                tc_row['TEST_RESULT'] = 'passed'
                if tc_flag.upper() == 'Y':  # iterate over the list and check if TC flag == 'Y'
                    print('Start execute test case: ' + tc_id)
                    f_writer.writerow(tc_row)
                elif tc_flag.upper() == 'N':
                    print('Skip execute test case: ' + tc_id + ' as flag is N!')
                else:
                    print('****Unexpected TC flag been assigned, please check the test_input_csv file!***')
            return True
    except OSError as err:
        print('Failed to open the file as ', err)


# load_test_input_list = load_csv(TEST_INPUT_DATA)
# result_header = load_test_input_list[0]
# test_case_list = load_test_input_list[1]
#
# write_csv(TEST_RESULT_CSV, test_case_list, result_header)
