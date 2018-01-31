#!C:\Python27\
"""th_logger.py holds logging handler and config for the Regression test"""

import logging
from testProperty import TEST_OUTPUT_PATH

test_logger = logging.getLogger('TEST_HARNESS')
handler = logging.FileHandler(TEST_OUTPUT_PATH + 'runTest.log')
formatter = logging.Formatter('%(asctime)s %(name)-10s %(levelname)-6s %(message)s')
handler.setFormatter(formatter)
test_logger.addHandler(handler)
test_logger.setLevel(logging.DEBUG)
