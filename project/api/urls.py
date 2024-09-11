from django.urls import include, path

from . import generatecode
from . import views
# from rest_framework.authtoken import views as authTokenVeiw
from knox import views as knox_views # type: ignore
from .views import PostViewSet

app_name='api'


# post_list = PostViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })

# post_detail = PostViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })



urlpatterns = [
 
    # # Ex 3: For generate_code_view function-based view
    # path('generate-code/', generatecode.generate_code_view, name='generate_code'),

    # # Ex 4: For GenerateCodeView_cbv class-based view
    # path('generate-code-cbv/', generatecode.GenerateCodeView_cbv.as_view(), name='generate_code_cbv'),

    # # Ex 5: For RegistrationAPI APIView
    # path('register/', views.RegistrationAPI.as_view(), name='register'),

    # # Ex 6: For LoginAPI APIView
    # path('login/', views.LoginAPI.as_view(), name='login'),

    # # Ex 7: For UserAPI APIView
    # path('user/', views.UserAPI.as_view(), name='user'),

    # # Ex 8: For UpdateUserAPI APIView
    # path('update-user/<int:pk>/', views.UpdateUserAPI.as_view(), name='update_user'),

    # # Ex 9: For CheckEmailAPI APIView
    # path('check-email/<str:email>/', views.CheckEmailAPI.as_view(), name='check_email'),

    # # Ex 10: For CheckPhoneNumberAPI APIView
    # path('check-phone/<str:phone_number>/', views.CheckPhoneNumberAPI.as_view(), name='check_phone'),
    
    # # Ex 11: For LogoutView provided by knox
    # path('logout/', knox_views.LogoutView.as_view(), name='logout'),





#  post


    # path('posts/', post_list, name='post-list'),
    # path('posts/<int:pk>/', post_detail, name='post-detail'),
    # path('posts/<int:pk>/delete/', views.PostDeleteAPIView.as_view(), name='post_delete'),  # URL لحذف المنشور
    # path('posts/create/', views.PostCreateAPIView.as_view(), name='post_create'),  # URL لإنشاء منشور جديد
    # path('posts/<int:pk>/update/', views.PostUpdateAPIView.as_view(), name='post_update'),  # URL لتحديث المنشور
    # path('posts/all/', views.PostListAPIView.as_view(), name='post_list'),  # URL لعرض جميع المنشورات
    # path('posts/all/alaa/', views.AlaaPostsAPIView.as_view(), name='alaa_posts'),  # URL لعرض منشورات Alaa





]































# urlpatterns = [

# # 3-    do it 
#      path('custom_user/my_view', views.my_view, name='my_view'),

   
   
# #    8-     do it 
#     path('custom_user/my_view_cbv', views.MyView_cbv.as_view(), name='my_view'),


# # rundom value  function & class    2       do it 

#     path('generate-code/', views.generate_code_view, name='generate_code'),

#     path('generate-code_cbv/', views.GenerateCodeView_cbv.as_view(), name='generate_code_cbv'),











# # 

#     #  path('chick_group/', views.chick_group, name='chick_group'),










# # token & api 



#     path('register/', views.RegistrationAPI.as_view()),
#     path('login/', views.LoginAPI.as_view()),
#     path('user/', views.UserAPI.as_view()),
#     path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
#     path('aupdate/<int:pk>/', views.UpdateUserAPI.as_view(), name='update_user'),





# # 

#     path('check-email/<str:email>/', views.CheckEmailAPI.as_view(), name='check_email'),
#     path('check-phone/<str:phone_number>/', views.CheckPhoneNumberAPI.as_view(), name='check_phone_number'),


 

# ]

