from rest_framework import serializers
from .models import Usuario


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'provincia', 'municipio',
                  'carnet_identidad', 'phone']

    def create(self, validated_data):
        user = Usuario(**validated_data)
        user.is_active = False
        user.save()
        return user
