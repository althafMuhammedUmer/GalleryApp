from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Post, Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required(login_url='user_login')
def index(request):
    gallery = Post.objects.all()
    context = {
        "images": gallery
    }
    return render(request, 'index.html', context)

@login_required(login_url='user_login')
def create_post(request):
    if request.method == "POST":
        user = request.user
        image = request.FILES.get('image')
        tags_input = request.POST.get('tags', '')

        if not image or not tags_input:
            return JsonResponse({'error': 'Image and tags are required.'}, status=400)
        
        tags = [tag.strip() for tag in tags_input.split(',')]

        try:
            new_post = Post.objects.create(user=user, image=image)
            for tag_name in tags:
                tag, create = Tag.objects.get_or_create(name=tag_name)
                new_post.tags.add(tag)
            
            new_post.save()

            return JsonResponse({'message': 'Post created successfully.'})
        
        except Exception as e:
            return JsonResponse({'message': f'Error creating post: {str(e)}'}, status=400)
    
    else:
        return JsonResponse({'message':'something went wrong.'}) 
