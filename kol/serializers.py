from rest_framework import serializers
from kol.models import Profile #, KolBasicData Brand, Attribute, Product


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['uid', 'username', 'gender', 'platform', 'city', 'province', 'avataruri', 'followers']

class AutocompleteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('uid', 'username')

# class KolSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Kol
#         fields = ['id', 'username']
#
#
#
# class BrandSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Brand
#         fields = ['brand_id', 'brand', 'origin', 'segment', 'kw_original', 'kw_formatted']
#
# class AttributeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Attribute
#         fields = ['attribute_id', 'layer_1', 'layer_2', 'layer_3', 'layer_4', 'kw_original', 'kw_formatted']
#
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['brand_id', 'brand', 'prod_id', 'hero_product', 'product_series', 'kw_original', 'kw_formatted']