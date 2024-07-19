from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .utils import *
from django.http import JsonResponse

# Create your views here.
@api_view(['POST'])
def yo(request):
    return HttpResponse("yuuuu")


@api_view(['POST'])
def pdf_compare(request):

    nuova_regola = request.data.get('regole', '')
    print(nuova_regola)

    if 'file1' in request.FILES and 'file2' in request.FILES:

        #Save PDFs into files folder
        file_path1, file_path2 = save_PDF(request)

        # PDF Compare
        res, pos_client_senza_match1, pos_client_senza_match2, data_ordine, renamed_data = get_ordine_conferma_ordine_data(file_path1, file_path2)

        # Aggiungi regole
        if nuova_regola != '':
            res_AI, result1_pos_cliente, result2_pos_cliente = aggiungi_regole(nuova_regola, data_ordine, renamed_data)
            pos_client_senza_match1, pos_client_senza_match2 = remove_resul12_from_array_senza_match(pos_client_senza_match1, pos_client_senza_match2, result1_pos_cliente, result2_pos_cliente)

            if res_AI != '':
                res = append_2_dict(res, res_AI)
                # print(res)
                # print(res_AI)
            else:
                res_AI = 'No match found'
        else:
            res_AI = 'stocazzo'

        # print(pos_client_senza_match1)
        # print(pos_client_senza_match2)
        response_data = {
            'res': res,
            'pos_cliente_senza_match1': pos_client_senza_match1,
            'pos_cliente_senza_match2': pos_client_senza_match2,
            'res_AI': res_AI
        }
        
        
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Both files are required'}, status=400)
