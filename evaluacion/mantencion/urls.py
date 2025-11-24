from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('main/', views.main_view, name='main'),
    path('create/responsable/', views.create_responsable, name='create_responsable'),
    path('create/maquina/', views.create_maquina, name='create_maquina'),
    path('create/mantencion/', views.create_mantencion, name='create_mantencion'),
    path('delete/mantencion/<int:pk>/', views.delete_mantencion, name='delete_mantencion'),
]
