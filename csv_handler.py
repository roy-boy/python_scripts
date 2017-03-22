import csv
import os
import datetime

# to load the csv file inta a list

def get_csv_header():
    try:
        with open('mock_testInputCSV.csv', 'r') as f:
            reader = csv.reader(f)
            tc_list = list(reader)
            f.close()
        csv_header = tc_list[0]
    
    except OSError as err:
        print('Failed to open the file as ', err)
    return csv_header

header = get_csv_header()
#print(header)

field_names = ['target_file']
try:
    with open('mock_testInputCSV.csv', 'rb') as csv_f:
        with open('actual_testInput.csv', 'wb') as output_file:
            TC_list = csv.DictReader(csv_f)
            f_writer = csv.DictWriter(output_file, header)
            f_writer.writeheader()
        # interate over the list and check if TC flag == 'Y'
            for tc_row in TC_list:
                #print(tc_row)
                tc_flag = tc_row['Test_flag'].strip()
                tc_id = tc_row['TestCase_ID'].strip()
                trade_cpt = tc_row['Counterparty'].strip()
                test_timestamp = datetime.datetime.now()
                test_timestamp = test_timestamp.strftime('%d_%H_%M_%S_%f')
                tc_row['target_file'] = 'testID' + test_timestamp + '.xml'
                if tc_flag.upper() == 'Y':
                    
                    print('Start execute test case: ' + tc_id)
                    print(trade_cpt)
                    f_writer.writerow(tc_row)
                elif tc_flag.upper() == 'N':
                    print('Skip execute test case: ' + tc_id + ' as flag is N!')
                else:
                    print('****Unexpected TC flag been assigned, please check the test_input_csv file!***')
    
except OSError as err:
    print('Failed to open the file as ', err)
