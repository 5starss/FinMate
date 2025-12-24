from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    # 게시판에서는 실명(ID) 대신 닉네임을 보여줍니다.
    user_nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = Comment
        fields = ('id', 'user_nickname', 'content', 'created_at', 'updated_at')
        read_only_fields = ('user', 'article')

class ArticleListSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source='user.nickname')
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'user_nickname', 'title', 'representative_category', 'total_asset_snapshot', 'like_count', 'created_at')

class ArticleSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source='user.nickname')
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'like_users', 'total_asset_snapshot', 'representative_category')