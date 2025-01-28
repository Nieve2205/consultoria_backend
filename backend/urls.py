from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from consultoria.views import (
    ServiceCategoryViewSet, 
    ServiceSubcategoryViewSet, 
    ServiceViewSet,
    BrochureViewSet,  # Nuevo
    NewsViewSet,      # Nuevo
    AdminCheckView,
    RegisterAdminView,
    OfferViewSet,
)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'service-categories', ServiceCategoryViewSet, basename='servicecategory')
router.register(r'service-subcategories', ServiceSubcategoryViewSet, basename='servicesubcategory')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'brochures', BrochureViewSet, basename='brochure')  # Nuevo
router.register(r'news', NewsViewSet, basename='news')  # Nuevo
router.register(r'offers', OfferViewSet, basename='offer')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/check-admin/', AdminCheckView.as_view(), name='check_admin'),
    path('api/register/', RegisterAdminView.as_view(), name='register_admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)