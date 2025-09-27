from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from uuid import uuid4


class Category(models.Model):
    """Category model for organizing articles"""
    name = models.CharField(max_length=100, verbose_name="اسم الفئة")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="الرابط")
    description = models.TextField(blank=True, verbose_name="الوصف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "فئة"
        verbose_name_plural = "الفئات"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            if not base_slug:
                base_slug = f"category-{uuid4().hex[:8]}"
            slug_candidate = base_slug
            counter = 1
            while Category.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)


class Article(models.Model):
    """Article model for news and articles"""
    STATUS_CHOICES = [
        ('draft', 'مسودة'),
        ('published', 'منشور'),
        ('archived', 'مؤرشف'),
    ]

    title = models.CharField(max_length=200, verbose_name="العنوان")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="الرابط")
    excerpt = models.TextField(max_length=500, verbose_name="المقتطف")
    content = models.TextField(verbose_name="المحتوى")
    thumbnail = models.ImageField(
        upload_to='articles/thumbnails/',
        blank=True,
        null=True,
        verbose_name="الصورة المصغرة"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="الفئة"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="المؤلف"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="الحالة"
    )
    featured = models.BooleanField(default=False, verbose_name="مقال مميز")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    published_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="تاريخ النشر"
    )

    class Meta:
        verbose_name = "مقال"
        verbose_name_plural = "المقالات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            if not base_slug:
                base_slug = f"article-{uuid4().hex[:8]}"
            slug_candidate = base_slug
            counter = 1
            while Article.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        
        # Set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        elif self.status != 'published':
            self.published_at = None
            
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:article_detail', kwargs={'slug': self.slug})

    @property
    def is_published(self):
        return self.status == 'published'


class ArticleView(models.Model):
    """Track article views"""
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='views'
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "مشاهدة مقال"
        verbose_name_plural = "مشاهدات المقالات"
        unique_together = ['article', 'ip_address']

    def __str__(self):
        return f"مشاهدة: {self.article.title} - {self.viewed_at}"
