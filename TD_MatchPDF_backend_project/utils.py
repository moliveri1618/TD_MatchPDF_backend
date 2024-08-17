import re
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
import Levenshtein
from django.core.files.storage import FileSystemStorage
import os
import shutil
import string
import json
import fitz  # PyMuPDF
from .models import *

def tipologia_infissi_definer(text_line):

    if text_line in tipologia_infisso:
        return tipologia_infisso[text_line]
    else:
        return 'None'
    
def soglia_infissi_definer(text_line):
    if text_line in soglia_infissi:
        return soglia_infissi[text_line]
    elif text_line[:1] in soglia_infissi:
        return soglia_infissi[text_line[:1]]
    else:
        return 'None'

def nodo_centrale_definer(text_line):
    if text_line in nodo_centrale:
        return nodo_centrale[text_line]
    else:
        return 'None'
    
def Modello_finestra__cerniere_codice_vetro_infissi_pattern_definer(text_line):
    if text_line in modello_finestra:
        return modello_finestra[text_line], 1
    elif text_line in cerniere:
        return cerniere[text_line], 2
    else:
        return 'None', 'None'
        


def flattening_data(data):
    # Flattening the data so that each entry has just one element
    flattened_data = []
    for sublist in data:
        for item in sublist:
            flattened_data.append(item)

    return flattened_data



# name_mapping = {
#     'PF2Salone+Stu': 'PF2 Salone+Studio',
#     'PF2Salone': 'PF2 Salone',
#     'FissoLavander': 'Fisso Lavanderia',
#     'F2C.tta': 'F2 C.tta'
# }

# def rename_pos_cliente(data):
#     for item in data:
#         original_name = item['pos_cliente']
#         if original_name in name_mapping:
#             item['pos_cliente'] = name_mapping[original_name]
#     return data




def extract_data_from_page(text):
    lines = text.split('\n')
    extracted_data_list = []
    
    # Iterate through the lines
    i = 0
    while i < len(lines):
        # Check if the current line matches the target line
        if lines[i].strip() == "pos.. pos. cliente tipo":
            extracted_lines = lines[i:i+4]
            parts1 = extracted_lines[1].rsplit(' ', 1)
            parts2 = extracted_lines[2].lstrip().split()
            parts3 = extracted_lines[3].split()

            extracted_data_list.append({
                            'pos_cliente': parts1[0],
                            'tipo': parts1[1][:-5] + parts2[1],
                            'pezzi': parts2[0],
                            'BRM-L': parts3[1],
                            'BRM-A': parts3[0]
                            })
            # Move the index to the line after the extracted section
            i += 4
        else:
            # Move to the next line
            i += 1
    
    return extracted_data_list




def extract_data_from_ordine(pdf_path):
    reader = PdfReader(pdf_path)
    data = []
    
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()
        page_data = extract_data_from_page(text)

        if page_data:
            data.append(page_data)

    
    flattened_data = flattening_data(data)
    return flattened_data





def extract_number(input_string):
    number = ''
    for char in reversed(input_string):
        if char.isdigit():
            number = char + number
        else:
            break
    return number




def extract_word(input_string):
    number_start_index = None
    for i, char in enumerate(reversed(input_string)):
        if not char.isdigit():
            number_start_index = len(input_string) - i
            break
    
    if number_start_index is None:
        return ''  # The string consists only of digits
    else:
        word_part = input_string[:number_start_index]
        return word_part if word_part and not word_part.isdigit() else None




