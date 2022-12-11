from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *

# Create your views here.
def classimage_view(request):
 
    if request.method == 'POST':
        form = FaceForm(request.POST, request.FILES)
 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('classimage:success'))
    else:
        form = FaceForm()
    return render(request, 'classimage/classimage.html', {'form': form})
 
 
def success(request):
    return HttpResponse('successfully uploaded')

def display_face_images(request):
 
    if request.method == 'GET':
 
        # getting all the objects of face.
        Faces = Face.objects.all()
        return render(request, 'classimage/display_image.html',
                       {'face_images': Faces})