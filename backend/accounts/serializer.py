from rest_framework import serializers
from .models import Variable, Provincia, Municipio, Dispositivo, Usuario, RegistroVariable


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'municipio',
                  'carnet_identidad', 'phone']

    def create(self, validated_data):
        user = Usuario(**validated_data)
        user.is_active = True
        user.save()
        return user


class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = '__all__'


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = '__all__'


class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'


class DispositivoSerializer(serializers.ModelSerializer):
    variables_dict = serializers.StringRelatedField(many=True, source='variables')

    class Meta:
        model = Dispositivo
        fields = ['id', 'protocolo', 'identificador', 'variables_dict', 'descripcion', 'latitud', 'longitud']


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class RegistroVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroVariable
        fields = '__all__'
