from django.urls import path, include
from rest_framework import routers
from .views import DriverViewSet, RouteViewSet, OrderViewSet, RunSimulationAPIView

router = routers.DefaultRouter()
router.register("drivers", DriverViewSet)
router.register("routes", RouteViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("simulations/", RunSimulationAPIView.as_view(), name="run-simulation"),
]
