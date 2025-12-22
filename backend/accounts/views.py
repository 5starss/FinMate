from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile_detail(request):
    """
    로그인한 사용자의 프로필을 조회하거나 수정합니다.
    """
    # 1. 현재 로그인한 유저의 프로필을 가져오거나, 없으면 생성합니다.
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # 2. GET 요청: 프로필 정보 보여주기
    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    # 3. PUT 요청: 프로필 정보 수정하기
    elif request.method == 'PUT':
        # partial=True를 넣어주면 모든 필드를 다 보내지 않고 일부만 수정할 때 에러가 나지 않습니다.
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        # 유효성 검사 실패 시 에러 메시지 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)