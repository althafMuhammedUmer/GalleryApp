from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Post, Tag, Bookmark
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@login_required(login_url='user_login')
def index(request):
    post_list = Post.objects.all().order_by('-created_at')

    paginator = Paginator(post_list, 5)  # Number of posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        return JsonResponse({'posts': None})

    context = {
        "posts": posts
    }
    return render(request, 'index.html', context)

@login_required(login_url='user_login')
def bookmarkpage(request):
    mybookmarks = Bookmark.objects.filter(user=request.user)
    context = {
        "mybookmarks": mybookmarks
    }
    return render(request, 'bookmark.html', context)

@login_required(login_url='user_login')
def profile(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('created_at')
    userprofile = get_object_or_404(UserProfile, user=user)

    context = {
        "posts": posts,
        "userprofile": userprofile,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='user_login')
def search_posts(request):
    query = request.GET.get('q')

    if query:
        posts_by_caption = Post.objects.filter(caption__icontains=query)
        posts_by_tags = Post.objects.filter(tags__name__icontains=query)

        posts = (posts_by_caption | posts_by_tags).distinct() # distinct is used to remove duplicates
    
    else:
        posts = Post.objects.all()

    return render(request, 'index.html', {"posts": posts, "query": query })




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

@login_required(login_url='user_login')
def bookmark_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    existing_bookmark = Bookmark.objects.filter(user=request.user, post=post).first()

    if user in post.saved_by.all():
        post.saved_by.remove(user)
        existing_bookmark.delete()
        is_saved = False
    
    else:
        bookmark = Bookmark.objects.create(
                user=request.user,
                post=post
            )
        bookmark.save()
        post.saved_by.add(user)
        is_saved = True
    
    saveby_count = post.saved_by.count()
    print(saveby_count)

    return JsonResponse({'is_saved': is_saved, "saveby_count": saveby_count})
    
@login_required(login_url='user_login')
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user in post.liked_by.all():
        post.liked_by.remove(user)
        is_liked = False
    
    else:
        post.liked_by.add(user)
        is_liked = True
    
    likes_count = post.liked_by.count()

    return JsonResponse({'is_liked': is_liked, "likes_count": likes_count})


@login_required(login_url='user_login')
def deletePost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect(profile)

    




