from rest_framework.routers import DefaultRouter

from chain.apps import ChainConfig
from chain.views import NetworkLinkViewSet

app_name = ChainConfig.name

router = DefaultRouter()
router.register(r"network_links", NetworkLinkViewSet, basename="network_link")

urlpatterns = router.urls
