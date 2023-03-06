from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
from datetime import date


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all()), EmailValidator(message="Invalid Email")]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email', 'first_name', 'last_name', 'date_of_birth')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'date_of_birth': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if attrs['date_of_birth'].year >= date.today().year - 16:
            raise serializers.ValidationError({"date_of_birth": "You must be at least 16 years old."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
