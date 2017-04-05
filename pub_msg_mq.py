import pymqi


def put_xml_to_mq(input_xml_file):
    """this function read the xml content into a string and put onto a MQ queue as testMessage"""
    put_mqmd = pymqi.md()
    put_mqmd["Format"] = 'MQSTR'  # This is to describe the message to be sent as jms_text Message type!!!!
    logging.basicConfig(level=logging.INFO)
    qmgr = pymqi.connect(Q_MANAGER_LEGACY, Q_CHANNEL_LEGACY, Q_HOST_LEGACY + Q_PORT_LEGACY)
    with open(input_xml_file, 'r') as xml_file:
        xml_string_list = xml_file.readlines()
        xml_string = ''.join(str(e) for e in xml_string_list)
    try:
        qmgr.put1(Q_NAME_LEGACY, xml_string, put_mqmd)
        print('message published to MQ via Non-SSL Channel!')
        return True
    except Exception as exp:
        print('Failed to put the xml to MQ: ', exp)
        return False
    qmgr.disconnect()
    
