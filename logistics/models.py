from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model

class Driver(models.Model):
    name = models.CharField(max_length=120)
    shift_hours = models.FloatField(default=0)  # current shift hours
    past_week_hours = ArrayField(models.FloatField(), size=7)  # length 7
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Route(models.Model):
    route_id = models.IntegerField(unique=True)
    distance_km = models.FloatField()
    TRAFFIC_CHOICES = (("Low","Low"),("Medium","Medium"),("High","High"))
    traffic_level = models.CharField(max_length=10, choices=TRAFFIC_CHOICES)
    base_time_min = models.FloatField()

    def __str__(self):
        return f"Route {self.route_id}"

class Order(models.Model):
    order_id = models.IntegerField(unique=True)
    value_rs = models.FloatField()
    route = models.ForeignKey(Route, on_delete=models.PROTECT, related_name="orders")
    delivery_time = models.TimeField()  # requested delivery time (HH:MM)
    assigned_driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default="pending")  # pending/delivered/late/unassigned
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id}"

class SimulationResult(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    inputs = models.JSONField()
    results = models.JSONField()