def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    arrays_of_strings = []
    arrays_of_strings = []
    
    # Replace sequences of whitespace with a newline
    formatted_text = re.sub(r'\s+', '\n', text)

    # Split the formatted text into lines
    lines = formatted_text.split('\n')
    
    # Iterate through the lines to find occurrences of "base"
    for i in range(len(lines)):
        if "base" in lines[i]:
            array_of_strings = lines[i+1:i+8]

            if ',' in array_of_strings[-1]:
                brm_a = array_of_strings[-2]
                brm_l = array_of_strings[-3]
                pezzi = array_of_strings[-4]
                tipo = extract_number(array_of_strings[-6]) + ' ' + array_of_strings[-5]
            else:
                brm_a = array_of_strings[-1]
                brm_l = array_of_strings[-2]
                pezzi = array_of_strings[-3]
                tipo = extract_number(array_of_strings[-5]) + ' ' + array_of_strings[-4]
            pos_cliente = array_of_strings[0][1:] + extract_word(array_of_strings[1])  

            arrays_of_strings.append({
                            'pos_cliente': pos_cliente,
                            'tipo': tipo,
                            'pezzi': pezzi,
                            'BRM-L': brm_l,
                            'BRM-A': brm_a
                            })
    
    return arrays_of_strings





def rename_pos_cliente2(data):
    # Count the occurrences of 'F1sxLavand'
    count = sum(1 for item in data if item['pos_cliente'] == 'F1sxLavand')
    
    # If there's more than one 'F1sxLavand', proceed with renaming
    if count > 1:
        counter = 1
        for item in data:
            if item['pos_cliente'] == 'F1sxLavand':
                item['pos_cliente'] = f'F1sxLavand{counter}'
                counter += 1
                
    return data




def guess_compare_strings(str1, str2):
    
    # Remove all spaces from the strings
    str1_clean = str1.replace(" ", "")
    str2_clean = str2.replace(" ", "")
    
    # Check if they are exactly the same
    if str1_clean == str2_clean:
        return True
    
    # Check if they contain 'sx' and 'dx'
    if ('sx' in str1_clean and 'dx' in str2_clean) or ('dx' in str1_clean and 'sx' in str2_clean):
        return False
    
    # Check if one string ends with '1' and the other ends with '2'
    if (str1_clean.endswith('1') and str2_clean.endswith('2')) or (str1_clean.endswith('2') and str2_clean.endswith('1')):
        return False
    
    # Check if they are different by only one character
    if Levenshtein.distance(str1_clean, str2_clean) <= 1:
        return True
    
    return False

def compare_data_AI(res, result1, result2):

    res[result1['pos_cliente']] = []

    if result1['tipo'] == result2['tipo'].replace(" ", ""): 
        res[result1['pos_cliente']].append(['tipo', 'true', 'true', 'true'])
    else:
        res[result1['pos_cliente']].append(['tipo', 'true', 'true', 'false'])

    if result1['pezzi'] == result2['pezzi'].replace(" ", ""): 
        res[result1['pos_cliente']].append(['pezzi', 'true', 'true', 'true'])
    else:
        res[result1['pos_cliente']].append(['pezzi', 'true', 'true', 'false'])

    if result1['BRM-L'] == result2['BRM-L'].replace(" ", ""): 
        res[result1['pos_cliente']].append(['BRM-L', 'true', 'true', 'true'])
    else:
        res[result1['pos_cliente']].append(['BRM-L', 'true', 'true', 'false'])

    if result1['BRM-A'] == result2['BRM-A'].replace(" ", ""): 
        res[result1['pos_cliente']].append(['BRM-A', 'true', 'true', 'true'])
    else:
        res[result1['pos_cliente']].append(['BRM-A', 'true', 'true', 'false'])

    return res

    

    

from collections import defaultdict

