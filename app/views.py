from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Gallery

# Create your views here.

def index(request):
    gallery = Gallery.objects.all()
    context = {
        "images": gallery
    }
    return render(request, 'index.html', context)

def upload_image(request):
    if request.method == "POST":
        upload_image = request.FILES['image']
        gallery = Gallery.objects.create(image=upload_image)
        gallery.save()

        return redirect(index)
    
    else:
        return JsonResponse({'status': 'error', 'message': 'Image upload failed.'}) 
