# myapp/serializers.py

from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        help_text="Your username",
        style={'input_type': 'text'},  # This makes it a text input
    )
    password = serializers.CharField(
        required=True,
        write_only=True,  # This prevents the password from being read back
        help_text="Your password",
        style={'input_type': 'password'},  # This makes it a password input (hidden)
    )