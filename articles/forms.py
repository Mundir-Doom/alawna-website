from django import forms
from django.contrib.auth.models import User
from .models import Article, Category


class ArticleForm(forms.ModelForm):
    """Form for creating and editing articles"""
    
    class Meta:
        model = Article
        fields = [
            'title', 'excerpt', 'content', 'category', 
            'thumbnail', 'status', 'featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل عنوان المقال'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'أدخل مقتطف من المقال'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'أدخل محتوى المقال'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make sure categories are ordered by name
        self.fields['category'].queryset = Category.objects.all().order_by('name')
        
        # Add Arabic labels
        self.fields['title'].label = 'العنوان'
        self.fields['excerpt'].label = 'المقتطف'
        self.fields['content'].label = 'المحتوى'
        self.fields['category'].label = 'الفئة'
        self.fields['thumbnail'].label = 'الصورة المصغرة'
        self.fields['status'].label = 'الحالة'
        self.fields['featured'].label = 'مقال مميز'
    
    def clean_content(self):
        """Validate content field"""
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) < 50:
            raise forms.ValidationError('المحتوى يجب أن يكون أكثر من 50 حرف')
        return content
    
    def clean_excerpt(self):
        """Validate excerpt field"""
        excerpt = self.cleaned_data.get('excerpt')
        if excerpt and len(excerpt.strip()) < 20:
            raise forms.ValidationError('المقتطف يجب أن يكون أكثر من 20 حرف')
        return excerpt


class ArticleSearchForm(forms.Form):
    """Form for searching articles"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'البحث في المقالات...',
            'id': 'search-input'
        }),
        label='البحث'
    )
