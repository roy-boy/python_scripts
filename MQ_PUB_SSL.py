import pymqi

def put_xml_to_mq_ssl(input_xml_file, q_name):
    """this function read the xml content into a string and put onto a MQ queue as testMessage"""
    put_mqmd = pymqi.md()
    put_mqmd["Format"] = 'MQSTR'  # This is to describe the message to be sent as jms_text Message type!!!!
    cd = pymqi.CD()
    cd.ChannelName = Q_CHANNEL_SSL
    cd.ConnectionName = CONN_INFO_SSL
    cd.ChannelType = pymqi.CMQC.MQCHT_CLNTCONN
    cd.TransportType = pymqi.CMQC.MQXPT_TCP
    cd.SSLCipherSpec = SSL_CIPHER_SPEC
    sco = pymqi.SCO()
    sco.KeyRepository = KEY_REPO_LOCATION
    tl.test_logger.info('sending message via SSL to MQ >> ' + Q_CHANNEL_SSL + ':' + q_name)
    qmgr = pymqi.QueueManager(None)
    qmgr.connect_with_options(Q_MANAGER_SSL, cd, sco)
    put_queue = pymqi.Queue(qmgr, q_name)
    with open(input_xml_file, 'r') as xml_file:
        xml_string_list = xml_file.readlines()
        xml_string = ''.join(str(e) for e in xml_string_list)
    try:
        put_queue.put(xml_string, put_mqmd)
        tl.test_logger.info('message published to MQ via SSL Channel!')
        put_queue.close()
        qmgr.disconnect()
        return True
    except Exception as exp:
        tl.test_logger.debug('Failed to put the xml to MQ via SSL: ', exp)
        put_queue.close()
        qmgr.disconnect()
        return False
