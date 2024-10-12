import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.models import User, Group 
from django.contrib.auth.hashers import make_password
from rest_framework import status # type: ignore
from .models import Customer
from .services import UserService, CustomerService
from rest_framework import viewsets, permissions, generics # type: ignore
from rest_framework.response import Response # type: ignore
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer
from rest_framework.views import APIView # type: ignore

from knox.models import AuthToken # type: ignore

from knox.settings import CONSTANTS  # type: ignore # تحقق من أن هذه الاستيراد صحيح



from .models import Post, Company
from .serializers import PostSerializer
from custom_user import serializers




# RegistrationAPI return all data
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


 

# class LoginAPI(generics.GenericAPIView):
#     serializer_class = LoginUserSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user_data = serializer.validated_data
#         user = user_data['user']
#         user_type = user_data.get('user_type')  # احصل على نوع المستخدم

#         # استرداد الصلاحيات والمعلومات الأخرى عبر السيريالايزر
#         user_serializer = UserSerializer(user, context=self.get_serializer_context())
#         user_data_with_permissions = user_serializer.data

#         return Response({
#             "user": user_data_with_permissions,
#             "token": AuthToken.objects.create(user)[1],
#             "user_type": user_type  # أرجع نوع المستخدم أيضًا
#         }, status=status.HTTP_200_OK)






# login and remember me

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        user = user_data['user']
        user_type = user_data.get('user_type')  # احصل على نوع المستخدم
        remember_me = user_data.get('remember_me', False)  # احصل على قيمة تذكرني

        # استرداد الصلاحيات والمعلومات الأخرى عبر السيريالايزر
        user_serializer = UserSerializer(user, context=self.get_serializer_context())
        user_data_with_permissions = user_serializer.data

        # إعداد عمر رمز المصادقة بناءً على قيمة تذكرني
        if remember_me:
            expiry = datetime.timedelta(days=30)
        else:
            expiry = CONSTANTS.TOKEN_TTL

        # إنشاء رمز المصادقة
        token = AuthToken.objects.create(user, expiry=expiry)[1]

        return Response({
            "user": user_data_with_permissions,
            "token": token,
            "user_type": user_type  # أرجع نوع المستخدم أيضًا
        }, status=status.HTTP_200_OK)










 


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UpdateUserAPI(generics.UpdateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all() # type: ignore

    def get_object(self):
        user_id = self.kwargs['pk']
        return self.get_queryset().get(pk=user_id)

    def perform_update(self, serializer):
        serializer.save()
 
class CheckEmailAPI(APIView):
    def get(self, request, email):
        if User.objects.filter(email=email).exists():
            return Response({"message": "البريد الإلكتروني {} موجود بالفعل.".format(email)}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "البريد الإلكتروني {} غير موجود.".format(email)}, status=status.HTTP_200_OK)
        
class CheckPhoneNumberAPI(APIView):
    def get(self, request, phone_number):
        if Customer.objects.filter(phone_number=phone_number).exists():
            return Response({"message": "رقم الهاتف {} موجود بالفعل.".format(phone_number)}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "رقم الهاتف {} غير موجود.".format(phone_number)}, status=status.HTTP_200_OK)
        








# ----------------------------
# ----------------------------
# ----------------------------
# ----------------------------



# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         user = self.request.user
#         if Company.objects.filter(user=user).exists():
#             serializer.save(author=user)
#         else:
#             return Response({"error": "You must be a company to create a post."}, status=status.HTTP_403_FORBIDDEN)


# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         user = self.request.user
#         if Company.objects.filter(user=user).exists():
#             # Pass author_id explicitly
#             serializer.save(author=user, author_id=user.id)
#         else:
#             return Response({"error": "You must be a company to create a post."}, status=status.HTTP_403_FORBIDDEN)



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        author_id = self.request.data.get('author_id')
        user = self.request.user
        
        if author_id:
            try:
                author = User.objects.get(id=author_id)
            except User.DoesNotExist:
                return Response({"error": "Invalid author ID provided."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            author = user if user.is_authenticated else None

        if author:
            serializer.save(author=author, author_id=author.id)
        else:
            return Response({"error": "You must provide a valid author ID or be authenticated to create a post."}, status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        author_id = self.request.data.get('author_id')
        user = self.request.user
        instance = serializer.instance

        if author_id:
            try:
                author = User.objects.get(id=author_id)
            except User.DoesNotExist:
                return Response({"error": "Invalid author ID provided."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            author = instance.author  # Keep the current author if no new one is specified

        if author:
            serializer.save(author=author, author_id=author.id)
        else:
            return Response({"error": "You must provide a valid author ID to update the post."}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.delete()






# ----------------------------
# لعرض كل البوست 

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# ----------------------------
# لعرض كل البوست الخاصه بعلاء

class AlaaPostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author__username='alaa')

# ----------------------------
# الحذف فقط 

class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]  # تحديد صلاحيات الوصول
    # لا تحتاج لدالة destroy() إلا إذا كنت بحاجة لتخصيص سلوك الحذف
    # يمكنك تعيين أي سلوك إضافي لعملية الحذف هنا

# ----------------------------
# ----------------------------
# ----------------------------
#  الاضافه فقط 

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]  # تحديد صلاحيات الوصول

    def perform_create(self, serializer):
        author_id = self.request.data.get('author_id')
        user = self.request.user
        
        if author_id:
            try:
                author = User.objects.get(id=author_id)
            except User.DoesNotExist:
                return Response({"error": "Invalid author ID provided."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            author = user if user.is_authenticated else None

        if author:
            serializer.save(author=author, author_id=author.id)
        else:
            return Response({"error": "You must provide a valid author ID or be authenticated to create a post."}, status=status.HTTP_403_FORBIDDEN)

# ----------------------------
# ----------------------------
# ----------------------------
# عمليه update 
class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]  # تحديد صلاحيات الوصول

    def perform_update(self, serializer):
        author_id = self.request.data.get('author_id')
        user = self.request.user
        instance = serializer.instance

        if author_id:
            try:
                author = User.objects.get(id=author_id)
            except User.DoesNotExist:
                return Response({"error": "Invalid author ID provided."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            author = instance.author  # Keep the current author if no new one is specified

        if author:
            serializer.save(author=author, author_id=author.id)
        else:
            return Response({"error": "You must provide a valid author ID to update the post."}, status=status.HTTP_400_BAD_REQUEST)

