def compare_data(res, data_ordine, renamed_data):

    errors = {}
    matched_pairs = defaultdict(bool)

    for item1 in data_ordine:
        for item2 in renamed_data:

            if guess_compare_strings(item1['pos_cliente'], item2['pos_cliente']):
                matched_pairs[(item1['pos_cliente'], item2['pos_cliente'])] = True

                res[item1['pos_cliente']] = []
                errors[item1['pos_cliente']] = []

                if item1['tipo'] == item2['tipo'].replace(" ", ""): 
                    res[item1['pos_cliente']].append(['tipo', 'true', 'true', 'true'])
                else:
                    res[item1['pos_cliente']].append(['tipo', 'true', 'true', 'false'])
                    #errors[item1['pos_cliente']].append(['tipo', item1['tipo'], item2['tipo']])
                    errors[item1['pos_cliente']].append(['tipo---> PDF1 - ' + item1['tipo'], ' PDF2 - ' + item2['tipo']])


                if item1['pezzi'] == item2['pezzi'].replace(" ", ""):
                    res[item1['pos_cliente']].append(['pezzi', 'true', 'true', 'true'])
                else:
                    res[item1['pos_cliente']].append(['pezzi', 'true', 'true', 'false'])
                    #errors[item1['pos_cliente']].append(['pezzi', item1['tipo'], item2['tipo']])
                    errors[item1['pos_cliente']].append(['pezzi---> PDF1 - ' + item1['tipo'], ' PDF2 - ' + item2['tipo']])

                if item1['BRM-L'] == item2['BRM-L'].replace(" ", ""):
                    res[item1['pos_cliente']].append(['BRM-L', 'true', 'true', 'true'])
                else:
                    res[item1['pos_cliente']].append(['BRM-L', 'true', 'true', 'false'])
                    #errors[item1['pos_cliente']].append(['BRM-L', item1['tipo'], item2['tipo']])
                    errors[item1['pos_cliente']].append(['BRM-L---> PDF1 - ' + item1['tipo'], ' PDF2 - ' + item2['tipo']])

                if item1['BRM-A'] == item2['BRM-A'].replace(" ", ""):
                    res[item1['pos_cliente']].append(['BRM-A', 'true', 'true', 'true'])
                else:
                    res[item1['pos_cliente']].append(['BRM-A', 'true', 'true', 'false'])
                    errors[item1['pos_cliente']].append(['BRM-A---> PDF1 - ' + item1['tipo'], ' PDF2 - ' + item2['tipo']])

    # Unmatched items
    matched_pos_clienti_1 = {pair[0] for pair in matched_pairs}
    matched_pos_clienti_2 = {pair[1] for pair in matched_pairs}
    pos_cliente_senza_match1 = [item['pos_cliente'] for item in data_ordine if item['pos_cliente'] not in matched_pos_clienti_1]
    pos_client_senza_match2 = [item['pos_cliente'] for item in renamed_data if item['pos_cliente'] not in matched_pos_clienti_2]
    # print(pos_cliente_senza_match1)
    # print(pos_client_senza_match2)

    return res, pos_cliente_senza_match1, pos_client_senza_match2



def print_res(res):
    for key, value in res.items():
        print(f"'{key}': {value},\n")

    return 'diocane'


def save_PDF(request, folder_name):
    #Save files into Files directory
    uploaded_file1 = request.FILES['file1']
    uploaded_file2 = request.FILES['file2']
    # print(f'Filename 1: {uploaded_file1.name}')
    # print(f'Filename 2: {uploaded_file2.name}')

    # Define the directory to store the files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files_dir = os.path.join(script_dir, folder_name)
    # print(script_dir)

    # Delete all existing files in the directory
    if os.path.exists(files_dir):
        shutil.rmtree(files_dir)
    os.makedirs(files_dir)

    # Save the uploaded files to the Files directory
    fs = FileSystemStorage(location=files_dir)
    filename1 = fs.save(uploaded_file1.name, uploaded_file1)
    filename2 = fs.save(uploaded_file2.name, uploaded_file2)
    file_path1 = fs.path(filename1)
    file_path2 = fs.path(filename2)
    #print(f'File 1 saved at: {file_path1}')
    #print(f'File 2 saved at: {file_path2}')

    return file_path1, file_path2


def get_regola_from_pos_cliente(renamed_data_ordine, renamed_data, res, nuova_regola):

    #get the two pos client from nuova_regola
    pos_cliente_data_ordine = [entry['pos_cliente'] for entry in renamed_data_ordine]
    pos_cliente_data = [entry['pos_cliente'] for entry in renamed_data]

    #split into words
    words_in_nuova_regola = nuova_regola.split() 

    # Check if any word is in pos_cliente_data_ordine or pos_cliente_data
    translator = str.maketrans('', '', string.punctuation)
    words_in_nuova_regola = nuova_regola.translate(translator).split()


    matches = [word for word in words_in_nuova_regola if word in pos_cliente_data_ordine or word in pos_cliente_data]
    return matches 


