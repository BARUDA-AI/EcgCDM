import fire
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import os
### read xml file

class Config:
    """
    GE is vendor name of ECG machine

    ### xml structure in this Config #############
    #               | <DiagnosisStatement> - <StmtText>
    # <Diagnosis> - | <DiagnosisStatement> - <StmtText>
    #               | <DiagnosisStatement> - <StmtText>
    ### we extract the text in <StmtText> tag

    """
    vender = 'GE'
    output_file_name = 'data.csv'
    output_columns = ['Filename', 'Vendor','Diagnosis Statement']
    xml_structure = ['Diagnosis','DiagnosisStatement', 'StmtText']  # if other xml structure, change code of find diagnosis statement
    remove_previous_result = True

def find_diagnosis_statement(tree):
    config = Config()
    # TODO: 다양한 tree 구조 반영
    diagnosis = tree.find(config.xml_structure[0])
    if diagnosis is None:
        raise Exception(f"The xml file does not have the key config.xml_structure[0]")
    diagnosis_list = []

    for diagnosis_statement in diagnosis.findall(config.xml_structure[1]):
        if diagnosis_statement is None:
            raise Exception(f"The xml file does not have the key {config.xml_structure[1]}")
        diagnosis_statement_text = diagnosis_statement.find(config.xml_structure[2])
        if diagnosis_statement_text is not None:
            diagnosis_list.append(diagnosis_statement_text.text)


    return diagnosis_list 

def main(folder_name, output_folder = '.'):
    """
    read ecg xml file and output as a csv file

    Args: 
        folder_name (str) : the folder name that contains the xml files
        output_folder (str) : the folder name that output will be located
    
    Raises:
        FolderNotFoundError : if the folder does not exist
        ExsitFileError : if the csv file already exists
        KeyError : if the xml file does not follow given xml structure.
    
    Returns : create a csv file in the folder
    """
    config = Config()
    output_file = os.path.join(output_folder, config.output_file_name)

    if os.path.exists(output_file):
        if config.remove_previous_result:
            os.remove(output_file)
        else:
            raise Exception("The csv file already exists")

    if not os.path.exists(folder_name):
        raise Exception("The folder does not exist")
    xml_list = glob.glob(os.path.join(folder_name,"*.xml"), recursive=True)

    df = pd.DataFrame(columns=config.output_columns)

    tree_list = []
    for xml in xml_list:
        diagnosis_list =[]
        tree_list.append(ET.parse(xml))

    for xml, tree in zip(xml_list, tree_list):
        diagnosis_list = find_diagnosis_statement(tree)
        df = df._append({'Filename':xml, 'Vendor':config.vender, 'Diagnosis Statement':str(diagnosis_list)}, ignore_index=True)                                
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    fire.Fire(main)
