from django.urls import include, path


from . import generatecode

app_name='api'





urlpatterns = [
 
    # Ex 3: For generate_code_view function-based view
    path('generate-code/', generatecode.generate_code_view, name='generate_code'),

    # Ex 4: For GenerateCodeView_cbv class-based view
    path('generate-code-cbv/', generatecode.GenerateCodeView_cbv.as_view(), name='generate_code_cbv'),


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