def add_regola_to_res(res, nuova_regola, data_ordine, renamed_data):
    res.append()





def get_ordine_conferma_ordine_data(file_path1, file_path2):

    #Ordine
    data_ordine = extract_data_from_ordine(file_path1)
    renamed_data_ordine = rename_pos_cliente2(data_ordine)
    # for data in renamed_data_ordine:
    #     print(data)
    # print('...............')

    #Conferma
    extracted_text = extract_text_from_pdf(file_path2)
    renamed_data = rename_pos_cliente2(extracted_text)
    # for item in renamed_data:
    #     print(item)
    # print('...............')

    #Compare the two lists
    res = {}
    res, pos_client_senza_match1, pos_client_senza_match2 = compare_data(res, data_ordine, renamed_data)

    return res, pos_client_senza_match1, pos_client_senza_match2, data_ordine, renamed_data


def replace_index_with_label(errors):
    # Mapping of indices to labels
    index_to_label = {
        0: 'tipo',
        1: 'pezzi',
        2: 'BRM-L',
        3: 'BRM-A'
    }
    
    # New dictionary to store the replaced values
    replaced_errors = {}
    
    for key, error_list in errors.items():
        replaced_errors[key] = []
        for error in error_list:
            index, sub_index, value = error
            label = index_to_label.get(index, index)  # Replace index with label if it exists in the dictionary
            replaced_errors[key].append((label, sub_index, value))
    
    return replaced_errors

def split_last_two_word(my_string):
    # print('-------------')
    # print(list2)
    split_obj2 = my_string.split()
    last_two_words_obj2_tipologia_infisso = ' '.join(split_obj2[-2:])

    return last_two_words_obj2_tipologia_infisso

def convert_to_dict(errors):
    converted_dict = {}
    for key, error_list in errors.items():
        labels = set()  # Using a set to avoid duplicates
        for error in error_list:
            label, _, _ = error
            labels.add(label)
        converted_dict[key] = list(labels)  # Converting the set back to a list
    
    return converted_dict

def remove_empty_errors(errors_dict):
    return {k: v for k, v in errors_dict.items() if v}


def nuova_regola_safe_check(nuova_regola):

    if nuova_regola == '[]':
        nuova_regola_list = ''
    else:
        nuova_regola_list = json.loads(nuova_regola)

    return nuova_regola_list


# Function to normalize the string by removing punctuation and extra spaces
def normalize_string(s):
    return re.sub(r'\s+', ' ', re.sub(r'\W+', ' ', s)).strip().lower()

# Function to check for the presence of consecutive words
def is_full_string_match(words, array):
    longest_match = None
    longest_length = 0
    for element in array:
        normalized_pos_cliente = normalize_string(element['pos_cliente'])
        pos_words = normalized_pos_cliente.split()
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                substring = ' '.join(words[i:j])
                if substring == normalized_pos_cliente:
                    current_length = j - i
                    if current_length > longest_length:
                        longest_match = element
                        longest_length = current_length
    return longest_match


# Function to remove the matched substring from the original string
def remove_matched_substring(original_string, substring):
    pattern = re.compile(re.escape(substring), re.IGNORECASE)
    return pattern.sub('', original_string, count=1)



# Function to compare and create new lists
def remove_matches_from_list(list1, list2):
    matched_list = {}

    for key1 in list(list1.keys()):
        obj1 = list1[key1]
        
        # Iterate over the items in list2
        for key2 in list(list2.keys()):
            obj2 = list2[key2]
            # print(obj1['Tipologia Infisso'])
            # print(obj2['Tipologia Infisso'])
            # print(key1)
            
            if  obj1['Tipologia Infissi'] == obj2.get('Tipologia Infissi', obj1['Tipologia Infissi'])                                                   and \
                obj1['Soglia Infissi'] == obj2.get('Soglia Infissi', obj1['Soglia Infissi'])       and \
                obj1['Colore PVC'] == obj2.get('Colore PVC', obj1['Colore PVC'])          and \
                obj1['Modello Finestra'] == obj2.get('Modello Finestra', obj1['Modello Finestra']) and \
                obj1['Cerniere'] == obj2.get('Cerniere', obj1['Cerniere']):
                    
                    matched_list[str(key1) + ' match con ' + str(key2)] = obj1
                    
                    del list1[key1]
                    del list2[key2]
                    
                    break

    return matched_list, list1, list2


