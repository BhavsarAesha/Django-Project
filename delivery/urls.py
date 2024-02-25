from django.urls import path
from delivery import views

urlpatterns = [
    path('index/', views.hello_django, name='index'),
    path('order/', views.order_section, name='order'),
    #path('order_details/', views.order_details, name='order_details'),
    path('register/', views.signUp, name='signUp'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout2/',views.LogoutPage,name='logout2'),
    path('profile1/', views.profile, name='profile1'),
    path('editProfile/',views.edit_profile ,name='editProfile'),
    #path('order/1/', views.order_details, name='order_details'),
    path('order/<int:customer_id>/', views.order_details, name='order_details'),
    path('mark_as_delivered/<int:customer_id>/', views.mark_as_delivered, name='mark_as_delivered'),
]