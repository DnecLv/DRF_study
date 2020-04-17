from rest_framework import serializers
from cbvpro import models

class PagerSerialiser(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = "__all__"