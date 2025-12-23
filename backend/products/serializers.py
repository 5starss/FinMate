from rest_framework import serializers
from .models import DepositOptions, DepositProducts, SavingOptions, SavingProducts, DepositSubscription, SavingSubscription

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
    # 중첩 Serializer를 사용하여 연결된 상품 상세 정보를 가져옵니다.
    # DepositProductSerializer는 이미 만드신 것을 사용하거나 아래처럼 정의하세요.
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = DepositSubscription
        fields = ['id', 'user', 'deposit_product', 'created_at', 'product_details']
        read_only_fields = ['user']

    def get_product_details(self, obj):
        # 가입된 예금 상품의 상세 정보를 반환
        product = obj.deposit_product
        return {
            "fin_prdt_nm": product.fin_prdt_nm,
            "kor_co_nm": product.kor_co_nm,
            # 모델에 정의된 금리나 기간 필드명을 사용하세요
            "intr_rate": getattr(product, 'intr_rate', None), 
            "save_trm": getattr(product, 'save_trm', None),
        }

# 적금 가입 정보 Serializer
class SavingSubscriptionSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = SavingSubscription
        fields = ['id', 'user', 'saving_product', 'created_at', 'product_details']
        read_only_fields = ['user']

    def get_product_details(self, obj):
        product = obj.saving_product
        return {
            "fin_prdt_nm": product.fin_prdt_nm,
            "kor_co_nm": product.kor_co_nm,
            # 모델에 정의된 금리나 기간 필드명을 사용해야함.
            "intr_rate": getattr(product, 'intr_rate', None),
            "save_trm": getattr(product, 'save_trm', None),
        }