def aggiungi_regole(nuova_regola_list, renamed_data, renamed_data_conferma_ordine):

    # Convert the first string to lower case and split into words
    words_1 = normalize_string(nuova_regola_list).split()

    # Check for consecutive words in the second array
    result1 = is_full_string_match(words_1, renamed_data)

    if result1:
        #print(f"First Match found: {result1}")
        updated_nuova_regola = remove_matched_substring(nuova_regola_list, result1['pos_cliente'])
        #print(f"Updated nuova_regola_list: {updated_nuova_regola}")
        words_2 = normalize_string(updated_nuova_regola).split()
        result2 = is_full_string_match(words_2, renamed_data_conferma_ordine)

        if result2:
            #print(f"Second Match found: {result2}")
            res_AI = {}
            res_AI = compare_data_AI(res_AI, result1, result2)
            return res_AI, result1['pos_cliente'], result2['pos_cliente']
        else:
            #print("No second match found")
            res_AI = ''
            result1 = ''
            result2 = ''
            return res_AI, result1, result2
    else:
        #print("No second match found")
        res_AI = ''
        result1 = ''
        result2 = ''
        return res_AI, result1, result2



def append_2_dict(dict1, dict2):

    # Append the second dictionary to the first one
    for key, value in dict2.items():
        if key in dict1:
            dict1[key].extend(value)
        else:
            dict1[key] = value

    return dict1


def remove_duplicates_from_dict(all_ai_matches):

    seen_keys = set()
    unique_data = []

    for dictionary in all_ai_matches:
        # Get the key of the current dictionary
        key = next(iter(dictionary))
        # Check if the key is already in seen_keys
        if key not in seen_keys:
            # Add the key to seen_keys
            seen_keys.add(key)
            # Add the dictionary to unique_data
            unique_data.append(dictionary)

    return unique_data


def remove_resul12_from_array_senza_match(pos_client_senza_match1, pos_client_senza_match2, result1_pos_cliente, result2_pos_cliente):
    
    if result1_pos_cliente != '' and result2_pos_cliente != '':
        try:
            pos_client_senza_match1.remove(result1_pos_cliente)
        except ValueError:
            print(f"{result1_pos_cliente} not found in pos_client_senza_match1")
        
        try:
            pos_client_senza_match2.remove(result2_pos_cliente)
        except ValueError:
            print(f"{result2_pos_cliente} not found in pos_client_senza_match2")

    return pos_client_senza_match1, pos_client_senza_match2


def pdf_to_text(pdf_path, txt_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Initialize an empty string for the text content
    text_content = ""

    # Loop through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)  # Load page
        text_content += page.get_text()  # Extract text from page

    # Write the text content to a text file
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text_content)

    return 1

def get_obj2_tipologia_infissi(obj1, obj2):
    #print(obj2['Tipologia Infissi'])
    if obj2.get('Tipologia Infissi'):
        try:
            last_two_words_obj2_tipologia_infisso = split_last_two_word(obj2['Tipologia Infissi'])
            obj2['Tipologia Infissi'] = last_two_words_obj2_tipologia_infisso
        except KeyError:
            pass
    else:
        obj2['Tipologia Infissi'] = obj1['Tipologia Infissi']

    return obj2['Tipologia Infissi']



