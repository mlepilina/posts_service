from datetime import datetime, date

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, Comment
from posts.paginators import paginate
from posts.serializers import PostSerializer, CommentSerializer
from posts.services import validate_user_age


class PostView(APIView):

    def post(self, request: Request):
        """Создать новый пост"""

        if validate_user_age(user=request.user):
            serializer = PostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            post = Post(
                author=request.user,
                **serializer.validated_data
            )
            post.save()

            response_data = {
                'id': post.pk,
                'title': post.title,
                'text': post.text
            }
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        return Response(
            data={'error': 'Пост можно писать только по достижению возраста 18 лет'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: Request):
        """Удалить пост"""
        post_id = request.query_params.get('post_id', 0)
        post = get_object_or_404(Post, pk=post_id)
        if post.author == request.user or request.user.is_staff is True:
            post.delete()
            return Response(data={'Пост успешно удален'}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={'error': 'Нет прав для удаления'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request):
        """Редактировать пост"""
        post_id = request.query_params.get('post_id', 0)
        post = get_object_or_404(Post, pk=post_id)
        if post.author == request.user or request.user.is_staff is True:
            serializer = PostSerializer(post, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                'id': post.pk,
                'title': post.title,
                'text': post.text
            }

            return Response(data=response_data, status=status.HTTP_200_OK)

        return Response(data={'error': 'Нет прав для редактирования'}, status=status.HTTP_400_BAD_REQUEST)


class PostListView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request: Request, *args, **kwargs):
        """Получить все посты"""
        page_number = request.query_params.get('page', 1)
        posts = Post.objects.all()
        response = paginate(
            query=PostSerializer(posts, many=True).data,
            per_page=1,
            page_number=page_number,
        )

        return Response(data=response, status=status.HTTP_200_OK)


class PostImageServiceView(APIView):

    def post(self, request: Request, pk) -> Response:
        """Загрузить изображение к посту"""

        post = get_object_or_404(Post, pk=pk)

        if post.author == request.user or request.user.is_staff is True:
            image = request.data.get('file')
            post.image.save(image.name, image, True)
            return Response(data={'Изображение к посту загружено'}, status=status.HTTP_200_OK)

        return Response(data={'error': 'Нет прав для редактирования'}, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):

    def post(self, request: Request):
        """Создать новый комментарий"""
        post_id = request.query_params.get('post_id', 0)
        post = get_object_or_404(Post, pk=post_id)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = Comment(
            author=request.user,
            **serializer.validated_data
        )
        comment.post = post
        comment.save()

        response_data = {
            'post': comment.post.title,
            'post_author': comment.post.author.email,
            'comment_text': comment.text,
            'comment_author': comment.author.email,
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def delete(self, request: Request):
        """Удалить комментарий"""
        comment_id = request.query_params.get('comment_id', 0)
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.author == request.user or request.user.is_staff is True:
            comment.delete()
            return Response(data={'Коммент успешно удален'}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={'error': 'Нет прав для удаления'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request):
        """Редактировать комментарий"""
        comment_id = request.query_params.get('comment_id', 0)
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.author == request.user or request.user.is_staff is True:
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response_data = {
                'post': comment.post.title,
                'text': comment.text,
                'author': comment.author.email,
            }

            return Response(data=response_data, status=status.HTTP_200_OK)

        return Response(data={'error': 'Нет прав для редактирования'}, status=status.HTTP_400_BAD_REQUEST)


class CommentListView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request: Request, *args, **kwargs):
        """Получить все комментарии по id поста"""
        post_id = request.query_params.get('post_id', 0)
        post = get_object_or_404(Post, pk=post_id)
        page_number = request.query_params.get('page', 1)
        comments = Comment.objects.filter(post_id=post.pk)
        response = paginate(
            query=CommentSerializer(comments, many=True).data,
            per_page=1,
            page_number=page_number,
        )

        return Response(data=response, status=status.HTTP_200_OK)
