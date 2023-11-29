from django.db import models

# Create your models here.

class Profile(models.Model):
    uid = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=500, db_index=True)
    gender = models.CharField(max_length=1)
    platform = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    avataruri = models.URLField(max_length=500)
    followers = models.BigIntegerField()

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
