from django.contrib.auth.models import User, Group
from rest_framework import serializers
from sara_cmt.cluster.models import HardwareUnit, Cluster


class UserSerializer(serializers.ModelSerializer):
#class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')


class GroupSerializer(serializers.ModelSerializer):
#class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class HardwareSerializer(serializers.ModelSerializer):
#class HardwareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HardwareUnit
        fields = ('rack', 'first_slot', 'label', 'warranty_tag')


class ClusterSerializer(serializers.ModelSerializer):
#class ClusterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cluster
        fields = ('name',)
