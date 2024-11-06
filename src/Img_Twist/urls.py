"""
URL configuration for Img_Twist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include 
from django.conf import settings

# API Doc Config
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions 

schema_view = get_schema_view(
    openapi.Info(
        title="Img Twist API",
        default_version="v1",
        description="API Endpoints for Img Twist Backend",
        contact=openapi.Contact(email="connect.mahboobalam@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    
    # Admin 
    path(f"{settings.ADMIN_URL}",  admin.site.urls),
    
    # Doc 
    path("doc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc-ui"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    
    # ### API URLs 
    
    # Common App 
    path("api/v1/common/", include("core_apps.common.urls")),
    
]
