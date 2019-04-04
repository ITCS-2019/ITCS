from django.shortcuts import render

def index_page(request):
    return render(request,"index.html")

def page_not_found(request):
    return render(request,"page-404.html")

def server_error(request):
    return render(request,"page-500.html")
