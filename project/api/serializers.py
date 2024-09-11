# serializers.py
from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User




class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author_username', 'created_at', 'updated_at']
