import csv

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

# Create your views here.

def file_upload_form(request):
    if request.method == 'POST':
        request.FILES['csv_file']
        fs = FileSystemStorage()
        name = fs.save(request.FILES['csv_file'].name, request.FILES['csv_file'])
        # response = processCSV(name)
    return render(request, 'file_upload/upload.html')


def processCSV(csvfile):

    csvfile = csvfile.decode('utf-8')
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        print(row)
    

    # content = csv_file.decode("utf-8")
    # print(content)
    # content = content.split("\r\n")
    # print(content[0])
    