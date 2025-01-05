from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Online platform for electronics (DRF)",
        default_version="v1",
        description="Онлайн-платформа торговой сети по продаже электроники с API-интерфейсом и админ-панелью.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jedialar@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("chain/", include("chain.urls", namespace="chain")),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
