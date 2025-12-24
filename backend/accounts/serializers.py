from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction

User = get_user_model()

# 1. 프로필 시리얼라이저
class UserProfileSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        # 'image' 필드를 반드시 포함시켜야 합니다.
        fields = ('birth_date', 'age', 'income', 'gender', 'spending_habits', 'image')

# 2. 유저 정보 조회 및 수정 시리얼라이저
# serializers.py

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'profile', 'date_joined')
        read_only_fields = ('id', 'username', 'date_joined')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # 1. 유저 정보 수정 (nickname, email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # 2. 프로필 정보 수정
        if profile_data:
            profile = instance.profile
            profile.birth_date = profile_data.get('birth_date', profile.birth_date)
            profile.income = profile_data.get('income', profile.income)
            profile.gender = profile_data.get('gender', profile.gender)
            profile.spending_habits = profile_data.get('spending_habits', profile.spending_habits)
            
            # --- 중요: 이미지 필드 업데이트 로직 추가 ---
            # 프론트에서 보낸 'image'가 있다면 덮어쓰고, 없으면 기존 값을 유지합니다.
            if 'image' in profile_data:
                profile.image = profile_data.get('image', profile.image)
            
            profile.save()

        return instance

# 3. 회원가입 시리얼라이저
class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=30, required=True)
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=True)
    birth_date = serializers.DateField(required=True)

    # dj-rest-auth 내부 로직에 맞게 데이터 정리
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['gender'] = self.validated_data.get('gender')
        data['birth_date'] = self.validated_data.get('birth_date')
        return data

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.nickname = self.cleaned_data.get('nickname')
        user.save()

        # UserProfile 생성 시 birth_date와 income 초기값 설정
        UserProfile.objects.create(
            user=user,
            gender=self.cleaned_data.get('gender'),
            birth_date=self.cleaned_data.get('birth_date'),
            income=0 # 초기 수입 0원 세팅
        )
        return user