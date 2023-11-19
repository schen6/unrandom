from rest_framework import serializers
from kol.models import Brand, Attribute, Product #Kol, KolBasicData


# class KolSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Kol
#         fields = ['id', 'username']
#
#
# class KolBasicDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KolBasicData
#         fields = ['id', 'username', 'platform', 'followers', 'desc', 'avatarurl']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_id', 'brand', 'origin', 'segment', 'kw_original', 'kw_formatted']

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['attribute_id', 'layer_1', 'layer_2', 'layer_3', 'layer_4', 'kw_original', 'kw_formatted']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['brand_id', 'brand', 'prod_id', 'hero_product', 'product_series', 'kw_original', 'kw_formatted']