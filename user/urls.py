from django.conf.urls import url
from django.urls import path, re_path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from user import views as user_views
from . import views # import views so we can use them in urls.


urlpatterns = [
    path('', views.homepage, name='homepage'), 
    path('menu', views.menu, name='menu'),
    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('clubdata/<club_id>', views.clubdata, name='clubdata'),
    path('editpage/<club_id>/<member_id>', views.editpage, name='editpage'),
    path('delete_member/<club_id>/<member_id>', views.delete_member, name='delete_member'),
    path('certificate_recall/<club_id>', views.certificate_recall, name='certificate_recall'),
    path('mail_sent/<club_id>', views.mail_sent, name='mail_sent'),
    path('xls_completed/<club_id>', views.xls_completed, name='xls_completed'),
    path('csv_completed/<club_id>', views.csv_completed, name='csv_completed'),
    path('password-reset',
        auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), 
            name='password_reset'),
    path('password-reset/done',
        auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), 
            name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), 
            name='password_reset_complete'),
]