from django.shortcuts import render


def tickets_page(request):
    return render(request, 'tickets/tickets_page.html')

