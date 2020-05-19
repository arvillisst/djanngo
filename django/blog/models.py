from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
import unidecode  # pip install unidecode
from django.utils.text import slugify as _slugify
from django.utils import timezone
from hitcount.models import HitCountMixin
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation


def slugify(value):
    return _slugify(unidecode.unidecode(value))


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Post(models.Model, HitCountMixin):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=225, verbose_name='Название')
    slug = models.SlugField(max_length=225, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, verbose_name='Фото')
    content = RichTextUploadingField(blank=True, default='')
    # content = models.TextField(blank=True, default='')
    likes = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    dislikes = models.PositiveIntegerField(default=0, verbose_name='Диз-лайки')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='draft')
    publish = models.DateTimeField('Опубликован', default=timezone.now)
    liked = models.ManyToManyField('IpUser', blank=True, verbose_name='Понравилось')
    disliked = models.ManyToManyField('IpUser', blank=True, related_name='disliked', verbose_name='Не понравилось')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def delete(self):
        self.image.delete()
        super(Post, self).delete()

    def __str__(self):
        return 'Статья {0} из категории {1}'.format(self.title, self.category.name)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'category': self.category.slug, 'slug': self.slug})

    def get_comments_by_created(self):
        return self.comments.filter(active=True, parent__isnull=True).order_by('-created')


class Tag(models.Model):
    name = models.CharField('Заголовок', max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})


class IpUser(models.Model):
    ip_user = models.CharField('IP User', max_length=55)

    class Meta:
        verbose_name = 'IP user'
        verbose_name_plural = 'IP users'

    def __str__(self):
        return f'{self.ip_user}'