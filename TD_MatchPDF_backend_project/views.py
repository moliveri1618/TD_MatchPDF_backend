from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.core.files.storage import FileSystemStorage
import os
import shutil


# Create your views here.
@api_view(['POST'])
def yo(request):
    return HttpResponse("hahahaha")


@api_view(['POST'])
def pdf_compare(request):

    if 'file1' in request.FILES and 'file2' in request.FILES:
        uploaded_file1 = request.FILES['file1']
        uploaded_file2 = request.FILES['file2']

        # Define the directory to store the files
        script_dir = os.path.dirname(os.path.abspath(__file__))
        files_dir = os.path.join(script_dir, 'Files')

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

        # Here you can add your logic to compare the PDF files
        # For example, you could use a library like PyPDF2 or pdfminer to extract text and compare

    else:
        print('Both files are required')

    return HttpResponse("Files received and processed")