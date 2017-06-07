#!C:\Python27\
"""readeXML_diff.py compares two xml files with the option to ignore certain tags"""
import xml.etree.ElementTree as ET
import logging
from testProperty import NAME_SPACE, TEST_OUTPUT_PATH


class XMLTree:
    """This module takes two xml tree and does structure and text comparision for each node unless it's ignored."""

    def __init__(self):
        self.logger = logging.getLogger('xml_compare')
        self.logger.setLevel(logging.DEBUG)
        self.hdlr = logging.FileHandler(TEST_OUTPUT_PATH + 'xml-comparison.log')
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s- %(message)s')
        self.hdlr.setLevel(logging.DEBUG)
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)

    def load_xml(self, xml_file):
        """load the xml file into string and update it then write it back to the file."""
        xml_root = ''
        self.logger.info('started FPML comparison for test trade xml: %s <<<<<<<<<<<<<' % xml_file)
        try:
            with open(xml_file, 'r') as xml_input:
                xml_string_list = xml_input.readlines()
                if 'cyb' in str(xml_file):  # this is to drop the undesired line in FPML came from CYB trades
                    if '?xml' not in str(xml_string_list[0]):  # to check if the FPML has been tempered already
                        xml_string_list.pop(0)
                        xml_string_list.pop(0)
                        last_index = len(xml_string_list) - 1
                        xml_string_list.pop(last_index)
                        last_index -= 1
                        xml_string_list.pop(last_index)
                        xml_string = ''.join(str(e) for e in xml_string_list)
                        xml_f = open(xml_file, 'w')
                        xml_f.write(xml_string)
                        xml_f.close()
            tree = ET.parse(xml_file)
            xml_root = tree.getroot()
        except IOError as err:
            print('Failed to open the file as ', err)
        return xml_root

    def xml_compare(self, xml_tree_a, xml_tree_b, excludes=[]):
        """ compare two xml trees for syntax and value of each node which is not in the exclude list"""
        ns_excludes = []
        for tags in excludes:
            name_space_tags = NAME_SPACE + tags
            ns_excludes.append(name_space_tags)
        # if xml_tree_a.tag not in ns_excludes and xml_tree_b.tag not in ns_excludes:
        if xml_tree_a.tag != xml_tree_b.tag:
            self.logger.debug('Tags do not match: %s and %s' % (str(xml_tree_a.tag).replace(NAME_SPACE, ''),
                                                                str(xml_tree_b.tag).replace(NAME_SPACE, '')))
            return False
        for name, value in xml_tree_a.attrib.items():
            if name not in ns_excludes:
                if xml_tree_b.attrib.get(name) != value:
                    self.logger.debug('Attributes do not match: %s=%r, %s=%r'
                                      % (name, value, name, xml_tree_b.attrib.get(name)))
                    return False
        for name in xml_tree_b.attrib.keys():
            if name not in ns_excludes:
                if name not in xml_tree_a.attrib:
                    self.logger.debug('target xml file has am attribute that baseline file is missing: %s'
                                      % name)
                    return False
        if not self.text_compare(xml_tree_a.text, xml_tree_b.text):
            self.logger.debug('FPML node: %r text not match, %r != %r'
                              % (str(xml_tree_a.tag).replace(NAME_SPACE, ''), xml_tree_a.text, xml_tree_b.text))
            return False
        if not self.text_compare(xml_tree_a.tail, xml_tree_b.tail):
            self.logger.debug('tail: %r != %r' % (xml_tree_a.tail, xml_tree_b.tail))
            return False
        tree_list_1 = list(xml_tree_a)
        tree_list_2 = list(xml_tree_b)
        diff_result = True
        if len(tree_list_1) > 0 and len(tree_list_2) > 0:
            i = 0
            j = 0
            for child_node_a, child_node_b in zip(tree_list_1, tree_list_2):
                if child_node_a.tag in ns_excludes and child_node_b.tag not in ns_excludes:
                    i += 1
                    if i < len(tree_list_1):
                        child_node_a_next = tree_list_1[i]
                        child_node_a = child_node_a_next
                if child_node_b.tag in ns_excludes and child_node_a.tag not in ns_excludes:
                    j += 1
                    if j < len(tree_list_2):
                        child_node_b_next = tree_list_2[j]
                        child_node_b = child_node_b_next
                else:
                    child_node_a = tree_list_1[i]
                    child_node_b = tree_list_2[j]
                    i += 1
                    j += 1
                if child_node_a.tag not in ns_excludes and child_node_b.tag not in ns_excludes:
                    if not self.xml_compare(child_node_a, child_node_b, excludes):
                        diff_result = False
        return diff_result

    @staticmethod
    def text_compare(node_text_a, node_text_b):
        """ Compare two text strings """
        if not node_text_a and not node_text_b:
            return True
        if node_text_a == '*' or node_text_b == '*':
            return True
        return (node_text_a or '').strip() == (node_text_b or '').strip()

# scripts to call and run the xml diff---------------------------------------------------------
# baseline_xml = '../test_input_data/fpml/a.xml'
# target_xml = '../test_output_data/fpml/b.xml'
# xml_comparator = XMLTree()
# root_1 = xml_comparator.load_xml(baseline_xml)
# root_2 = xml_comparator.load_xml(target_xml)
# IGNORE_TAGS = ['tradeId', 'creationTimestamp', 'messageId', 'executionDateTime', 'timestamps',
#                'onBehalfOf', 'actionType', 'businessUnit', 'partyTradeIdentifier', 'contactInfo']
# if xml_comparator.xml_compare(root_1, root_2, IGNORE_TAGS):
#     print('XMLs match, test passed.')
# else:
#     print('Test Failed as XMLs do not match!!!')
