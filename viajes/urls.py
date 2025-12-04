from django.urls import path
from . import views

app_name = 'viajes'

urlpatterns = [
    # Viajes
    path('', views.ViajeListView.as_view(), name='viaje_list'),
    path('nuevo/', views.ViajeCreateView.as_view(), name='viaje_create'),
    path('<int:pk>/', views.ViajeDetailView.as_view(), name='viaje_detail'),
    path('<int:pk>/editar/', views.ViajeUpdateView.as_view(), name='viaje_update'),
    path('<int:pk>/eliminar/', views.ViajeDeleteView.as_view(), name='viaje_delete'),
    
    # Gestión de pasajeros en viajes
    path('<int:pk>/pasajeros/', views.viaje_pasajeros_view, name='viaje_pasajeros'),
    path('<int:pk>/pasajeros/agregar/', views.agregar_pasajero_viaje, name='agregar_pasajero_viaje'),
    path('<int:pk>/pasajeros/<int:pasajero_pk>/quitar/', views.quitar_pasajero_viaje, name='quitar_pasajero_viaje'),
    path('<int:pk>/pasajeros/<int:pasajero_pk>/editar/', views.editar_pasajero_viaje, name='editar_pasajero_viaje'),
    
    # Gestión de pasajeros (CRUD)
    path('pasajeros/', views.PasajeroListView.as_view(), name='pasajero_list'),
    path('pasajeros/nuevo/', views.PasajeroCreateView.as_view(), name='pasajero_create'),
    path('pasajeros/<int:pk>/', views.PasajeroDetailView.as_view(), name='pasajero_detail'),
    path('pasajeros/<int:pk>/editar/', views.PasajeroUpdateView.as_view(), name='pasajero_update'),
    path('pasajeros/<int:pk>/eliminar/', views.PasajeroDeleteView.as_view(), name='pasajero_delete'),
]
