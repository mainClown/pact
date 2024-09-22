# from django.shortcuts import render


from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile

def home(request):
    return render(request, 'home.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('display_files')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})

def display_files(request):
    files = UploadedFile.objects.all()
    return render(request, 'display_files.html', {'files': files})