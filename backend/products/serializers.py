from rest_framework import serializers
from .models import (DepositOptions, DepositProducts, 
                     SavingOptions, SavingProducts, 
                     DepositSubscription, SavingSubscription
                     )

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

# 예금 가입 정보 Serializer
class DepositSubscriptionSerializer(serializers.ModelSerializer):
    # 가입한 옵션의 상세 정보 (기간, 기본금리, 최고금리)
    option_details = serializers.SerializerMethodField()
    # 상품 정보 (은행명, 상품명, 우대조건 텍스트)
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    bank_name = serializers.CharField(source='product.kor_co_nm', read_only=True)
    special_condition = serializers.CharField(source='product.spcl_cnd', read_only=True)

    class Meta:
        model = DepositSubscription
        fields = [
            'id', 'product', 'deposit_option', 'amount',
            'bank_name', 'product_name', 'option_details', 
            'special_condition'
        ]
        read_only_fields = ['user', 'joined_at']
    
    # 금액이 0원 이하일 경우 에러 처리
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("가입 금액은 0원보다 커야 합니다.")
        return value
    
    def get_option_details(self, obj):
        option = obj.deposit_option
        if option:
            return {
                "save_trm": option.save_trm,      # 저축 기간
                "intr_rate": option.intr_rate,    # 기본 저축 금리
                "intr_rate2": option.intr_rate2,  # 최고 우대 금리
            }
        return None


# 적금 가입 정보 Serializer
class SavingSubscriptionSerializer(serializers.ModelSerializer):
    option_details = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    bank_name = serializers.CharField(source='product.kor_co_nm', read_only=True)
    special_condition = serializers.CharField(source='product.spcl_cnd', read_only=True)

    class Meta:
        model = SavingSubscription
        fields = [
            'id', 'product', 'saving_option', 'amount',
            'bank_name', 'product_name', 'option_details', 
            'special_condition'
        ]
        read_only_fields = ['user', 'joined_at']
    
    # 금액이 0원 이하일 경우 에러 처리
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("가입 금액은 0원보다 커야 합니다.")
        return value
    
    def get_option_details(self, obj):
        option = obj.saving_option
        if option:
            return {
                "save_trm": option.save_trm,      # 저축 기간
                "intr_rate": option.intr_rate,    # 기본 저축 금리
                "intr_rate2": option.intr_rate2,  # 최고 우대 금리
            }
        return None