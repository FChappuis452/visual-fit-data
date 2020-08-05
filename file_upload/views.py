import csv
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.shortcuts import render

# Create your views here.

# def file_upload_form(request):
#     if request.method == 'POST' and request.FILES['csv_file']:
#         file_content = request.FILES['csv_file']
#         fs = FileSystemStorage()
#         filename = fs.save(file_content.name, file_content)
    
#         processCSV(filename)
            
        
#         # fs = FileSystemStorage()
#         # name = fs.save(request.FILES['csv_file'].name, request.FILES['csv_file'])
#         # response = processCSV(name)
#     return render(request, 'file_upload/upload.html')


# def processCSV(csvfile):
#     with open(os.path.join(settings.MEDIA_ROOT, csvfile), 'r') as f:
#         reader = csv.reader(f, delimiter=',')
#         i = next(reader)
        
#         for row in reader:
#             print(row[0])
#     os.remove(os.path.join(settings.MEDIA_ROOT, csvfile))