from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from articles.models import Category, Article
from django.utils import timezone
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Set up initial categories and sample articles'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial data...')

        # Create categories
        categories_data = [
            {
                'name': 'أخبار القبيلة',
                'slug': 'tribe-news',
                'description': 'أخبار ومستجدات قبيلة العلاونة'
            },
            {
                'name': 'التراث والثقافة',
                'slug': 'heritage-culture',
                'description': 'مقالات عن تراث وثقافة قبيلة العلاونة'
            },
            {
                'name': 'التعليم والتنمية',
                'slug': 'education-development',
                'description': 'مقالات عن التعليم والتنمية في القبيلة'
            },
            {
                'name': 'التكنولوجيا والتحول الرقمي',
                'slug': 'technology-digital',
                'description': 'مقالات عن التكنولوجيا والتحول الرقمي'
            },
            {
                'name': 'الفعاليات والأنشطة',
                'slug': 'events-activities',
                'description': 'فعاليات وأنشطة أبناء القبيلة'
            }
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create superuser if doesn't exist
        if not User.objects.filter(is_superuser=True).exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@alawna.com',
                password='admin123',
                first_name='مدير',
                last_name='الموقع'
            )
            self.stdout.write('Created superuser: admin/admin123')
        else:
            admin_user = User.objects.filter(is_superuser=True).first()

        # Create sample articles
        sample_articles = [
            {
                'title': 'مؤتمر قبيلة العلاونة السنوي 2025',
                'excerpt': 'يعقد الاتحاد مؤتمره السنوي لعام 2025 لمناقشة التطورات الجديدة ومشاريع التحول الرقمي المقبلة للقبيلة.',
                'content': '''<p>نحن سعداء بالإعلان عن عقد مؤتمر قبيلة العلاونة السنوي لعام 2025، والذي سيشهد نقاشات مهمة حول مستقبل القبيلة ومشاريع التحول الرقمي.</p>

<p>سيتم خلال المؤتمر مناقشة عدة محاور مهمة:</p>
<ul>
<li>مشاريع التحول الرقمي</li>
<li>توثيق التراث الثقافي</li>
<li>برامج التعليم والتنمية</li>
<li>التواصل بين أبناء القبيلة</li>
</ul>

<p>نرحب بجميع أبناء القبيلة للمشاركة في هذا الحدث المهم.</p>''',
                'category': categories[0],  # أخبار القبيلة
                'status': 'published',
                'featured': True
            },
            {
                'title': 'توثيق الحكايات الشفوية',
                'excerpt': 'مشروع جديد لجمع وتوثيق الحكايات والذكريات الشفوية من كبار السن لحفظ التراث الثقافي.',
                'content': '''<p>نطلق مشروعاً جديداً لجمع وتوثيق الحكايات الشفوية من كبار السن في قبيلة العلاونة.</p>

<p>يهدف هذا المشروع إلى:</p>
<ul>
<li>حفظ التراث الثقافي للقبيلة</li>
<li>توثيق القصص والحكايات التاريخية</li>
<li>ربط الأجيال الجديدة بتراثها</li>
</ul>

<p>نرحب بمساهماتكم في هذا المشروع المهم.</p>''',
                'category': categories[1],  # التراث والثقافة
                'status': 'published',
                'featured': False
            },
            {
                'title': 'إطلاق الخريطة التفاعلية',
                'excerpt': 'قريباً سنطلق الخريطة التفاعلية التي تُظهر توزيع أبناء القبيلة في جميع أنحاء الوطن العربي.',
                'content': '''<p>نعمل حالياً على تطوير خريطة تفاعلية تُظهر توزيع أبناء قبيلة العلاونة في مختلف الدول العربية.</p>

<p>ستتضمن الخريطة:</p>
<ul>
<li>مواقع تواجد أبناء القبيلة</li>
<li>معلومات عن كل منطقة</li>
<li>إحصائيات ديموغرافية</li>
<li>معلومات التواصل</li>
</ul>

<p>الخريطة ستكون متاحة قريباً للجميع.</p>''',
                'category': categories[3],  # التكنولوجيا والتحول الرقمي
                'status': 'published',
                'featured': False
            },
            {
                'title': 'ملتقى الشباب العلواني',
                'excerpt': 'دعوة لجميع شباب القبيلة للمشاركة في الملتقى السنوي الذي يهدف إلى تعزيز التواصل وتبادل الأفكار.',
                'content': '''<p>ندعو جميع شباب قبيلة العلاونة للمشاركة في الملتقى السنوي للشباب.</p>

<p>سيشمل الملتقى:</p>
<ul>
<li>جلسات نقاش حول قضايا الشباب</li>
<li>ورش عمل في مجالات مختلفة</li>
<li>فرص للتواصل وتبادل الأفكار</li>
<li>عروض لمشاريع شبابية</li>
</ul>

<p>ننتظر مشاركتكم المتميزة.</p>''',
                'category': categories[4],  # الفعاليات والأنشطة
                'status': 'published',
                'featured': False
            },
            {
                'title': 'برنامج المنح الدراسية',
                'excerpt': 'الإعلان عن فتح باب التقديم لبرنامج المنح الدراسية لأبناء القبيلة المتفوقين أكاديمياً.',
                'content': '''<p>نفتح باب التقديم لبرنامج المنح الدراسية لأبناء قبيلة العلاونة المتفوقين أكاديمياً.</p>

<p>شروط التقديم:</p>
<ul>
<li>أن يكون من أبناء قبيلة العلاونة</li>
<li>الحصول على معدل ممتاز في الدراسة</li>
<li>تقديم الوثائق المطلوبة</li>
<li>اجتياز المقابلة الشخصية</li>
</ul>

<p>للمزيد من التفاصيل، يرجى التواصل مع لجنة التعليم.</p>''',
                'category': categories[2],  # التعليم والتنمية
                'status': 'published',
                'featured': False
            }
        ]

        for i, article_data in enumerate(sample_articles):
            # Create unique slug for each article
            base_slug = slugify(article_data['title'])
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            article_data_copy = article_data.copy()
            article_data_copy['slug'] = slug
            
            article, created = Article.objects.get_or_create(
                slug=slug,
                defaults={
                    **article_data_copy,
                    'author': admin_user,
                    'published_at': timezone.now()
                }
            )
            if created:
                self.stdout.write(f'Created article: {article.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully set up initial data!')
        )
        self.stdout.write('\nYou can now:')
        self.stdout.write('1. Login with admin/admin123')
        self.stdout.write('2. Access Django admin at /admin/')
        self.stdout.write('3. Create and manage articles')
