from rest_framework import serializers
from .models import Group
from .models import GroupKOLAssociation


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'group_name', 'creator', 'create_time', 'update_time']
        read_only_fields = ['creator', 'create_time', 'update_time']

    def validate_group_name(self, value):
        if Group.objects.filter(group_name=value, creator=self.context['request'].user).exists():
            raise serializers.ValidationError("A group with this name already exists.")
        return value


class GroupKOLAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupKOLAssociation
        fields = ['id', 'group', 'profile', 'create_time', 'update_time']
        read_only_fields = ['create_time', 'update_time']