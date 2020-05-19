from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('comments-loading-ajax/', views.CommentsLoadingWithAjax.as_view(), name='comments_loading_with_ajax'),
    path('user-reaction/', views.UserReactionView.as_view(), name='user_reaction'),
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('contact/', views.ContactView.as_view(), name='contact'),

    path('<slug:category>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    path('scrape/', views.scrape_data, name='scrape'),
    path('new-win/', views.get_win_news, name='neo_win'),
    path('verge_news/', views.get_verge_news, name='verge_news'),
]