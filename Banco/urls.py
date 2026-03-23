"""
URL configuration for Banco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro_clientes/', registrar_cliente, name='registrar_clientes'),
    path('registro_cuentas/', registrar_cuenta, name='registrar_cuentas'),
    path('registro_transaccion/', registrar_transaccion, name='registrar_transaccion'),
    path('Ver_listado_clientes/', Ver_listado_clientes, name='Ver_listado_clientes'),
    path('Self_lista_cuentas/int:<dpi>', Self_lista_cuentas, name='Self_lista_cuentas'),
    path('Transacciones/int:<numero_cuenta>', Transacciones, name='Transacciones'),
    path('Historial_transacciones', Historial_transacciones, name='Historial_transacciones'),
    path('Historial_transacciones_individual/int:<numero_cuenta>', Historial_transacciones_individual, name='Historial_transacciones_individual'),
]
