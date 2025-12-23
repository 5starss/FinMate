# accounts/serializers.py
from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('age', 'income', 'gender', 'spending_habits')
        # user 필드는 제외하거나 read_only로 설정하여 수정을 방지합니다.

class UserSerializer(serializers.ModelSerializer):
    # 유저 정보를 조회할 때 프로필도 함께 보여줍니다.
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile', 'date_joined')
        read_only_fields = ('id', 'username', 'date_joined') # 아이디나 가입일은 수정 불가

    # [중요] 중첩된 시리얼라이저의 수정을 처리하기 위한 update 로직
    def update(self, instance, validated_data):
        # 프로필 데이터 분리
        profile_data = validated_data.pop('profile', None)
        
        # 1. 기본 유저 정보 업데이트 (email 등)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 2. 프로필 정보 업데이트
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance