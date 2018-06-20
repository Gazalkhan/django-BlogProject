from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Article
from django.contrib.auth.decorators import login_required
from . import forms
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.cache import patch_vary_headers


def article_list(request):
    articles = Article.objects.all().order_by('-date');
    return render(request, 'articles/article_list.html', { 'articles': articles })

def article_detail(request, slug):
    # return HttpResponse(slug)
    article = Article.objects.get(slug=slug)
    return render(request, 'articles/article_detail.html', { 'article': article })

@login_required(login_url="/accounts/login/")
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            # save article to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_create.html', { 'form': form })

@login_required(login_url="/accounts/login/")
def article_add_comment_to_post(request, slug):
    #return HttpResponse(slug)
    article = Article.objects.get(slug=slug)
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = article
            comment.author = request.user
            comment.save()
            return redirect('articles:detail', slug=article.slug)
    else:
        form = forms.CommentForm()
    return render(request, 'articles/article_add_comment_to_post.html', {'form': form})

@cache_page(900,key_prefix='mycache') #will be catched for 15 mins 60*15
def cache_view(request):
    cache_key= Article.title
   # cache_time = 86400  
    data = cache.get(cache_key)
    if not data:
        article = Article()
        data = article.get_data()
        cache.set(cache_key, data)
    response=render(request,'articles/article_list.html')
    patch_vary_headers(response,['Cookie'])
    return response


