from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import SIIDataViewSet

router = DefaultRouter()
router.register(r'', SIIDataViewSet, basename='')

urlpatterns = [
    path('', include(router.urls)),
]
