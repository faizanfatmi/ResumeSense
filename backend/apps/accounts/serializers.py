from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    display_name = serializers.CharField(max_length=100, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm',
                  'first_name', 'last_name', 'display_name')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        display_name = validated_data.pop('display_name', '')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        UserProfile.objects.create(
            user=user,
            display_name=display_name or user.get_full_name() or user.username
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for login — accepts username or email."""
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Read serializer for User data."""
    display_name = serializers.SerializerMethodField()
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'display_name', 'avatar', 'date_joined')
        read_only_fields = ('id', 'username', 'date_joined')

    def get_display_name(self, obj):
        try:
            if hasattr(obj, 'profile') and obj.profile and obj.profile.display_name:
                cleaned = obj.profile.display_name.strip()
                if cleaned:
                    return cleaned
        except Exception:
            pass

        full_name = obj.get_full_name().strip()
        if full_name:
            return full_name

        if obj.first_name and obj.first_name.strip():
            return obj.first_name.strip()

        if obj.username and obj.username.strip():
            return obj.username.strip()

        return "User"


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    display_name = serializers.CharField(max_length=100, required=False)
    avatar = serializers.ImageField(required=False)
    first_name = serializers.CharField(max_length=30, required=False, source='user.first_name')
    last_name = serializers.CharField(max_length=30, required=False, source='user.last_name')
    email = serializers.EmailField(required=False, source='user.email')

    class Meta:
        model = UserProfile
        fields = ('display_name', 'avatar', 'first_name', 'last_name', 'email')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value
