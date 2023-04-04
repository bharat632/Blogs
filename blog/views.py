from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Blog,Author,Tag
from django.views.generic import ListView, DetailView, View
from .forms import CommentForm
from  django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Blog
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
    
class AllPostView(ListView):
    template_name = "blog/all_post.html"
    model = Blog
    ordering = ["-date"]
    context_object_name = "posts"

class SinglePostView(View):

    def is_stored_blog(self, request, blog_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = blog_id in stored_posts
        else:
            is_saved_for_later = False
        
        return is_saved_for_later

    def get(self, request, slug):
        blog = Blog.objects.get(slug = slug) 

        context = {
            "post": blog,
            "post_captions":blog.caption.all(),
            "comment_form" : CommentForm(),
            "comments": blog.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_blog(request, blog.id)
        }
        return render(request, "blog/post-detail.html", context)
    

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        blog = Blog.objects.get(slug = slug) 

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.save()

            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))


        context = {
            "post": blog,
            "post_captions":blog.caption.all(),
            "comment_form" : CommentForm(),
            "comments": blog.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_blog(request, blog.id)
        }
        return render(request, "blog/post-detail.html", context)

class ReadLaterView(View):

    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context ={}

        if stored_posts is None or len(stored_posts)==0:
            context["posts"]=[]
            context["has_posts"]= False
        else:
            posts = Blog.objects.filter(id__in=stored_posts)
            context["posts"]=posts
            context["has_posts"]=True

        return render(request, "blog/stored-post.html", context)



    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/")
    