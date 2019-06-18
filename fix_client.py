"""fix_client.py is FIX client to send FIX message to server via socket"""
import asyncore
import socket
import simplefix
import logger as tl
import datetime
import time
from test_config import (HEART_BEAT_INTERVAL, ORDER_STATUS, SESSION_STATE, FIX_LOGON, FIX_HB,
                         FIX_LOGOFF, TargetCompID, SOCKET_ERROR)


# to initialise the session state
currentState = SESSION_STATE['NO_SESSION']


class FIXClient(asyncore.dispatcher):

    def __init__(self, host, port, nos_fix_msg):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = logon_buffer()
        self.fix_msg = nos_fix_msg

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def readable(self):
        return True

    def handle_read(self):
        print("----------INBOUND----------")
        tl.test_logger.info('Receiving inbound FIX message from Daxle adapter...')
        msg = self.recv(8192)
        if msg:
            self.parse_fix(msg)

    def writable(self):
        global currentState
        if currentState == SESSION_STATE['LOGON_SENT']:
            self.buffer = nos_buffer(self.fix_msg)
            currentState = SESSION_STATE['NOS_SENT']
        elif currentState in (SESSION_STATE['LOGON_SENT'], SESSION_STATE['NOS_SENT'], SESSION_STATE['HEART_BEAT_SENT']):
            self.buffer = heart_beat_buffer()
            currentState = SESSION_STATE['HEART_BEAT_SENT']
            time.sleep(HEART_BEAT_INTERVAL)
        return len(self.buffer) > 0

    def handle_write(self):
        print("----------OUTBOUND----------")
        tl.test_logger.info('Sending outbound FIX message to Daxle adapter...')
        time.sleep(3)
        print(self.buffer.decode('ASCII'))
        tl.test_logger.info(self.buffer.decode('ASCII'))
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def handle_expt(self):
        self.handle_error()
        tl.test_logger.error(SOCKET_ERROR)

    def handle_error(self):
        print("System Error, exiting...")
        tl.test_logger.error(SOCKET_ERROR)
        exit(-1)

    def parse_fix(self, raw_msg):
        global currentState
        order_status = ''
        fix_parser = simplefix.FixParser()
        fix_parser.append_buffer(raw_msg)
        fix_msg = fix_parser.get_message()
        print(fix_msg)  # dump the inbound FIX message
        tl.test_logger.info('Incoming FIX: ' + str(fix_msg))
        if fix_msg.get(39):
            order_status = fix_msg.get(39).decode('ASCII')
        msg_type = fix_msg.get(35).decode('ASCII')
        if msg_type == 'A':
            currentState = SESSION_STATE['LOGON_SENT']
        elif msg_type == '8':
            currentState = SESSION_STATE['EXECUTION_REPORT_RECEIVED']
        elif msg_type == '5':
            currentState = SESSION_STATE['LOG_OUT']

        if currentState == 5:
            tl.test_logger.info('Daxle Deal booking done.')
            raise asyncore.ExitNow('Test done, stop socket loop now...')
        elif order_status == ORDER_STATUS['FILLED'] and currentState == 4:
            print('Daxle Oder Status is FILLED')
            tl.test_logger.info('Daxle Oder Status is FILLED, logout FIX session...')
            self.buffer = logoff_buffer()
        elif order_status == ORDER_STATUS['PARTIALLY_FILLED'] and currentState == 4:
            print('Daxle Oder Status is PARTIALLY FILLED')
            tl.test_logger.info('Daxle Oder Status is PARTIALLY FILLED, logout FIX session...')
            self.buffer = logoff_buffer()
        elif order_status == ORDER_STATUS['REJECTED'] and currentState == 4:
            print('Daxle Oder Status is REJECTED')
            tl.test_logger.info('Daxle Oder Status is REJECTED, logout FIX session...')
            self.buffer = logoff_buffer()
        elif order_status == ORDER_STATUS['CANCELLED'] and currentState == 4:
            print('Daxle Oder Status is CANCELLED')
            tl.test_logger.info('Daxle Oder Status is CANCELLED, logout FIX session...')
            self.buffer = logoff_buffer()


# load fix file into a fix message object
def load_fix(input_fix_file):
    """read from FIX text file return a fix object with updated timestamp"""
    tl.test_logger.info('test input fix file is loaded.')
    new_fix_msg = simplefix.FixMessage()  # instantiate the FixMessage class
    global client_order_id
    try:
        with open(input_fix_file, 'r') as input_fix:
            fix_msg_string = input_fix.readline()
        #  fix_delimiter = chr(1)  # Get the 'SOH' character given by an ASCII number
        fix_string_list = fix_msg_string.split('|')  # split the input string into a list
        for fix_string in fix_string_list:
            if fix_string[:3] == '52=':  # update the timestamp
                fix_string = '52=' + datetime.datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]
            if fix_string[:3] == '60=':
                fix_string = '60=' + datetime.datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]
            if fix_string[:3] == '49=':  # update the targetCompID for different test ENV
                fix_string = '49=' + TargetCompID
            if fix_string[:3] == '11=':  # update the targetCompID for different test ENV
                client_order_id = 'AIT' + datetime.datetime.utcnow().strftime("%Y%m%d-%H-%M-%S%f")[:-6]
                fix_string = '11=' + client_order_id
            new_fix_msg.append_string(fix_string)  # add the FIX field pair value into the new_fix_msg object
        # print(new_fix_msg)
        return new_fix_msg
    except IOError:
        print('FIX is missing, check log for details!!!!')
        tl.test_logger.exception('FIX checked did NOT run as: ')


# to return the client order id to track the deal
def get_order_id():
    print('client order ID = ' + client_order_id)
    return client_order_id


#  logon fix to be sent
def logon_buffer():
    logon_fix = load_fix(FIX_LOGON)
    return logon_fix.encode()


# HB fix to be sent
def heart_beat_buffer():
    heart_beat_fix = load_fix(FIX_HB)
    return heart_beat_fix.encode()


# NOS fix to be sent
def nos_buffer(fix_file):
    nos_fix = load_fix(fix_file)
    return nos_fix.encode()


#  logoff fix
def logoff_buffer():
    logoff_fix = load_fix(FIX_LOGOFF)
    return logoff_fix.encode()
#  below to call this client:
# FIXClient(HOST, PORT, FIX_PATH + test_case['FIX_FILE'])
#        try:
#            asyncore.loop()
#        except Exception as e:
#            print(e)

