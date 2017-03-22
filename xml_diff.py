import xml.etree.ElementTree as ET
import logging
#from testProperty import NEW_XML_PATH, NAME_SPACE, IGNORE_TAGS

NAME_SPACE = 'xmlns=\"http://www.blah\"'

IGNORE_TAGS = ['id', 'Timestamp']

class XMLTree():
    """ docstring for XmlTree"""
    def __init__(self):
        self.logger = logging.getLogger('xml_compare')
        self.logger.setLevel(logging.DEBUG)
        self.hdlr = logging.FileHandler('xml-comparison.log')
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s- %(message)s')
        self.hdlr.setLevel(logging.DEBUG)
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)

    def xml_compare(self, xml_tree_a, xml_tree_b, excludes=[]):
        """
        """
        baseline_trade_id = xml_tree_a.findtext('.//tradeId')
        target_trade_id = xml_tree_b.findtext('.//tradeId')

        if xml_tree_a.tag != xml_tree_b.tag:
            self.logger.debug('Tags do not match: %s and %s' % (xml_tree_a.tag, xml_tree_b.tag))
            return False
        for name, value in xml_tree_a.attrib.items():
            if not name in excludes:
                if xml_tree_b.attrib.get(name) != value:
                    self.logger.debug('Attributes do not match: %s=%r, %s=%r'
                                      % (name, value, name, xml_tree_b.attrib.get(name)))
                    return False
        for name in xml_tree_b.attrib.keys():
            if not name in excludes:
                if name not in xml_tree_a.attrib:
                    self.logger.debug('target xml file has am attribute that baseline file is missing: %s'
                                      % name)
                    return False
        if not self.text_compare(xml_tree_a.text, xml_tree_b.text):
            self.logger.debug('text: %r != %r' % (xml_tree_a.text, xml_tree_b.text))
            return False
        if not self.text_compare(xml_tree_a.tail, xml_tree_b.tail):
            self.logger.debug('tail: %r != %r' % (xml_tree_a.tail, xml_tree_b.tail))
            return False
        tree_list_1 = list(xml_tree_a)
        tree_list_2 = list(xml_tree_b)
        if len(tree_list_1) != len(tree_list_2):
            self.logger.debug('children length differs, %i != %i'
                              % (len(tree_list_1), len(tree_list_2)))
            return False
        i = 0
        for child_node_a, child_node_b in zip(tree_list_1, tree_list_2):
            i +=1
            if not child_node_a.tag in excludes:
                #print(child_node_a.tag)
                if not self.xml_compare(child_node_a, child_node_b, excludes):
                    self.logger.info('For test trade xml: baseline %s and target %s <<<<<<<<<<<<<'
                                     % (baseline_trade_id, target_trade_id))
                    self.logger.debug('children %i do not match: %s'
                                      % (i, child_node_a.tag))
                    return False

        return True

    def text_compare(self, node_text_a, node_text_b):
        """
        Compare two text strings
        """
        if not node_text_a and not node_text_b:
            return True
        if node_text_a == '*' or node_text_b == '*':
            return True
        return (node_text_a or '').strip() == (node_text_b or '').strip()

# scripts to call and run the xml diff---------------------------------------------------------

baseline_xml = 'base.xml'
target_xml = 'target.xml'
try:
    with open(baseline_xml, 'r') as xml_file:
        xml_string_list = xml_file.readlines()
        xml_string = ''.join(str(e) for e in xml_string_list)
        xml_string = xml_string.replace(NAME_SPACE, '')
    f1 = open(baseline_xml, 'w')
    f1.write(xml_string)
    f1.close()

    tree_1 = ET.parse(baseline_xml)
    root_1 = tree_1.getroot()
except IOError as err:
    print('Failed to open the file as ', err)
try:
    with open(target_xml, 'r') as xml_file:
        xml_string_list = xml_file.readlines()
        xml_string = ''.join(str(e) for e in xml_string_list)
        xml_string = xml_string.replace(NAME_SPACE, '')
    f2 = open(target_xml, 'w')
    f2.write(xml_string)
    f2.close()

    tree_2 = ET.parse(target_xml)
    root_2 = tree_2.getroot()
except IOError as err:
    print('Failed to open the file as ', err)

xml_comparator = XMLTree()
if xml_comparator.xml_compare(root_1, root_2, IGNORE_TAGS):
    print('XMLs match, test passed.')
else:
    print('Test Failed as XMLs do not match!!!')
