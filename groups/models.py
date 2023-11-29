from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from kol.models import Profile


class Group(models.Model):
    group_name = models.CharField(max_length=255)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_groups'
    )
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('group_name', 'creator')

class GroupKOLAssociation(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='kol_associations')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='group_associations')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('group', 'profile')
