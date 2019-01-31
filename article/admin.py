from django.contrib import admin

from .models import Article,Comment

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display=["title","author","created_date"]
    list_display_links=["author","created_date"]
    search_fields=["title","author__username"]
    list_filter=["created_date"]

    class Meta:
        model=Article

admin.site.register(Comment)