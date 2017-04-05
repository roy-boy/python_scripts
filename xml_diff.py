import xml.etree.ElementTree as ET
import logging
# import re


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
                xml_string = xml_string.replace(NAME_SPACE, '')
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
        baseline_trade_id = xml_tree_a.findtext('.//tradeId')
        target_trade_id = xml_tree_b.findtext('.//tradeId')

        if xml_tree_a.tag != xml_tree_b.tag:
            self.logger.debug('Tags do not match: %s and %s' % (xml_tree_a.tag, xml_tree_b.tag))
            return False
        for name, value in xml_tree_a.attrib.items():
            if name not in excludes:
                if xml_tree_b.attrib.get(name) != value:
                    self.logger.debug('Attributes do not match: %s=%r, %s=%r'
                                      % (name, value, name, xml_tree_b.attrib.get(name)))
                    return False
        for name in xml_tree_b.attrib.keys():
            if name not in excludes:
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
            i += 1
            if child_node_a.tag not in excludes:
                # print(child_node_a.tag)
                if not self.xml_compare(child_node_a, child_node_b, excludes):
                    self.logger.info('For test trade xml: baseline %s and target %s <<<<<<<<<<<<<'
                                     % (baseline_trade_id, target_trade_id))
                    self.logger.debug('children %i do not match: %s'
                                      % (i, child_node_a.tag))
                    return False
        return True

    @staticmethod
    def text_compare(node_text_a, node_text_b):
        """ Compare two text strings """
        if not node_text_a and not node_text_b:
            return True
        if node_text_a == '*' or node_text_b == '*':
            return True
        return (node_text_a or '').strip() == (node_text_b or '').strip()

# scripts to call and run the xml diff---------------------------------------------------------
# baseline_xml = 'gtr_us_pet_murex_fx_2540303_base.xml'
# target_xml = 'gtr_us_pet_murex_fx_2540303_target.xml'
#
# xml_comparator = XMLTree()
# root_1 = xml_comparator.load_xml(baseline_xml)
# root_2 = xml_comparator.load_xml(target_xml)
# if xml_comparator.xml_compare(root_1, root_2, IGNORE_TAGS):
#     print('XMLs match, test passed.')
# else:
#     print('Test Failed as XMLs do not match!!!')
