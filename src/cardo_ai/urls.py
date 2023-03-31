"""cardo_ai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from cash_flow.views import CashFlowViewSet
from data_upload.views import DataUploadView
from loan.views import LoanViewSet
from statistic.views import StatisticViewSet
from user.views import UserViewSet

router = DefaultRouter()
list_routes: list[tuple[str, type[ModelViewSet]]] = [
    (r'users', UserViewSet),
    (r'loans', LoanViewSet),
    (r'cash_flows', CashFlowViewSet),
    (r'statistics', StatisticViewSet)
]

for prefix, view_set in list_routes:
    router.register(prefix, view_set, basename='api')

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='swagger-ui', permanent=False)),
    path('api/v1/', include(router.urls), name='api'),
    path('api/v1/data_upload/', DataUploadView.as_view({
                                                           'post': 'post'}), name='data_upload'),
    path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),
]
