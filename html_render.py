"""html_render.py converts csv to a html test report."""

import datetime
from csv_handler import load_csv
from lib import HTML
import logger as tl
from test_config import TEST_OUTPUT_PATH, TEST_RESULT_CSV


def produce_report():

    test_timestamp = datetime.datetime.now()
    test_timestamp = test_timestamp.strftime('%y-%m-%d-%H-%M-%S')
    tl.test_logger.info('Producing HTML test report...')
    html_file = TEST_OUTPUT_PATH + test_timestamp + '-test_result.html'
    # dict of colors for each result:
    result_colors = {
            'passed':      'lime',
            'failed':      'red',
            'unknown':     'yellow',
        }
    # to load test result csv file:
    load_test_result_list = load_csv(TEST_RESULT_CSV)
    result_header = load_test_result_list[0]
    test_result_list = load_test_result_list[1]
    t = HTML.Table(header_row=result_header)
    for test_case in test_result_list:
        fill_color = result_colors[test_case['TEST_RESULT']]  # to set color to the cell
        colored_result = HTML.TableCell(test_case['TEST_RESULT'], bgcolor=fill_color)
        t.rows.append([test_case['TEST_FLAG'], test_case['TEST_CASE_ID'], test_case['TEST_CASE_NAME'],
                       test_case['REGION'], test_case['VENUE'], test_case['TRADE_TYPE'], test_case['TRADE_YAML'],
                       test_case['TRADE_ID'], colored_result])
    html_code = str(t)
    # print(html_code)
    try:
        with open(html_file, 'w') as html_report:
            html_report.write('<H2 style="font-family:verdana">Integration Smoke Test Result</H2>')
            html_report.write('<p style="font-family:verdana">Execution time: ' + test_timestamp)
            html_report.write(html_code)
            html_report.write('</p>')
    except OSError as err:
        print('Failed to open the file as ', err)

produce_report()
