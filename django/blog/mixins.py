from django.views.generic.base import ContextMixin
from .models import Category, Post, Tag
from comments.models import Comment
from django.db.models import Count


class SidebarMixin(ContextMixin):

    def get_context_data(self, *args, **kwargs):
        context = super(SidebarMixin, self).get_context_data(**kwargs)
        context['category_from_mixin'] = Category.objects.all()

        most_viewed_posts = Post.objects.order_by('-hit_count_generic__hits')[:4]
        context['most_viewed_posts'] = most_viewed_posts.select_related('category')

        """ Сортировка по кол-ву комментариев 5, 4, 3, 2, 1 """
        most_commenting_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments').select_related('category')
        context['most_commenting_posts'] = most_commenting_posts[:4]
        
        context['all_tags'] = Tag.objects.order_by('?')[:20]

        return context


