from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # name = serializers.CharField(max_length=80)
        # body = serializers.CharField(max_length=80)
        fields = (
            'id',
            'post',
            'name',
            'body',
        )
