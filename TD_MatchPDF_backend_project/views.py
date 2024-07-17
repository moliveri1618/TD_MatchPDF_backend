from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .utils import *
from django.http import JsonResponse

# Create your views here.
@api_view(['POST'])
def yo(request):
    return HttpResponse("hahahaha")


@api_view(['POST'])
def pdf_compare(request):

    nuova_regola = request.data.get('nuova_regola', ['null', 'null'])

    if 'file1' in request.FILES and 'file2' in request.FILES:

        #Save PDFs into files folder
        file_path1, file_path2 = save_PDF(request)

        # PDF Compare
        res = get_ordine_data(file_path1, file_path2, nuova_regola)

        errori = find_errors(res)

        response_data = {
            'res': res,
            'errori': errori
        }
        
        
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Both files are required'}, status=400)
