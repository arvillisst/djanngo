from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View, DetailView, ListView
from hitcount.views import HitCountDetailView
from .models import Category, Post, Tag, IpUser
from .mixins import SidebarMixin
from comments.models import Comment
from comments.forms import CommentForm
from .forms import SearchForm
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User


class HomeView(SidebarMixin, ListView):
    model = Post
    template_name = 'blog/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['first_four_posts'] = Post.objects.filter(status='draft')[:4]
        # pagination
        last_posts = Post.objects.filter(status='draft')[4:]
        page = self.request.GET.get('page', 1)
        paginator = Paginator(last_posts, 8)
        try:
            context['last_posts'] = paginator.page(page)
        except PageNotAnInteger:
            context['last_posts'] = paginator.page(1)
        except EmptyPage:
            context['last_posts'] = paginator.page(paginator.num_pages)
        return context


class CategoryDetailView(SidebarMixin, DetailView):
    model = Category
    template_name = 'blog/category-detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        context['category'] = self.get_object()
        # pagination
        posts = self.get_object().post_set.all()
        page = self.request.GET.get('page', 1)
        paginator = Paginator(posts, 8)
        try:
            context['last_posts'] = paginator.page(page)
        except PageNotAnInteger:
            context['last_posts'] = paginator.page(1)
        except EmptyPage:
            context['last_posts'] = paginator.page(paginator.num_pages)
        return context


class PostDetailView(SidebarMixin, HitCountDetailView):
    template_name = 'blog/blog-detail.html'
    model = Post
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context['post'] = self.get_object()
        context['comments'] = self.get_object().comments.filter(active=True, parent__isnull=True).order_by('-created')
        context['comment_form'] = CommentForm()
        context['superuser_admin'] = 'trini' #settings.ADMINS[0][0]
        context['superuser_email'] = 'liwver@gmail.com' #settings.ADMINS[0][1]
        return context

    def post(self, request, category, slug):
        post = get_object_or_404(self.model, category__slug=category, slug=slug)
        comments = post.comments.filter(active=True, parent__isnull=True)
        comment_form = CommentForm()
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            # print('DATA SEND POST: ', comment_form)
            if comment_form.is_valid():
                parent_obj = None
                try:
                    parent_id = int(request.POST.get('parent_id'))
                except:
                    parent_id = None

                if parent_id:
                    parent_obj = Comment.objects.get(id=parent_id)

                    if parent_obj:
                        replay_comment = comment_form.save(commit=False)
                        replay_comment.parent = parent_obj
                        name_for_reply_to = request.POST.get('reply-to')
                        message_for_reply_to = request.POST.get('message-reply-to')
                        replay_comment.reply_to = name_for_reply_to
                        # replay_comment.message_reply_to = message_for_reply_to
                        replay_comment.message_reply_to = ' '.join(message_for_reply_to.split(',')[1:])
                        # print(message_for_reply_to)
                if request.user.is_superuser:
                    new_comment = comment_form.save(commit=False)
                    new_comment.post = post
                    new_comment.save()
                    return HttpResponseRedirect(post.get_absolute_url())
                
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
                return HttpResponseRedirect(post.get_absolute_url())
            else:
                comment_form = CommentForm()


def page_not_found(request, exception):
  return render(request, '404.html')

