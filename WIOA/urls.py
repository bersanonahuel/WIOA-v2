"""WIOA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path , include
from django.contrib.auth.decorators import login_required
from apps.administracion.views import Inicio
from apps.session.views import Login, logoutUsuario
# from app.registros.views import Inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(Inicio.as_view()), name = 'index'),
    path('accounts/login/', Login.as_view(), name = 'login'),
    path('logout/', login_required(logoutUsuario), name = 'logout'),
    path('administracion/',include(('apps.administracion.urls', 'administracion'))),
    path('registros/',include(('apps.registros.urls', 'registros'))),

]
