from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    # Autenticación
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Conductores
    path('conductores/', views.ConductorListView.as_view(), name='conductor_list'),
    path('conductores/nuevo/', views.ConductorCreateView.as_view(), name='conductor_create'),
    path('conductores/<int:pk>/', views.ConductorDetailView.as_view(), name='conductor_detail'),
    path('conductores/<int:pk>/editar/', views.ConductorUpdateView.as_view(), name='conductor_update'),
    path('conductores/<int:pk>/eliminar/', views.ConductorDeleteView.as_view(), name='conductor_delete'),
]
