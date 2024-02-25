from django.urls import path
from app import views 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm,MySetPasswordForm
from .views import SearchResultsView


# from django.conf import settings

urlpatterns = [
    # path('', views.home),
     path('',views.ProductView.as_view(),name="home"),
     path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
     path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
     path('cart/',views.show_cart,name='showcart'),
     path('category/',views.category,name='category'),

     path('pluscart/',views.plus_cart),
     path('minuscart/',views.minus_cart),
     path('removecart/',views.remove_cart),

     path('plussize/',views.plus_size),
     path('minussize/',views.minus_size),

     path("search/", SearchResultsView.as_view(), name="search_results"),

     path('buy/', views.buy_now, name='buy-now'),
     path('profile/', views.ProfileView.as_view(), name='profile'),
     path('address/', views.address, name='address'),
     path('orders/', views.orders, name='orders'),
     path('men/', views.men, name='men'),
     path('men/<slug:data>', views.men, name='mendata'),
     path('women/', views.women, name='women'),
     path('women/<slug:data>', views.women, name='womendata'),
     path('kid/', views.kid, name='kid'),
     path('kid/<slug:data>', views.kid, name='kiddata'),

     path('checkout/', views.checkout, name='checkout'),
     path('paymentnew/', views.payment, name='payment'),

     path('paymentdone/', views.payment_done, name='paymentdone'),

     path('contactus/',views.contactus,name='contactus'),
     path('aboutus/',views.aboutus,name='aboutus'),

     #authentication
     path('accounts/login/', auth_views.LoginView.as_view
         (template_name='app/login.html', authentication_form=LoginForm), name='login'),

     path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),

     path('passwordchange/',auth_views.PasswordChangeView.as_view
         (template_name='app/passwordchange.html',form_class=MyPasswordChangeForm, 
          success_url='/passwordchangedone/'),name='passwordchange'),

     path('passwordchangedone/', auth_views.PasswordChangeView.as_view
          (template_name='app/passwordchangedone.html'),name='passwordchangedone'),

     path('password-reset/',auth_views.PasswordResetView.as_view
          (template_name='app/password_reset.html',
          form_class=MyPasswordResetForm),name='password_reset'),

     path('password-reset/done/',auth_views.PasswordResetDoneView.as_view
          (template_name='app/password_reset_done.html'),
         name='password_reset_done'),

     path('password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view
          (template_name='app/password_reset_Confirm.html',
         form_class=MySetPasswordForm),name='password_reset_confirm'),

     path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view
          (template_name='app/password_reset_complete.html'),
         name='password_reset_complete'),

     path('registration/',views.CustomerRegistrationView.as_view(), name="customerregistration"),

     #path('dwld_pdf/',views.down_pdf,name="dwld_pdf"),
     #path('download_pdf',views.dwnld_pdf,name='download_pdf'),
     path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



