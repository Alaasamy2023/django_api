# serializers.py
from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User
from .models import Customer , Company
from django.contrib.auth.models import User, Group,Permission







# ----------------------------
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)  # لتضمين أسماء المجموعات
    user_permissions = serializers.StringRelatedField(many=True)  # لتضمين أسماء الصلاحيات

    class Meta:
        model = User
        fields = ('id', 'username', 'groups', 'user_permissions')
# ----------------------------
# ----------------------------

class CreateUserSerializer(serializers.ModelSerializer):
    website = serializers.URLField(write_only=True)
    user_type = serializers.ChoiceField(choices=[('customer', 'Customer'), ('company', 'Company')])
    phone_number = serializers.CharField(max_length=20)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'website', 'user_type', 'phone_number', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("البريد الإلكتروني مستخدم بالفعل.")
        return value

    def validate_phone_number(self, value):
        if Customer.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("رقم الهاتف مستخدم بالفعل.")
        return value

    def create(self, validated_data):
        website = validated_data.pop('website')
        user_type = validated_data.pop('user_type')
        phone_number = validated_data.pop('phone_number')
        email = validated_data.pop('email')
        user = User.objects.create_user(email=email, **validated_data)

        # إضافة المستخدم إلى المجموعة
        group_name = 'customer' if user_type == 'customer' else 'company'
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            group = Group.objects.create(name=group_name)
        user.groups.add(group)

        # إضافة الصلاحيات
        permissions = Permission.objects.filter(name__startswith='Can change')
        user.user_permissions.add(*permissions)

        # إنشاء سجل Customer أو Company
        if user_type == 'customer':
            Customer.objects.create(user=user, website=website, phone_number=phone_number)
        else:
            Company.objects.create(user=user, website=website, phone_number=phone_number)

        return user

# ----------------------------
# ----------------------------








class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author_username', 'created_at', 'updated_at']
