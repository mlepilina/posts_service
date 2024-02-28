from django.urls import path

from posts.apps import PostsConfig

from posts.views import PostView, CommentView, PostListView, CommentListView, PostImageServiceView

app_name = PostsConfig.name

urlpatterns = [
    path('posts/', PostView.as_view(), name='post'),
    path('posts_list/', PostListView.as_view(), name='posts'),
    path('post_image/<int:pk>', PostImageServiceView.as_view(), name='post_image'),
    path('comments/', CommentView.as_view(), name='comment'),
    path('comments_list/', CommentListView.as_view(), name='comments'),
]
