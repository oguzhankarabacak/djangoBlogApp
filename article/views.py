from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm
from django.contrib import messages
from .models import Article,Comment
from django.contrib.auth.decorators import login_required

def articles(request):
    keyword=request.GET.get("keyword")
    if keyword:
        articles=Article.objects.filter(title__contains=keyword )
        content={"articles":articles}
        return render(request,"articles.html",content)
    articles=Article.objects.all()
    content={"articles":articles}
    return render(request,"articles.html",content)

def index(request):
    

    return render(request,"index.html")


def about(request):

    return render(request,"about.html")    


def detail(request,id):

    article=get_object_or_404(Article,id=id)
    comments=article.comments.all()
    content = {
        "article":article,
        "comments":comments
    }
    return render(request,"detail.html",content)

        
@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    content={
       "articles":articles
    }
    

    return render(request,"dashboard.html",content)
@login_required(login_url="user:login")
def addArticle(request):

    form=ArticleForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        article=form.save(commit=False)
        article.author=request.user
        article.save()
        messages.success(request,"Makale Başarıyla Oluşturuldu")
        return redirect("index")


    context={
        "form":form
    }    
    return render(request,"addarticle.html",context)
@login_required(login_url="user:login")
def updateArticle(request,id):

    article=get_object_or_404(Article,id=id)
    form=ArticleForm(request.POST or None,request.FILES or None,instance=article)
    if form.is_valid():
        article=form.save(commit=False)
        article.author=request.user
        article.save()
        messages.success(request,"Makale Başarıyla Güncellendi")
        return redirect("article:dashboard")

    context={
        "form":form
    }    
    return render(request,"update.html",context)    

@login_required(login_url="user:login")
def deleteArticle(request,id):

    article=get_object_or_404(Article,id=id,author=request.user)
    article.delete()
    messages.success(request,"Makale Başarıyla Silindi")
    return redirect("article:dashboard")

def addComment(request,id):
    article=get_object_or_404(Article,id=id)
    if request.method=="POST":
        comment_author=request.POST.get("comment_author")
        comment_content=request.POST.get("comment_content")
        newComment=Comment(comment_author=comment_author,comment_content=comment_content)
        newComment.article=article
        newComment.save()

    return redirect(reverse("article:detail",kwargs={"id":id}))    
    
    



    

