from django.shortcuts import render


def pesquisa_passo_um(request):
    return render(request, 'ces/pesquisa_passo_um.html', {'afirmacao': '“O sistema facilitou a solicitação de uma nova Dieta Especial”'})


def pesquisa_passo_dois(request):
    return render(request, 'ces/pesquisa_passo_dois.html')


def pesquisa_passo_tres(request):
    return render(request, 'ces/pesquisa_passo_tres.html')
