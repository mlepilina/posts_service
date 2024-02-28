from rest_framework import serializers

from users.models import User
from users.validators import EmailValidator, PasswordValidator, PhoneValidator


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'phone',
            'birth_date',
            'password',
        ]

        validators = [
            EmailValidator(fields=['email']),
            PasswordValidator(fields=['password']),
            PhoneValidator(fields=['phone'])
        ]