def pdf_rules2(context2):

    lines = context2.split('\n')
    all_obj = []
    res = {}
    n_obj = 1
    flag_specifiche_condizioni = 0

    for i in range(len(lines)):

        # Ignore empty lines
        if lines[i].strip() == "":
            continue
 
        if lines[i].strip() == "Infisso":

            try:
                for n in range(int(n_obj)):
                    all_obj.append(res)
                    # print(all_obj)
                    # print('\n')
            except ValueError:
                print(f"Skipping: {n_obj} is not an integer")

            res = {}
            n_obj = 0
            #print(lines[i-1].strip())

        if lines[i].strip()[:1] == "G" and "(" in lines[i]:
            if 'Fornitore'in lines[i]:

                #reset
                try:
                    for n in range(int(n_obj)):
                        all_obj.append(res)
                        # print(all_obj)
                        # print('\n')
                except ValueError:
                    print(f"Skipping: {n_obj} is not an integer")

                res = {}
                n_obj = 0

                res['Design'] = lines[i-1].strip()
                try:
                    n_obj = int(lines[i-2].strip())
                except (IndexError, ValueError) as e:
                    n_obj = 1
            
            # print(lines[i])
            split_string = lines[i].split("(", 1)
            res[split_string[0][1:].strip()] = split_string[1][:-1].strip()
            # print(split_string[0][1:])
            # print(split_string[1][:-1])

        if lines[i].strip() == 'CONDIZIONI' or lines[i].strip() == 'SPECIFICHE' and flag_specifiche_condizioni == 0:
            flag_specifiche_condizioni = 1
            all_obj.append(res)

        #print(lines[i].strip())

    return all_obj


def clean_and_enumerate(data):
    if data and isinstance(data[0], dict) and not data[0]:
        data = data[1:]  # Remove the first empty dictionary
    
    enumerated_data = {index + 1: obj for index, obj in enumerate(data)}
    return enumerated_data


