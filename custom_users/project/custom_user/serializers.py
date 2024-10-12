from rest_framework import serializers # type: ignore
from django.contrib.auth.models import User, Group,Permission
from django.contrib.auth import authenticate
from .models import Customer , Company
from .services import UserService, CustomerService

from .models import Post

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
# class LoginUserSerializer(serializers.Serializer):
#     username_or_email_or_phone = serializers.CharField()
#     password = serializers.CharField()
#     user_type = serializers.CharField(read_only=True)

#     def validate(self, data):
#         username_or_email_or_phone = data.get('username_or_email_or_phone')
#         password = data.get('password')

#         # التحقق مما إذا كانت قيمة المستخدم اسم المستخدم أو بريد إلكتروني أو رقم هاتف
#         user = None
#         if '@' in username_or_email_or_phone:
#             # إذا كانت القيمة تشبه عنوان بريد إلكتروني
#             try:
#                 user = User.objects.get(email=username_or_email_or_phone)
#             except User.DoesNotExist:
#                 pass
#         elif username_or_email_or_phone.isdigit():
#             # إذا كانت القيمة تشبه رقم هاتف
#             try:
#                 customer = Customer.objects.get(phone_number=username_or_email_or_phone)
#                 user = customer.user
#             except Customer.DoesNotExist:
#                 pass
#         else:
#             # قيمة عادية لاسم المستخدم
#             user = authenticate(username=username_or_email_or_phone, password=password)

#         if user and user.is_active:
#             # التحقق مما إذا كان المستخدم لديه زبون أو شركة
#             if Customer.objects.filter(user=user).exists():
#                 user_type = 'customer'
#             elif Company.objects.filter(user=user).exists():
#                 user_type = 'company'
#             else:
#                 user_type = None
                
#             return {'user': user, 'user_type': user_type}
        
#         raise serializers.ValidationError("بيانات غير صالحة.")



#  login and remember me 
class LoginUserSerializer(serializers.Serializer):
    username_or_email_or_phone = serializers.CharField()
    password = serializers.CharField()
    remember_me = serializers.BooleanField(required=False, default=False)
    user_type = serializers.CharField(read_only=True)

    def validate(self, data):
        username_or_email_or_phone = data.get('username_or_email_or_phone')
        password = data.get('password')
        remember_me = data.get('remember_me')

        # التحقق مما إذا كانت قيمة المستخدم اسم المستخدم أو بريد إلكتروني أو رقم هاتف
        user = None
        if '@' in username_or_email_or_phone:
            # إذا كانت القيمة تشبه عنوان بريد إلكتروني
            try:
                user = User.objects.get(email=username_or_email_or_phone)
            except User.DoesNotExist:
                pass
        elif username_or_email_or_phone.isdigit():
            # إذا كانت القيمة تشبه رقم هاتف
            try:
                customer = Customer.objects.get(phone_number=username_or_email_or_phone)
                user = customer.user
            except Customer.DoesNotExist:
                pass
        else:
            # قيمة عادية لاسم المستخدم
            user = authenticate(username=username_or_email_or_phone, password=password)

        if user and user.is_active:
            # التحقق مما إذا كان المستخدم لديه زبون أو شركة
            if Customer.objects.filter(user=user).exists():
                user_type = 'customer'
            elif Company.objects.filter(user=user).exists():
                user_type = 'company'
            else:
                user_type = None

            return {'user': user, 'user_type': user_type, 'remember_me': remember_me}
        
        raise serializers.ValidationError("بيانات غير صالحة.")

# ----------------------------
# ----------------------------
# ----------------------------
# ----------------------------









class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author', write_only=True, required=False)
    author = serializers.StringRelatedField(read_only=True)  # Show username instead of user ID

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'author_id', 'created_at', 'updated_at')
 













