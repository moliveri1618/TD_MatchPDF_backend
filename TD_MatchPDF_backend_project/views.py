from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .utils import *
from django.http import JsonResponse

# Create your views here.
@api_view(['POST'])
def yo(request):
    return HttpResponse("yuuuu")

all_ai_matches = []
@api_view(['POST'])
def pdf_compare_ordine_e_conferma(request):
    global all_ai_matches

    # Get data from session
    isPageReloaded = request.data.get('isPageReloaded', '')
    if isPageReloaded == 'true': all_ai_matches = []
    
    nuova_regola = request.data.get('regole', '')
    nuova_regola_list = nuova_regola_safe_check(nuova_regola)
    # print(nuova_regola_list)
    # print(isPageReloaded)

    if 'file1' in request.FILES and 'file2' in request.FILES:

        #Save PDFs into files folder
        file_path1, file_path2 = save_PDF(request, 'Files')

        # PDF Compare
        res, pos_client_senza_match1, pos_client_senza_match2, data_ordine, renamed_data = get_ordine_conferma_ordine_data(file_path1, file_path2)

        # Aggiungi regole
        if nuova_regola_list != '':
            print(nuova_regola_list[-1])
            res_AI, result1_pos_cliente, result2_pos_cliente = aggiungi_regole(nuova_regola_list[-1], data_ordine, renamed_data)
            pos_client_senza_match1, pos_client_senza_match2 = remove_resul12_from_array_senza_match(pos_client_senza_match1, pos_client_senza_match2, result1_pos_cliente, result2_pos_cliente)

            if res_AI != '':
                all_ai_matches.append(res_AI.copy())
                for item in all_ai_matches: res = append_2_dict(res, item)
                # append_2_dict(res, res_AI)
                # print(res)
                # print(all_ai_matches[0])
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


@api_view(['POST'])
def pdf_compare_contratto_ordine(request):

    if 'file1' in request.FILES and 'file2' in request.FILES:

        #Save PDFs into files folder
        file_path1, file_path2 = save_PDF(request, 'Files_contratto_ordine')

        # PDF Compare
        matched_list, list1_no_match, list2_no_match = get_contratto_ordine_data(file_path1, file_path2, 'Files_contratto_ordine')
        response_data = {
            'matched_list': matched_list,
            'no_match_list_ordine': list1_no_match,
            'no_match_list_contratto': list2_no_match
        }

        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Both files are required'}, status=400)

