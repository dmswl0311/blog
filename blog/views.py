from django.shortcuts import render,redirect
from .models import Blog,Comment
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json

def index(request):
    posts = Blog.objects.all().order_by('-created_at')
    paginator=Paginator(posts,3)
    now_page=request.GET.get('page')
    posts=paginator.get_page(now_page)
    context={
            "posts":posts
        }
    return render(request,'index.html',context)

def read(request,post_id):
    post=Blog.objects.get(id=post_id)
    comment = Comment.objects.filter(blog=post.id)
    context={
        "post":post,
        "comment":comment,
    }
    return render(request,'read.html',context)

def create(request):
    if request.method == "GET":
        return render(request,'create.html')

    elif request.method == "POST":
        post=Blog()

        post.user=request.user
        
        post.title=request.POST['title']
        post.content=request.POST['content']
        post.category=request.POST['category']
        try:
            post.pic=request.FILES['pic']
        except:
            pass

        post.save()

        return redirect(index)

def c_create(request,post_id):
    if request.method == "POST":
        comment = Comment() 
        comment.user = request.user 
        comment.blog = Blog.objects.get(id=post_id) 
        comment.content = request.POST['comment'] 
        anonymous = request.POST.get('anonymous',False)  
        if anonymous == "y":
            comment.anonymous = True
        comment.save() 
        return redirect(read,comment.blog.id)

def c_delete(request,comment_id):
    comment = Comment.objects.get(id=comment_id)
    pid=comment.blog.id
    comment.delete()
    return redirect(read,pid)

def update(request,post_id):
    if request.method=="GET":
        post=Blog.objects.get(id=post_id)
        context={
            "post":post
        }
        return render(request,'update.html',context)

    elif request.method=="POST":
        post=Blog.objects.get(id=post_id)
        post.title=request.POST['title']
        post.content=request.POST['content']
        post.save()
        return redirect(index)

def delete(request,post_id):
    post=Blog.objects.get(id=post_id)
    post.delete()
    return redirect(index)

def search(request):
    searcht=request.GET['search']
    search_filter=request.GET['search_filter']
    
    if search_filter=="제목":
        posts=Blog.objects.filter(title__icontains=searcht)
    elif search_filter=="내용":
        posts=Blog.objects.filter(content__icontains=searcht)
    elif search_filter=="제목과내용":
        posts=Blog.objects.all().filter(Q(title__icontains=searcht) | Q(content__icontains=searcht))
    context={
        "posts":posts
    }
    return render(request,'search.html',context)

def category(request):
    searchc=request.GET['category']
    posts=Blog.objects.filter(category=searchc)

    context={
        "posts":posts
    }
    return render(request,'category.html',context)

def like(request): 
    if request.is_ajax(): #ajax 방식일 때 아래 코드 실행
				# 좋아요 버튼 누른 post 데이터 불러오기
        post_id = request.GET['post_id'] 
        post = Blog.objects.get(id=post_id)
				
        if not request.user.is_authenticated: #버튼을 누른 유저가 비로그인 유저일 때
            message = "로그인을 해주세요" #화면에 띄울 메세지 
            context = {'like_count' : post.like.count(),"message":message}
            return HttpResponse(json.dumps(context), content_type='application/json')

        user = request.user #request.user : 현재 로그인한 유저
        if post.like.filter(id = user.id).exists(): #이미 좋아요를 누른 유저일 때
            post.like.remove(user) #like field에 현재 유저 추가
            message = "좋아요 취소" #화면에 띄울 메세지
        else: #좋아요를 누르지 않은 유저일 때
            post.like.add(user) #like field에 현재 유저 삭제
            message = "좋아요" #화면에 띄울 메세지
        # post.like.count() : 게시물이 받은 좋아요 수  
        context = {'like_count' : post.like.count(),"message":message}
        return HttpResponse(json.dumps(context), content_type='application/json')