class UserReactionView(View):
    template_name = 'blog/blog-detail.html'

    def get(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        like = self.request.GET.get('like')
        dislike = self.request.GET.get('dislike')

        ipuser = self.get_client_ip(request)
        ip_user, _ = IpUser.objects.get_or_create(ip_user=ipuser)

        if like and (ip_user not in post.liked.all()):
            if ip_user in post.disliked.all():
                post.disliked.remove(ip_user)
                post.dislikes -= 1
                post.liked.add(ip_user)
                post.likes += 1
                post.save()
            else:
                post.liked.add(ip_user)
                post.likes += 1
                post.save()

        elif like and (ip_user in post.liked.all()):
            post.liked.remove(ip_user)
            post.likes -= 1
            post.save()

        if dislike and (ip_user not in post.disliked.all()):
            if ip_user in post.liked.all():
                post.liked.remove(ip_user)
                post.likes -= 1
                post.disliked.add(ip_user)
                post.dislikes += 1
                post.save()
            else:
                post.disliked.add(ip_user)
                post.dislikes += 1
                post.save()

        elif dislike and (ip_user in post.disliked.all()):
            post.disliked.remove(ip_user)
            post.dislikes -= 1
            post.save()

        data = {
            'likes': post.likes,
            'dislikes': post.dislikes,
        }
        return JsonResponse(data)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_user = request.META.get('HTTP_X_FORWARDED_FOR')
        else:
            ip_user = request.META.get('REMOTE_ADDR')
        return ip_user


class TagDetailView(SidebarMixin, DetailView):
    template_name = 'blog/tag-list.html'
    model = Tag

    def get_context_data(self, *args, **kwargs):
        context = super(TagDetailView, self).get_context_data(*args, **kwargs)
        context['tag'] = self.get_object()
        # pagination
        post = Post.objects.filter(tags__name=self.get_object().name)
        print(post)
        print(self.get_object().name)
        # posts = self.get_object().post_set.all()
        posts = post
        page = self.request.GET.get('page', 1)
        paginator = Paginator(posts, 10)
        try:
            context['last_posts'] = paginator.page(page)
        except PageNotAnInteger:
            context['last_posts'] = paginator.page(1)
        except EmptyPage:
            context['last_posts'] = paginator.page(paginator.num_pages)
        return context


class SearchView(SidebarMixin, ListView):
    model = Post
    template_name = 'blog/search-result.html'
    form = SearchForm()
    query = None

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        if 'query' in self.request.GET:
            self.form = SearchForm(self.request.GET)
            if self.form.is_valid():
                self.query = self.form.cleaned_data['query']
                context['results_count'] = self.model.objects.select_related('category').filter(
                    Q(title__icontains=self.query) | Q(content__icontains=self.query))

                results = self.model.objects.select_related('category').filter(
                    Q(title__icontains=self.query) | Q(content__icontains=self.query))
                page = self.request.GET.get('page', 1)
                paginator = Paginator(results, 6)
                try:
                    context['results'] = paginator.page(page)
                except PageNotAnInteger:
                    context['results'] = paginator.page(1)
                except EmptyPage:
                    context['results'] = paginator.page(paginator.num_pages)
                context['query'] = self.query
        return context


class ContactView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email_from_ajax')
        theme = request.GET.get('theme_from_ajax')
        message = request.GET.get('message_from_ajax')
        body = f'Пришло письмо от {email}, с темой \n"{theme}",\n с сообщением: \n"{message}"'
        send_mail(f'{theme}', f'{body}', email, ['liwver@gmail.com'], fail_silently=False)
        return JsonResponse({"ok": "ok"})


class CommentsLoadingWithAjax(View):
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(active=True, parent__isnull=True).order_by('-created')
        page = request.GET.get('page', 1)
        paginator = Paginator(comments, 5)

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            comments = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, '_parts/list_ajax_comments.html', {'comments': comments})
            
        return render(request, '_parts/list_comments.html', {'comments': comments})





def scrape_data(request):
    from .parse_data import ParseIguides
    import wget

    parse_iguides = ParseIguides()
    data = parse_iguides.get_detail_info()

    try:
        for i in data:
            print(i['title'])
            print('--------------------------------------')

            temp_post = Post()

            temp_category, _ = Category.objects.get_or_create(name=i['category'])
            temp_post.category = temp_category
            temp_post.title = i['title']
            temp_post.content = i['content']

            if not Post.objects.filter(title=i['title']).exists():
                path_to_media = settings.MEDIA_ROOT + '\images'
                print(path_to_media)
                wget.download(i['image'], path_to_media)
                temp_post.image = f'images/{i["image"].split("/")[-1]}'
                temp_post.save()

                for i in i['tags']:
                    temp_tag, _ = Tag.objects.get_or_create(name=i)
                    temp_post.tags.add(temp_tag)

                temp_post.save()

    except Exception as err:
        print(err.__class__)
        pass

    finally:
        return redirect('home')


def get_win_news(request):
    from .new_win_news import NeoWinParser
    import wget

    neowin_obj = NeoWinParser()
    data = neowin_obj.get_detail_info()

    # print(data)

    try:
        for i in data:
            print(i['title'])
            # print(i['image'])
            # print(i['category'])
            # print(i['tags'])
            print('--------------------------------------')

            temp_post = Post()

            temp_category, _ = Category.objects.get_or_create(name=i['category'])
            temp_post.category = temp_category
            temp_post.title = i['title']
            temp_post.content = i['content']

            if not Post.objects.filter(title=i['title']).exists():
                path_to_media = 'D:/NEW_20/BLOG_12_04_2020/django/media/images'
                img_downloaded = wget.download(i['image'], path_to_media)
                temp_post.image = f'images/{i["image"].split("/")[-1]}'
                temp_post.save()

                for i in i['tags']:
                    temp_tag, _ = Tag.objects.get_or_create(name=i)
                    temp_post.tags.add(temp_tag)

                temp_post.save()

    except Exception as err:
        print(err)
        pass

    finally:
        return redirect('home')



def get_verge_news(request):
    from .verge_news import VergeParser
    import wget
    new_win = VergeParser()
    # new_win.get_links()
    data = new_win.get_detail_info()
    try:
        for i in data:
            print(i['title'])
            print('--------------------------------------')

            temp_post = Post()

            temp_category, _ = Category.objects.get_or_create(name=i['category'])
            temp_post.category = temp_category
            temp_post.title = i['title']
            temp_post.content = i['content']

            if not Post.objects.filter(title=i['title']).exists():
                path_to_media = settings.MEDIA_ROOT + '\images'
                print(path_to_media)
                wget.download(i['image'], path_to_media)
                temp_post.image = f'images/{i["image"].split("/")[-1]}'
                temp_post.save()

                for i in i['tags']:
                    temp_tag, _ = Tag.objects.get_or_create(name=i)
                    temp_post.tags.add(temp_tag)

                temp_post.save()

    except Exception as err:
        print(err)
        pass

    finally:
        return redirect('home')