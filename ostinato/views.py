from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import *
import bcrypt

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw)
        request.session['user_id'] = new_user.id
        return redirect('/home')
    return redirect('/')

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id = request.session['user_id'])
    posts = Post.objects.all()
    print(posts)
    context = {
        'user': user[0],
        'posts': posts
    }
    return render(request, 'home.html', context)

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/home')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def favorites(request, id):
    user = User.objects.get(id=id)
    user.liked_posts.all()
    context ={
        'posts': Post.objects.all()
    }
    return render(request, 'profile.html', context)

# def profile(request, id):
#     context = {
#         'user': User.objects.get(id=id),
#     }
#     return render(request, 'profile.html', context)


def create_post(request):
    posted_by = User.objects.get(id=request.session['user_id'])
    Post.objects.create(
        message=request.POST['mess'], 
        posted_by= posted_by,
        album = request.POST['album'],
        artist = request.POST['artist']
    )
    print('post created:', Post.objects.last().__dict__)
    return redirect('/home')

def post_comment(request, post_id):
    user = User.objects.get(id=request.session['user_id'])
    post = Post.objects.get(id=post_id)
    Comment.objects.create(
        comment = request.POST['comment'],
        user = user,
        post = post
    )
    print(Comment.objects.last().__dict__)
    return redirect('/home')

def delete_comment(request, id):
    delete = Comment.objects.get(id=id)
    delete.delete()
    return redirect('/home')

def delete_post(request, id):
    delete = Post.objects.get(id=id)
    delete.delete()
    return redirect('/home')


def add_likes(request, id):
    liked_message = Post.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/home')

def edit(request, user_id):
    info = User.objects.get(id=user_id)
    context ={
        'user': info
    }
    return render(request,'edit.html', context)

def update(request, user_id):
    if request.session['user_id'] != user_id:
        return redirect('/profile')
    
    errors = User.objects.edit_validator(request.POST)

    email_check = User.objects.filter(email__iexact=request.POST['email'])

    if email_check:
        if user_id != email_check[0].id:
            errors['email'] = 'Email already in use'

    if errors:
        for e in errors.values():
            messages.error(request,e)
        return redirect(f'/edit/{user_id}')
    else:
        user_update = User.objects.get(id=user_id)
        user_update.first_name = request.POST['first_name']
        user_update.last_name = request.POST['last_name']
        user_update.email = request.POST['email']
        user_update.save()
        print()
        return redirect(f'/edit/{user_id}')

def avatar(request):
    return render(request,'avatar.html')

def upload(request):
    if request.method =='POST':
        newimg = Document( 
            docfile = request.FILES['docfile'],
            user = User.objects.get(id=request.session['user_id'])
            )
        newimg.save()

        return HttpResponseRedirect('/upload')

    documents = Document.objects.all()
    user = User.objects.get(id=request.session['user_id'])
    images = user.files.all()
    if images:
        last_image = user.files.last()
        request.session['image'] = last_image.docfile.url

    return render(request, 'avatar.html', {'documents': images, 'last': last_image})

def delete_image(request, id):
    remove = Document.objects.get(id=id)
    remove.delete()
    return redirect('/upload')

def set_picture(request, id):
    file = Document.objects.get(id=id)
    Document.objects.create(
        docfile = file.docfile,
        user = User.objects.get(id=request.session['user_id'])
    )
    delete_image(request, id)
    return redirect('/upload')