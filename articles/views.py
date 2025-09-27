from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone
import json

from .models import Article, Category, ArticleView
from .forms import ArticleForm


class ArticleListView(ListView):
    """Display list of published articles"""
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 6
    
    def get_queryset(self):
        self.active_category = None
        queryset = Article.objects.filter(status='published').select_related('author', 'category')
        
        # Filter by category if specified
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            self.active_category = category
            queryset = queryset.filter(category=category)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        return queryset.order_by('-published_at', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            article_count=Count('article', filter=Q(article__status='published'))
        ).filter(article_count__gt=0)
        context['featured_articles'] = Article.objects.filter(
            status='published', 
            featured=True
        ).order_by('-published_at')[:3]
        context['search_query'] = self.request.GET.get('search', '')
        context['active_category'] = getattr(self, 'active_category', None)
        return context


class ArticleDetailView(DetailView):
    """Display single article"""
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
    
    def get_queryset(self):
        return Article.objects.filter(status='published').select_related('author', 'category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        
        # Track view
        self.track_view(article)
        
        # Get related articles
        context['related_articles'] = Article.objects.filter(
            status='published',
            category=article.category
        ).exclude(id=article.id).order_by('-published_at')[:3]
        
        return context
    
    def track_view(self, article):
        """Track article view"""
        ip_address = self.get_client_ip()
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        
        # Only track unique views per IP
        ArticleView.objects.get_or_create(
            article=article,
            ip_address=ip_address,
            defaults={'user_agent': user_agent}
        )
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create new article"""
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_form.html'
    permission_required = 'articles.add_article'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'تم إنشاء المقال بنجاح')
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Update existing article"""
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_form.html'
    permission_required = 'articles.change_article'
    
    def form_valid(self, form):
        messages.success(self.request, 'تم تحديث المقال بنجاح')
        return super().form_valid(form)


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete article"""
    model = Article
    template_name = 'articles/article_confirm_delete.html'
    permission_required = 'articles.delete_article'
    success_url = reverse_lazy('articles:article_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'تم حذف المقال بنجاح')
        return super().delete(request, *args, **kwargs)


def home_view(request):
    """Home page with featured articles"""
    featured_articles = Article.objects.filter(
        status='published',
        featured=True
    ).order_by('-published_at')[:6]
    
    recent_articles = Article.objects.filter(
        status='published'
    ).order_by('-published_at')[:6]
    
    context = {
        'featured_articles': featured_articles,
        'recent_articles': recent_articles,
    }
    
    return render(request, 'articles/home.html', context)


def api_article_search(request):
    """API endpoint for article search"""
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if len(query) >= 2:
            articles = Article.objects.filter(
                status='published'
            ).filter(
                Q(title__icontains=query) |
                Q(excerpt__icontains=query)
            )[:5]
            
            results = []
            for article in articles:
                results.append({
                    'title': article.title,
                    'excerpt': article.excerpt[:100] + '...',
                    'url': article.get_absolute_url(),
                    'date': article.published_at.strftime('%Y-%m-%d') if article.published_at else '',
                })
            
            return JsonResponse({'results': results})
    
    return JsonResponse({'results': []})
