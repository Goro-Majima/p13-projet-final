from django.conf.urls import url
from django.urls import path
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
    path('clubhomepage', views.clubhomepage, name='clubhomepage'),
    path('editpage/<member_id>', views.editpage, name='editpage'),
]