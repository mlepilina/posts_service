from rest_framework import serializers

from posts.models import Post, Comment
from posts.validators import TitleValidator


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'change_date',
        ]

        validators = [
            TitleValidator(fields=['title']),
        ]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'text',
        ]

