from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, StudentProfile, ActivityLog


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["full_name"] = user.get_full_name()
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "role", "pnfl", "phone", "avatar", "is_active",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "username", "email", "password", "first_name", "last_name",
            "role", "pnfl", "phone",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    mentor_name = serializers.CharField(source="mentor.get_full_name", read_only=True, default=None)
    tutor_name = serializers.CharField(source="tutor.get_full_name", read_only=True, default=None)

    class Meta:
        model = StudentProfile
        fields = [
            "id", "user", "student_id", "group", "course", "semester",
            "status", "grant_status", "enrollment_date",
            "mentor", "mentor_name", "tutor", "tutor_name", "parent",
        ]
        read_only_fields = ["id"]


class StudentProfileCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = StudentProfile
        fields = [
            "user", "student_id", "group", "course", "semester",
            "status", "grant_status", "enrollment_date",
            "mentor", "tutor", "parent",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["role"] = User.Role.STUDENT
        password = user_data.pop("password")
        user = User(**user_data)
        user.set_password(password)
        user.save()
        return StudentProfile.objects.create(user=user, **validated_data)


class ActivityLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    target_user_name = serializers.CharField(
        source="target_user.get_full_name", read_only=True, default=None
    )

    class Meta:
        model = ActivityLog
        fields = [
            "id", "user", "user_name", "target_user", "target_user_name",
            "action", "entity_type", "entity_id", "description",
            "metadata", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class PhoneLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone = attrs["phone"]
        password = attrs["password"]
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("Telefon raqami topilmadi")
        if not user.check_password(password):
            raise serializers.ValidationError("Parol noto'g'ri")
        if not user.is_active:
            raise serializers.ValidationError("Foydalanuvchi bloklangan")
        attrs["user"] = user
        return attrs


class PNFLSearchSerializer(serializers.Serializer):
    pnfl = serializers.CharField(max_length=14)


class ChildInfoSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "student_profile"]


class UserMeSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "role", "pnfl", "phone", "avatar",
            "student_profile", "created_at",
        ]
