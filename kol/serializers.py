from rest_framework import serializers
from kol.models import Profile, Post #, KolBasicData Brand, Attribute, Product


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'uid', 'username','platform', 'signature', 'enterprise', 'avataruri', 'city',
            'province', 'gender', 'followers', 'followers_growth', 'posts_per_week',
            'price_60', 'price_1_20', 'price_20_60', 'cpm', 'cpe', 'avg_plays',
            'avg_engagement', 'engagement_rate', 'avg_duration',
            'view_completion_rate', 'gmv'
        ]


class ProfileSerializerGroup(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['uid', 'username', 'avataruri']


class PostSerializer(serializers.ModelSerializer):
    uid = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = [
            'platform', 'uid', 'post_id', 'created_at_timestamp',
            'duration_sec', 'title', 'summary', 'content', 'ocr_content',
            'vid_to_text', 'cover_url', 'share_count',
            'comment_count', 'like_count', 'play_count'
        ]


class PostUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='uid.username')
    avataruri = serializers.URLField(source='uid.avataruri')

    class Meta:
        model = Post
        fields = ['platform', 'username', 'avataruri', 'post_id', 'created_at_timestamp', 'title', 'duration_sec', 'cover_url', 'share_count', 'comment_count', 'like_count', 'play_count']


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