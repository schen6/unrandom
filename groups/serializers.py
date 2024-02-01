from rest_framework import serializers
from .models import Group, GroupKOLAssociation
from kol.models import Profile
from kol.serializers import ProfileSerializerGroup


class KolAssociationSerializer(serializers.ModelSerializer):
    '''
    returns uid/user/avataruri from kol profiles
    '''
    association_id = serializers.IntegerField(source='id', read_only=True)
    uid = serializers.IntegerField(source='uid.uid')
    username = serializers.CharField(source='uid.username')
    avataruri = serializers.CharField(source='uid.avataruri')
    followers = serializers.IntegerField(source='uid.followers')
    user = serializers.IntegerField(source='group.user_id')
    class Meta:
        model = GroupKOLAssociation
        fields = ['user', 'group_id', 'association_id', 'uid', 'username', 'avataruri','followers', 'create_time', 'update_time']


class GroupKOLAssociationSerializer(serializers.ModelSerializer):
    association_id = serializers.IntegerField(source='id', read_only=True)
    # group_id = serializers.IntegerField(source='group.id')
    group_id = serializers.PrimaryKeyRelatedField(source='group', queryset=Group.objects.all())
    uid = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())

    class Meta:
        model = GroupKOLAssociation
        fields = ['association_id', 'group_id', 'uid', 'create_time', 'update_time']
        read_only_fields = ['association_id', 'group_id','create_time', 'update_time']

    def create(self, validated_data):
        # Create and return a new GroupKOLAssociation instance
        return GroupKOLAssociation.objects.create(**validated_data)


class GroupSerializer(serializers.ModelSerializer):
    group_id = serializers.IntegerField(source='id', read_only=True)
    # kol_associations = GroupKOLAssociationSerializer(many=True, read_only=True)
    kol_trunc = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['group_id', 'group_name', 'group_description', 'user', 'create_time', 'update_time', 'kol_trunc']
        read_only_fields = ['user', 'create_time', 'update_time']

    def validate_group_name(self, value):
        if Group.objects.filter(group_name=value, user=self.context['request'].user).exists():
            raise serializers.ValidationError("A group with this name already exists.")
        return value

    def get_kol_trunc(self, obj):
        # Fetch only up to 10 KOL associations for this group
        associations = obj.group_associations.all()[:5]
        return KolAssociationSerializer(associations, many=True).data

    # def get_kol_associations_full(self, obj):
    #     # Fetch all KOL associations for this group
    #     associations = obj.kol_associations.all()
    #     return KolAssociationSerializer(associations, many=True).data


