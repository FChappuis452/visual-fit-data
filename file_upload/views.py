from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def file_upload_form(request):
    return render(request, 'file_upload/upload.html')
