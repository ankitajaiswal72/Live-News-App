from django.shortcuts import render , redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
from .models import Article, Vote
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def feed(request):
    articles = Article.objects.all().order_by('-published_at')
    return render(request, 'feed.html', {'articles': articles})

@login_required
def post_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('feed')
    else:
        form = ArticleForm()
    return render(request, 'post_article.html', {'form': form})

# @login_required
# def vote_article(request):
#     if request.method == 'POST':
#         article_id = request.POST.get('article_id')
#         is_upvote = request.POST.get('is_upvote') == 'true'
        
#         article = Article.objects.get(id=article_id)
#         vote, created = Vote.objects.get_or_create(user=request.user, article=article)
        
#         if not created:
#             if vote.is_upvote == is_upvote:
#                 return JsonResponse({'success': False, 'message': 'You have already voted this way.'})
#             else:
#                 if vote.is_upvote:
#                     article.upvotes -= 1
#                     article.downvotes += 1
#                 else:
#                     article.upvotes += 1
#                     article.downvotes -= 1
#                 vote.is_upvote = is_upvote
#                 vote.save()
#                 article.save()
#         else:
#             if is_upvote:
#                 article.upvotes += 1
#             else:
#                 article.downvotes += 1
#             vote.is_upvote = is_upvote
#             vote.save()
#             article.save()
        
#         return JsonResponse({'success': True, 'upvotes': article.upvotes, 'downvotes': article.downvotes})

@login_required
def vote_article(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        is_upvote = request.POST.get('is_upvote') == 'true'
        article = get_object_or_404(Article, id=article_id)
        
        vote, created = Vote.objects.get_or_create(article=article, user=request.user)
        vote.is_upvote = is_upvote
        vote.save()
        
        response_data = {
            'article_id': article_id,
            'is_upvote': is_upvote,
        }
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)


temp_img = "https://images.pexels.com/photos/3225524/pexels-photo-3225524.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500"

def home(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)

    if search is None or search == "top":
        url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format("us", 1, settings.APIKEY)
    else:
        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(search, "popularity", page, settings.APIKEY)
    r = requests.get(url=url)

    data = r.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]
    context = {
        "success": True,
        "data": [],
        "search": search
    }
    for i in data:
        context["data"].append({
            "title": i["title"],
            "description": "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
            "publishedat": i["publishedAt"]
        })
    return render(request, 'index.html', context=context)

def loadcontent(request):
    try:
        page = request.GET.get('page', 1)
        search = request.GET.get('search', None)
        if search is None or search == "top":
            url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format("us", page, settings.APIKEY)
        else:
            url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(search, "popularity", page, settings.APIKEY)
        r = requests.get(url=url)

        data = r.json()
        if data["status"] != "ok":
            return JsonResponse({"success": False})
        data = data["articles"]
        context = {
            "success": True,
            "data": [],
            "search": search
        }
        for i in data:
            context["data"].append({
                "title": i["title"],
                "description": "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                "publishedat": i["publishedAt"]
            })
        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({"success": False})

def map_view(request):
    return render(request, 'map.html')

def news_by_country(request):
    country = request.GET.get('country', 'us')
    language = request.GET.get('language', 'en')
    url = "https://newsapi.org/v2/top-headlines?country={}&language={}&apiKey={}".format(country, language, settings.APIKEY)
    r = requests.get(url=url)

    data = r.json()
    if data["status"] != "ok":
        return JsonResponse({"success": False})
    data = data["articles"]
    context = {
        "success": True,
        "data": [],
    }
    for i in data:
        context["data"].append({
            "title": i["title"],
            "description": "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
            "publishedat": i["publishedAt"]
        })
    return JsonResponse(context)
