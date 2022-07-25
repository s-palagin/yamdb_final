import random

from rest_framework import serializers

from .models import User

CONFIRM_CODE_MIN = 1000000
CONFIRM_CODE_MAX = 9999999


def generate_confirmation_code():
    return random.randint(
        CONFIRM_CODE_MIN, CONFIRM_CODE_MAX
    )


class ConfirmationCodeGenerator:
    requires_context = False

    def __call__(self):
        return generate_confirmation_code()


class UserSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.HiddenField(
        default=ConfirmationCodeGenerator()
    )

    class Meta:
        fields = (
            'username', 'confirmation_code',
            'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                ['Using "me" as username is forbidden.']
            )
        return value


class UserMeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
