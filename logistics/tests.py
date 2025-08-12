from django.test import TestCase
from .utils import calc_fuel_cost, is_late, apply_fatigue_multiplier, calc_order_profit, run_simulation
from .models import Driver, Route, Order

class UtilsTest(TestCase):
    def test_calc_fuel_cost_high(self):
        cost = calc_fuel_cost(10, "High")
        self.assertEqual(cost, 10*(5+2))

    def test_is_late(self):
        self.assertFalse(is_late(120, 110))  # actual=120, base=110 -> base+10=120 -> not late
        self.assertTrue(is_late(121,110))

    def test_apply_fatigue_multiplier(self):
        d = Driver.objects.create(name="T", shift_hours=6, past_week_hours=[6,6,6,6,6,6,9])
        self.assertEqual(apply_fatigue_multiplier(d), 1.3)
        d2 = Driver.objects.create(name="U", shift_hours=6, past_week_hours=[6,6,6,6,6,6,8])
        self.assertEqual(apply_fatigue_multiplier(d2), 1.0)

    def test_order_profit_formula(self):
        profit = calc_order_profit(2000, 200, 50, 100)  # value, bonus, penalty, fuel
        self.assertEqual(profit, 2000+200-50-100)

class SimulationEndpointTest(TestCase):
    def setUp(self):
        # create drivers, routes, orders small set
        self.d1 = Driver.objects.create(name="A", shift_hours=0, past_week_hours=[7,7,7,7,7,7,7])
        self.d2 = Driver.objects.create(name="B", shift_hours=0, past_week_hours=[7,7,7,7,7,7,7])
        r = Route.objects.create(route_id=1, distance_km=10, traffic_level="Low", base_time_min=60)
        Order.objects.create(order_id=1, value_rs=500, route=r, delivery_time="01:00")
        Order.objects.create(order_id=2, value_rs=1500, route=r, delivery_time="02:00")
    def test_run_simulation_small(self):
        res = run_simulation(available_drivers=2, route_start_time="08:00", max_hours_per_driver=8)
        self.assertIn("total_profit", res)
        self.assertTrue(isinstance(res["orders"], list))

