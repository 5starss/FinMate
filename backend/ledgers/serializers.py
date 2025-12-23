from rest_framework import serializers
from .models import Category, Transaction, Budget

# ledgers/serializers.py 예시
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('user',) # 유저는 요청 데이터가 아닌 서버에서 자동 할당함

class TransactionSerializer(serializers.ModelSerializer):
    # 조회 시 카테고리 이름을 함께 보여주기 위함
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_type = serializers.CharField(source='category.type', read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('user',) # 유저는 요청 시 자동으로 할당하므로 읽기전용

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ('user',)