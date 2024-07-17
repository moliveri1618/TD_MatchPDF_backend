import re
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
import Levenshtein
from django.core.files.storage import FileSystemStorage
import os
import shutil


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
    
    # # Check if one string ends with '1' and the other ends with '2'
    # if (str1_clean.endswith('1') and str2_clean.endswith('2')) or (str1_clean.endswith('2') and str2_clean.endswith('1')):
    #     return False
    
    # Check if they are different by only one character
    if Levenshtein.distance(str1_clean, str2_clean) <= 1:
        return True
    
    return False



def compare_data(res, data_ordine, renamed_data, nuova_regola):

    errors = {}
    for item1 in data_ordine:
        for item2 in renamed_data:
            if  (item1['pos_cliente'] == nuova_regola[0] and item2['pos_cliente'] == nuova_regola[1]) or \
                (item1['pos_cliente'] == nuova_regola[1] and item2['pos_cliente'] == nuova_regola[0]) or \
                guess_compare_strings(item1['pos_cliente'], item2['pos_cliente']):

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
    return res, errors



def print_res(res):
    for key, value in res.items():
        print(f"'{key}': {value},\n")

    return 'diocane'


def save_PDF(request):
    #Save files into Files directory
    uploaded_file1 = request.FILES['file1']
    uploaded_file2 = request.FILES['file2']
    print(f'Filename 1: {uploaded_file1.name}')
    print(f'Filename 2: {uploaded_file2.name}')

    # Define the directory to store the files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files_dir = os.path.join(script_dir, 'Files')
    print(script_dir)

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
    print(f'File 1 saved at: {file_path1}')
    print(f'File 2 saved at: {file_path2}')

    return file_path1, file_path2


def get_regola_from_pos_cliente(renamed_data_ordine, renamed_data, nuova_regola):
    pos_cliente_data_ordine = [entry['pos_cliente'] for entry in renamed_data_ordine]
    pos_cliente_data = [entry['pos_cliente'] for entry in renamed_data]

    # Split the nuova_regola into words
    words = nuova_regola.split()

   # Find matching words in the arrays
    ordine_match = None
    data_match = None
    
    for word in words:
        if word in pos_cliente_data_ordine:
            ordine_match = word
        if word in pos_cliente_data:
            data_match = word
    
    # Return the two words if both matches are found, otherwise return False
    if ordine_match and data_match:
        return ordine_match, data_match
    else:
        return False


def get_ordine_data(file_path1, file_path2, nuova_regola):

    #Ordine
    data_ordine = extract_data_from_ordine(file_path1)
    renamed_data_ordine = rename_pos_cliente2(data_ordine)
    for data in renamed_data_ordine:
        print(data)
    print('...............')

    #Conferma
    extracted_text = extract_text_from_pdf(file_path2)
    renamed_data = rename_pos_cliente2(extracted_text)
    for item in renamed_data:
        print(item)
    print('...............')

    #Nuova regola logic
    nuova_regola_error = ''
    if nuova_regola != ['null', 'null']:
        nuova_regola = get_regola_from_pos_cliente(renamed_data_ordine, renamed_data, nuova_regola)
        if nuova_regola == False:
            nuova_regola_error = 'No Match Found'
            nuova_regola = ['null', 'null']

    #Compare the two lists
    res = {}
    res, errors = compare_data(res, data_ordine, renamed_data, nuova_regola)
    errors = remove_empty_errors(errors)

    return res, nuova_regola_error, errors


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