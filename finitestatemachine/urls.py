"""finitestatemachine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from statemachine import views
from statemachine.middlewares.cant_login_after_login import cantLoginAfterLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^_nested_admin/', include('nested_admin.urls')),
    path("signup/", cantLoginAfterLogin(views.signup)),
    path("login/", cantLoginAfterLogin(views.login)),
    path("logout/", views.logout),
    path("<int:workflow_id>/start", views.workflow_start),
    path("<int:workflow_id>/submit", views.workflow_submit),
    path("", views.home),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
