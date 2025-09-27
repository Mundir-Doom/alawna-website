from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Category, ArticleView


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'article_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

    def article_count(self, obj):
        return obj.article_set.count()
    article_count.short_description = 'عدد المقالات'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'category', 'status', 
        'featured', 'published_at', 'view_count'
    ]
    list_filter = [
        'status', 'featured', 'category', 'created_at', 
        'published_at', 'author'
    ]
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('تصنيف وإعدادات', {
            'fields': ('category', 'author', 'status', 'featured')
        }),
        ('صورة المقال', {
            'fields': ('thumbnail',),
            'classes': ('collapse',)
        }),
        ('تواريخ', {
            'fields': ('published_at',),
            'classes': ('collapse',)
        }),
    )

    def view_count(self, obj):
        return obj.views.count()
    view_count.short_description = 'عدد المشاهدات'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')

    def save_model(self, request, obj, form, change):
        if not change:  # New article
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ['article', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at', 'article__category']
    search_fields = ['article__title', 'ip_address']
    date_hierarchy = 'viewed_at'
    readonly_fields = ['viewed_at']
    ordering = ['-viewed_at']
