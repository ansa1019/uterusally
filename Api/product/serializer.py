from rest_framework import serializers
from .models import product, product_category


class productCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = product_category
        fields = '__all__'


class productSerializer(serializers.ModelSerializer):
    product_category = productCategorySerializer(read_only=True, many=True)

    class Meta:
        model = product
        fields = '__all__'






