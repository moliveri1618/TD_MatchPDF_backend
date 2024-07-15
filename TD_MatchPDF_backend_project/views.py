from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
@api_view(['POST'])
def yo(request):
    return HttpResponse("yuppiii")


# Create your views here.
@api_view(['POST'])
def pdf_compare(request):
    if 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        print('yoyo')
        print(f'Filename: {uploaded_file.name}')
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Save the uploaded file to the Files directory
        fs = FileSystemStorage(location=script_dir)
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        print(f'File saved at: {file_path}')

    else:
        print('No file uploaded')
    
    return HttpResponse("yuppiii")