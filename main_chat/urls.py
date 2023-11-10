from django.conf import settings
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from server.views import ServerListViewSet, CategoryListViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from webchat.consumer import WebChatConsumer
from webchat.views import MessageViewSet
from account.views import AccountViewSet

# Initializing a default router
router = DefaultRouter()


# Registering view sets with the router
router.register("api/server/select", ServerListViewSet)
router.register("api/server/category", CategoryListViewSet)
router.register("api/messages", MessageViewSet, basename="message")
router.register("api/account", AccountViewSet, basename="account")

# URL patterns for the app
urlpatterns = [
    # Admin interface URL
    path("admin/", admin.site.urls),
    # API schema URL
    path("api/docs/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI URL
    path("api/docs/swagger/ui/", SpectacularSwaggerView.as_view()),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Including the router URLs
] + router.urls

# WebSocket URL patterns
websocket_urlpatterns = [
    # WebSocket consumer URL
    path("<str:serverId>/<str:channelId>", WebChatConsumer.as_asgi())
]

# Serving media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