def define_txtfile_path(folder_name, txt_file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files_dir = os.path.join(script_dir, folder_name)
    txt_path = os.path.join(files_dir, txt_file_name)

    return txt_path

def get_text_from_textfile(txt_path):

    # Open the file in read mode
    with open(txt_path, 'r') as file:
        # Read the content of the file
        content = file.read()

    return content

def remove_trash(list2):
    res = {k: v for k, v in list2.items() if 'ENOVA' not in v}

    return res

def colore_pvc_definer(text_line):
    if text_line in colore_pvc:
        return colore_pvc[text_line]
    else:
        return 'None'

def modello_finestra_definer(text_line):
    if text_line in modello_finestra:
        return modello_finestra[text_line]
    else:
        return 'None'
    

def cerniere_definer(text_line):
    #print('aa', text_line)
    if text_line[:1] in cerniere:
        #print('aaa', text_line[:1])
        #print('bbbb', cerniere[text_line[:1]])
        return cerniere[text_line[:1]]
    else:
        return 'None'


def  pdf_rules(context):

    lines = context.split('\n')
    all_obj = []
    res = obj_model
    flag = ''
    for i in range(len(lines)):

        if lines[i].strip() == "anta"             or \
           lines[i].strip() == "ferramenta"       or \
           lines[i].strip() == "accessori"        or \
           lines[i].strip() == "telaio"           or \
           lines[i].strip() == "vetro/pannello" :
            flag = lines[i].strip()

        # Ignore empty lines
        if lines[i].strip() == "":
            continue

        # Tipologia infissi  A1 A2
        if lines[i].strip() == 'tipo':

            porta_finestra = ''
            if i + 2 < len(lines):
                #print(lines[i + 2])
                if lines[i + 2] == 'pezzi':
                    lines[i + 2] = '414'

                if lines[i + 5] == 'porta':
                    porta_finestra = 'PORTA FINESTRA'
                elif lines[i + 5] == 'finestra':
                    porta_finestra = 'FINESTRA'
                elif lines[i + 4] == 'porta':
                    porta_finestra = 'PORTA FINESTRA'
                elif lines[i + 4] == 'finestra':
                    porta_finestra = 'FINESTRA'
                elif lines[i + 6] == 'porta':
                    porta_finestra = 'PORTA FINESTRA'
                elif lines[i + 6] == 'finestra':
                    porta_finestra = 'FINESTRA'

                if lines[i + 2].strip() in tipologia_infisso_porta_finestra: 
                    res['Tipologia Infissi'] = porta_finestra + ' ' + tipologia_infissi_definer(lines[i + 2].strip())
                else:
                    res['Tipologia Infissi'] = tipologia_infissi_definer(lines[i + 2].strip())

                res['Pos Cliente'] = lines[i + 1]
                #print(res['tipologia_infisso'])
                #print('------')

        # Soglia infissi  B1
        elif flag == 'telaio' and lines[i].strip() == 'col. esterno':
            soglia_infissi_check = res['Tipologia Infissi'].split()[:2]
            #print(soglia_infissi_check[0] == 'PORTA' and soglia_infissi_check[1] == 'FINESTRA')
            if i + 3 < len(lines) and soglia_infissi_check[0] == 'PORTA' and soglia_infissi_check[1] == 'FINESTRA':
                #print(lines[i+3].strip())
                res['Soglia Infissi'] = soglia_infissi_definer(lines[i + 3].strip())
                # print(res['Soglia Infissi'])
                # print('------')
            if i + 5 < len(lines): # Nodo centrale B3
                #print('pos cliente', res['Pos Cliente'])
                #print(lines[i+5].strip())
                yoo = colore_pvc_definer(lines[i+5].strip())
                #print(yoo)
                if yoo == 'None':
                    if i + 6 < len(lines): # Nodo centrale B3
                        #print(lines[i+6].strip())
                        res['Colore PVC'] = colore_pvc_definer(lines[i+6].strip())
                else:
                    res['Colore PVC'] = yoo

                #print(res['Colore pvc'])
                #print("--------")

        # Modello finestra C1
        elif flag == 'anta' and re.match(modello_finestra__cerniere_pattern, lines[i].strip()):
            #print('anta', lines[i].strip())
            stoca = modello_finestra_definer(lines[i].strip())
            if stoca != 'None':
                res['Modello Finestra'] = stoca

        # Cerniere D1
        elif flag == 'ferramenta' and re.match(cerniere_pattern, lines[i].strip()) and lines[i-1].strip() != 'alt. Maniglia':
            # print('ferramenta', lines[i].strip())
            # print('pos cliente', res['Pos Cliente'])
            stoca = cerniere_definer(lines[i].strip())
            if stoca != 'None':
                res['Cerniere'] = stoca

        # # accessori E1
        # elif flag == 'accessori' and re.match(modello_finestra__cerniere_pattern, lines[i].strip()):
        #     print('accessori', lines[i].strip())
        
        # vetro/pannello Fn1 - Fn2 - Fn3 
        elif flag == 'vetro/pannello' and re.match(vetro_pannello_pattern, lines[i].strip()):
            #print('vetro/pannello', lines[i].strip())
            # F1.1
            if re.match(vetro_pannello_Fn1_pattern, lines[i].strip()):
                #print('F1n', lines[i].strip())
                try:
                    if res['Codice vetro infissi']:
                        res['Codice vetro infissi'] += ',VETRO ' + lines[i].strip()
                except KeyError:
                        res['Codice vetro infissi'] = 'VETRO ' + lines[i].strip()

            # F1.2
            if lines[i].strip() in fermavetro_infisso:
                res['Fermavetro Infisso'] = fermavetro_infisso[lines[i].strip()]

            # F1.3
            if lines[i].strip() in canalina_interno_vetro_Infisso:
                res['Canalina interno vetro Infisso'] = canalina_interno_vetro_Infisso[lines[i].strip()]

        # Fn4
        elif flag == 'vetro/pannello' and 'ornamentale' in lines[i].strip():
            rs = str(extract_numbers(lines[i].strip()))
            #print(type(rs))
            if rs in vetri_ornamentali:
                res['Vetri Ornamentali'] = vetri_ornamentali[rs]

        # reset all if end of the entry
        elif lines[i].strip() == 'data:':
            #print('--------')
            #print(res)
            all_obj.append(res)
            res = {}
            flag = ''

        elif lines[i].strip() == 'pos..':
            is_end_of_obj = res.get('Pos Cliente', 'porco dio') # we are the end of the obj if post cliente exists, return all
            if is_end_of_obj != 'porco dio':
                all_obj.append(res)
                res = {}
                flag = ''

        # if lines[i].strip() == '6/11':  # for testing
        #     print('yoo')


        #print(lines[i].strip())
    

    return all_obj


def extract_numbers(string):
    # Use regex to find all sequences of digits in the string
    numbers = re.findall(r'\d+', string)
    
    # Convert the found sequences to integers
    numbers = [int(num) for num in numbers]
    
    return numbers[0]

def clean_list(lst):
    if lst[0] == {'Tipologia Infissi': '', 'Modello Finestra': '', 'Soglia Infissi': '', 'Colore PVC': '', 'Cerniere': '', 'Codice vetro infissi': '', 'Fermavetro Infisso': '', 'Canalina interno vetro Infisso':'', 'Vetri Ornamentali':''}:
        lst.pop(0)
    return lst

def delete_not_tipologia_infissi(list1):
    for key in list(list1.keys()):
        if list1[key]['Tipologia Infissi'] == '':
            del list1[key]

    return list1

def delete_not_infisso(list2):
    for key in list(list2.keys()):
        if list2[key]['Design'].lower() != 'infisso':
            del list2[key]

    return list2


def modify_list(list):
    # Transform the data
    transformed_data = {item.get("Pos Cliente", "").strip(): {
        "Tipologia Infissi": item.get("Tipologia Infissi", ""),
        "Soglia Infissi": item.get("Soglia Infissi", ""),
        "Colore PVC": item.get("Colore PVC", ""),
        "Modello Finestra": item.get("Modello Finestra", ""),
        "Cerniere": item.get("Cerniere", ""),
        "Codice vetro infissi": item.get("Codice vetro infissi", ""),
        "Vetri Ornamentali": item.get("Vetri Ornamentali", ""),
        "Fermavetro Infisso": item.get("Fermavetro Infisso", ""),
        "Canalina interno vetro Infisso": item.get("Canalina interno vetro Infisso", "")
    } for item in list}

    return transformed_data


def get_text_from_textfile2(txt_path):
    # Open the file in read mode with the correct encoding
    with open(txt_path, 'r', encoding='utf-8') as file:
        # Read the content of the file
        content = file.read()

    return content

def clean_dict(d):
    for key, value in d.items():
        if isinstance(value, dict):
            clean_dict(value)
        elif value == 'None':
            d[key] = ''
    return d

#####
def get_contratto_ordine_data(pdf_path1, pdf_path2, folder_name):
    
    # extract rules from ordine
    txt_path1 = define_txtfile_path(folder_name, "output.txt")
    pdf_to_text(pdf_path1, txt_path1)
    context1 = get_text_from_textfile(txt_path1)
    list1 = pdf_rules(context1)
    list1 = clean_list(list1)
    list1 = modify_list(list1)
    list1 = clean_dict(list1)
    list1 = delete_not_tipologia_infissi(list1)
    # print(list1)
    # print('\n')

    # extract rules from contratto
    txt_path2 = define_txtfile_path(folder_name, "output1.txt")
    pdf_to_text(pdf_path2, txt_path2)
    context2 = get_text_from_textfile2(txt_path2)
    list2 = pdf_rules2(context2)
    list2 = clean_and_enumerate(list2)
    list2 = remove_trash(list2)
    list2 = delete_not_infisso(list2)
    # print(list2)
    # print('\n')

    #compare and remove the matches
    # list2 = remove_keys(list2)
    # print(list2)
    matched_list, list1_no_match, list2_no_match = remove_matches_from_list(list1, list2)

    # print(matched_list)
    # print('\n')
    # print(list1_no_match)
    # print('\n')
    # print(list2_no_match)
    # print('\n')

    return matched_list, list1_no_match, list2_no_match
