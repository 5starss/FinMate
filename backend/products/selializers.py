from rest_framework import serializers
from .models import DepositOptions, DepositProducts, SavingOptions, SavingProducts

class DepositProductsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DepositProducts
        fields = '__all__'


class DepositOptionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd',)


class SavingProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = '__all__'


class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd',)

# 예금 상세 serializer
class DepositProductDetailSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = DepositProducts
        fields = [
            'id',
            'fin_prdt_cd',
            'dcls_month',
            'kor_co_nm',
            'fin_prdt_nm',
            'etc_note',
            'join_deny',
            'join_member',
            'join_way',
            'spcl_cnd',
            'options',
        ]

    def get_options(self, obj):
        qs = DepositOptions.objects.filter(fin_prdt_cd=obj).order_by(
            'save_trm',
            'intr_rate_type_nm'
        )
        return DepositOptionsSerializer(qs, many=True).data
# 적금 상세 serailizer
class SavingProductDetailSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = SavingProducts
        fields = [
            'id',
            'fin_prdt_cd',
            'dcls_month',
            'kor_co_nm',
            'fin_prdt_nm',
            'etc_note',
            'join_deny',
            'join_member',
            'join_way',
            'spcl_cnd',
            'options',
        ]

    def get_options(self, obj):
        qs = SavingOptions.objects.filter(fin_prdt_cd=obj).order_by(
            'save_trm',
            'intr_rate_type_nm'
        )
        return SavingOptionsSerializer(qs, many=True).data
