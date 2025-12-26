from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserSerializer # 바뀐 시리얼라이저 임포트

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile_detail(request):
    """
    로그인한 사용자의 정보(User)와 프로필(Profile)을 통합 조회하거나 수정합니다.
    """
    # 1. 프로필이 없을 경우를 대비한 안전장치는 유지 (get_or_create)
    # UserSerializer가 profile 데이터를 찾을 때 에러가 나지 않도록 보장합니다.
    UserProfile.objects.get_or_create(user=request.user)
    
    # 이제 대상은 profile이 아니라 request.user입니다.
    user = request.user

    # 2. GET 요청: 유저 + 프로필 통합 정보 보여주기
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # 3. PUT 요청: 유저 정보 또는 프로필 정보 수정하기
    elif request.method == 'PUT' or request.method == 'PATCH':
        # UserSerializer의 update 메서드가 중첩된 profile 정보까지 한꺼번에 처리합니다.
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)