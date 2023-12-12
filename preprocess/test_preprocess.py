
import unittest
import os
import pandas as pd
import glob
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.etree.ElementTree as ET
from preprocess.preprocess_snuh_ecg import find_diagnosis_statement, main
import preprocess.preprocess_snuh_ecg as preprocess_snuh_ecg

class TestConfig:
    vender = 'GE'
    output_path = '.'
    output_file_name = 'testdata.csv'
    output_columns = ['Filename', 'Vendor','Diagnosis Statement']
    xml_structure = ['Diagnosis','DiagnosisStatement', 'StmtText']  # if other xml structure, change code of find diagnosis statement
    remove_previous_result = True
   

class TestPreprocessSNUHECG(unittest.TestCase):
    def setUp(self):
        # Create a simple xml tree for testing
        self.root = Element('root')
        self.diagnosis = SubElement(self.root, 'Diagnosis')
        self.statement = SubElement(self.diagnosis, 'DiagnosisStatement')
        self.stmttext = SubElement(self.statement, 'StmtText')
        self.stmttext.text = 'Test statement'

        # Create a test xml file
        self.test_file = 'test.xml'
        with open(self.test_file, 'wb') as f:
            f.write(tostring(self.root))
        # Create a test folder with the test xml file
        self.test_folder = 'test_folder'
        os.makedirs(self.test_folder, exist_ok=True)
        os.rename(self.test_file, os.path.join(self.test_folder, self.test_file))

    def test_find_diagnosis_statement(self):
        config = TestConfig()
        config.xml_structure = ['Diagnosis', 'DiagnosisStatement', 'StmtText']
        tree = ET.ElementTree(self.root)
        result = find_diagnosis_statement(tree)
        self.assertEqual(result, ['Test statement'])

    def test_main(self):
        config = TestConfig() ## TODO Test Config 반영
        config.output_path = self.test_folder
        config.output_file_name = 'data.csv'
        config.remove_previous_result = True
        config.output_columns = ['Filename', 'Vendor', 'Diagnosis Statement']
        config.vender = 'GE'
        main(self.test_folder, self.test_folder)
        self.assertTrue(os.path.exists(os.path.join(config.output_path, config.output_file_name)))
        df = pd.read_csv(os.path.join(config.output_path, config.output_file_name))
        self.assertEqual(df.iloc[0]['Filename'], os.path.join(self.test_folder,'test.xml'))
        self.assertEqual(df.iloc[0]['Vendor'], 'GE')
        self.assertEqual(df.iloc[0]['Diagnosis Statement'], "['Test statement']")

    def tearDown(self):
        # Remove test files and folder
        if os.path.isfile(os.path.join(self.test_folder, self.test_file)):
            os.remove(os.path.join(self.test_folder, self.test_file))
        if os.path.isfile(os.path.join(self.test_folder, 'data.csv')):
            os.remove(os.path.join(self.test_folder, 'data.csv'))
        if os.path.exists(self.test_folder):
            os.rmdir(self.test_folder)

class TestExampleXML(unittest.TestCase):
    def setUp(self):
        xml_list = glob.glob(os.path.join("data_folder/test_data","*.xml"), recursive=True)
        self.et = [ET.parse(xml) for xml in xml_list]

    def test_find_diangosis_statement(self):
        config = TestConfig()
        output_file = os.path.join(config.output_path, config.output_file_name)
        df = pd.DataFrame(columns=config.output_columns)
        for tree in self.et:
            diagnosis_list = find_diagnosis_statement(tree)
            df = df._append({'Vendor':config.vender, 'Diagnosis Statement':str(diagnosis_list)}, ignore_index=True)                             
        df.to_csv(output_file, index=False)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()