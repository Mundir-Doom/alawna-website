from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm


class CustomLoginView(LoginView):
    """Custom login view with Arabic support"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('articles:article_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'تم تسجيل الدخول بنجاح')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'خطأ في اسم المستخدم أو كلمة المرور')
        return super().form_invalid(form)


def custom_logout_view(request):
    """Log the user out and redirect home"""
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    return redirect('articles:home')


class SignUpView(CreateView):
    """User registration view"""
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'تم إنشاء الحساب بنجاح. يمكنك الآن تسجيل الدخول')
        return super().form_valid(form)


@login_required
def profile_view(request):
    """User profile view"""
    user = request.user
    articles = user.article_set.filter(status='published').order_by('-created_at')[:10]
    
    context = {
        'user': user,
        'articles': articles,
        'total_articles': user.article_set.count(),
        'published_articles': user.article_set.filter(status='published').count(),
    }
    
    return render(request, 'accounts/profile.html', context)
