from rest_framework_simplejwt import views as jwt_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_over_view, name='api_over_view'),

    path('create/account/', views.create_account, name='create_account'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
