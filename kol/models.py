from django.db import models

# Create your models here.


class Profile(models.Model):
    uid = models.BigIntegerField(primary_key=True)
    # douyin_sec_uid = models.CharField(null=True)
    # xintu_id = models.BigIntegerField(null=True)
    # douyin_unique_id = models.CharField(null=True, blank=True)
    username = models.CharField(max_length=500, db_index=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    platform = models.CharField(max_length=20)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    avataruri = models.URLField(max_length=500, blank=True, null=True)
    followers = models.BigIntegerField(null=True)
    signature = models.TextField(blank=True)
    enterprise = models.CharField(max_length=200, blank=True)
    post_count = models.BigIntegerField(null=True)
    # followers_growth = models.FloatField(null=True)
    # posts_per_week = models.FloatField(null=True)
    # price_60 = models.FloatField(null=True)
    # price_1_20 = models.FloatField(null=True)
    # price_20_60 = models.FloatField(null=True)
    # cpm = models.FloatField(null=True)
    # cpe = models.FloatField(null=True)
    # avg_plays = models.BigIntegerField(null=True)
    # avg_engagement = models.BigIntegerField(null=True)
    # engagement_rate = models.FloatField(null=True)
    # avg_duration = models.BigIntegerField(null=True)
    # view_completion_rate = models.FloatField(null=True)
    # gmv = models.BigIntegerField(null=True)

    def __str__(self):
        return f"{self.platform} - {self.uid}"


class Post(models.Model):
    platform = models.CharField(max_length=100)
    # uid = models.BigIntegerField()
    uid = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_uid')
    post_id = models.BigIntegerField(primary_key=True)
    created_at = models.BigIntegerField()
    created_at_timestamp = models.DateTimeField(null=True)
    duration_sec = models.IntegerField(null=True)
    title = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    ocr_content = models.TextField(null=True, blank=True)
    vid_to_text = models.TextField(null=True, blank=True)
    cover_url = models.URLField(null=True, blank=True)
    share_count = models.BigIntegerField(null=True)
    comment_count = models.BigIntegerField(null=True)
    like_count = models.BigIntegerField(null=True)
    play_count = models.BigIntegerField(null=True)
    # create_time = models.DateTimeField(auto_now_add=True)
    # update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


# class Kol(models.Model):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=500)
#
#

#
# class Brand(models.Model):
#     brand_id = models.AutoField(primary_key=True)
#     brand = models.CharField(max_length=200)
#     origin = models.CharField(max_length=200)
#     segment = models.CharField(max_length=200)
#     kw_original = models.TextField()
#     kw_formatted = models.TextField()
#
# class Attribute(models.Model):
#     attribute_id = models.AutoField(primary_key=True)
#     layer_1 = models.CharField(max_length=200)
#     layer_2 = models.CharField(max_length=200)
#     layer_3 = models.CharField(max_length=200)
#     layer_4 = models.CharField(max_length=200)
#     kw_original = models.TextField()
#     kw_formatted = models.TextField()
#
#     class Meta:
#         unique_together = (('attribute_id', 'layer_4'),)  # composite unique constraint
#
# class Product(models.Model):
#     prod_id = models.AutoField(primary_key=True)
#     hero_product = models.CharField(max_length=200)
#     brand = models.CharField(max_length=200)
#     brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', db_column='brand_id')
#     product_series = models.CharField(max_length=200)
#     kw_original = models.TextField()
#     kw_formatted = models.TextField()
