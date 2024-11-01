from rest_framework import serializers
from .models import Variable, Provincia, Municipio, Dispositivo, Usuario, RegistroVariable
from rest_framework import serializers
from .models import Usuario


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'municipio',
                  'carnet_identidad', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}  # La contraseña no se debe devolver en las respuestas
        }

    def create(self, validated_data):
        user = Usuario(**validated_data)
        user.set_password(validated_data['password'])  # Asegúrate de almacenar la contraseña de manera segura
        user.is_active = True
        user.save()
        return user


# serializers.py

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'



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


class RegistroVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroVariable
        fields = '__all__'
