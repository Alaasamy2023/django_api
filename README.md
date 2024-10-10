
python3 -m venv env

env\Scripts\activate.bat
source env/bin/activate
env\Scripts\activate
cd project

# 01_cereat_project_and_api_app

01- py -m venv env

02- django-admin startproject project

03- cd project

04- python manage.py runserver

05- python manage.py startapp api


06- 

إضافة التطبيق إلى إعدادات المشروع



INSTALLED_APPS = [
    # التطبيقات الافتراضية
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # التطبيقات المضافة
    'myapp',
]





07- python manage.py runserver





# 02_createsuperuser

1- python manage.py migrate

2- python manage.py createsuperuser

admin - admin 

3- python manage.py runserver



# 03 install Django REST Framework & knox

1- pip install djangorestframework

2- pip install django-rest-knox


3-
INSTALLED_APPS = [
    ...
    'rest_framework',
    'knox',
    ...
]


4- 

REST_FRAMEWORK = {
 
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
    
    ],

}







# 04 add urls in api app 

1- in project 

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('api.urls',)),

]



2- in api app 
  create urls.py 






# 05 add generatecode 
1- creat generatecode.py
2- edit urls.py in api app 
    add url 

هنا استخدمت ال 
function b v 
class b v 
باستخدام ال
api 


# 05 create Customer & company models 
1- add  Customer & company in  models
2-  add Customer & company in  admin.py

3- python manage.py makemigrations
4- python manage.py migrate


هكذا قمنا بانشاء نوعين اخرين من المستخدمين زبون وشركه ومربوط بجدول اليوزر 

# 06 create Post & Permission models 

1- add Post & Permission models
2-  add Post & Permission in  admin.py


3- python manage.py makemigrations
4- python manage.py migrate

قمنا بانشاء جدول صلاحيات وجدول للمنشورات 





# 07 show all post api 



هذا الكود قمنا بعرض كل المنشورات لكل اليوزر بدون اى فلتر مع اظهار اسم المستخدم على كل منشور 




# 08 show  post  detales in one post   api 



عند زيارة مسار URL مثل /posts/1/، سيتم استرجاع تفاصيل المنشور الذي يحمل pk=1 بتنسيق JSON. على سبيل المثال:


# 09 اضافه وتسجيل يوزر جديد فى السيستم واضافه جروبات وصلاحيات وربطه بجدول الخاص به اوتوماتك مع اعاده كل بياناته مع التوكين وعمل تشك على  رقم الهاتف و الايميل ان لايكونو متكررين 










# 010  حذف post  من السيستم 


يجب اضافه ف urls 
    path('posts/<int:pk>/delete/', views.PostDeleteAPIView.as_view(), name='post_delete'),  # URL لحذف المنشور



فقط التوجه لل view 

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



# 011 لعرض كل البوست عموما 
يجب اضافه ف urls 
    path('posts/all/', views.PostListAPIView.as_view(), name='post_list'),  # URL لعرض جميع المنشورات



فقط التوجه لل view 



# ----------------------------
# لعرض كل البوست 

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

























