from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

import app.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", app.views.index, name="index"),
    path("db/", app.views.db, name="db"),
    path("register/", app.views.RegisterView.as_view(), name="register"),
    path('login/', app.views.CustomLoginView.as_view(redirect_authenticated_user=True, template_name='login.html', authentication_form=app.views.LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path("about/", app.views.about, name="about"),
    path('profile', app.views.profile, name='profile'),
    path('password-change/', app.views.ChangePasswordView.as_view(), name='password_change'),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
