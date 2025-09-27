from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # Public views
    path('', views.home_view, name='home'),
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('articles/category/<slug:category_slug>/', views.ArticleListView.as_view(), name='article_list_by_category'),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    
    # API endpoints
    path('api/search/', views.api_article_search, name='article_search'),
    
    # Admin views (require login and permissions)
    path('admin/articles/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('admin/articles/<slug:slug>/edit/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('admin/articles/<slug:slug>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
]
