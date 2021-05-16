from rest_framework import serializers
from auth_.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
                email=validated_data['email'],
                full_name=validated_data['full_name'],
                address=validated_data['address'],
                phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
