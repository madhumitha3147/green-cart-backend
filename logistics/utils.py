# logistics/utils.py
from typing import List, Dict
from .models import Driver, Route, Order
from django.utils import timezone
import math

LATE_PENALTY = 50  # ₹50 per late order
FUEL_BASE_PER_KM = 5
FUEL_HIGH_SURCHARGE = 2

def calc_fuel_cost(distance_km: float, traffic: str) -> float:
    surcharge = FUEL_HIGH_SURCHARGE if traffic == "High" else 0
    return distance_km * (FUEL_BASE_PER_KM + surcharge)

def apply_fatigue_multiplier(driver: Driver) -> float:
    # Company rule: if driver works >8 hours in previous day => next day speed decreases by 30%
    # we check the last day in past_week_hours (assumed to be most recent).
    try:
        last_day_hours = driver.past_week_hours[-1]
    except:
        last_day_hours = 0
    if last_day_hours > 8:
        return 1.3  # increase time by 30%
    return 1.0

def is_late(actual_time_min: float, base_time_min: float) -> bool:
    return actual_time_min > (base_time_min + 10)

def calc_order_profit(value_rs: float, bonus: float, penalty: float, fuel_cost: float) -> float:
    return value_rs + bonus - penalty - fuel_cost

def run_simulation(available_drivers: int, route_start_time: str, max_hours_per_driver: float):
    """
    - available_drivers: number of drivers to use (must exist in DB)
    - route_start_time: "HH:MM" string (we do not rely on date)
    - max_hours_per_driver: in hours
    Returns dict with KPI summary and per-order breakdown.
    """
    if available_drivers <= 0:
        raise ValueError("available_drivers must be positive")
    drivers_qs = list(Driver.objects.all().order_by('shift_hours'))
    if available_drivers > len(drivers_qs):
        raise ValueError(f"available_drivers ({available_drivers}) exceeds total drivers ({len(drivers_qs)})")

    selected_drivers = drivers_qs[:available_drivers]
    # prepare driver state
    driver_states = []
    for d in selected_drivers:
        driver_states.append({
            "driver": d,
            "worked_minutes": 0.0,
            "multiplier": apply_fatigue_multiplier(d)
        })

    # fetch orders — we simulate for all orders in DB (could restrict)
    orders_qs = Order.objects.all().select_related('route').order_by('delivery_time', '-value_rs')
    results_orders = []
    driver_index = 0
    total_on_time = 0
    total_late = 0
    total_assigned = 0
    total_profit = 0.0
    total_fuel_cost = 0.0

    for order in orders_qs:
        assigned = False
        # choose a driver that has capacity
        for attempt in range(len(driver_states)):
            ds = driver_states[driver_index % len(driver_states)]
            est_deliver_minutes = order.route.base_time_min * ds["multiplier"]
            est_hours = est_deliver_minutes / 60.0
            if (ds["worked_minutes"] / 60.0) + est_hours <= max_hours_per_driver:
                # assign
                assigned = True
                ds["worked_minutes"] += est_deliver_minutes
                assigned_driver = ds["driver"]
                break
            driver_index += 1

        if not assigned:
            # No driver could take this order due to maxHours cap.
            # Mark unassigned
            results_orders.append({
                "order_id": order.order_id,
                "status": "unassigned"
            })
            continue

        # compute on-time/late
        actual_time_min = est_deliver_minutes
        late = is_late(actual_time_min, order.route.base_time_min)
        penalty = LATE_PENALTY if late else 0.0
        bonus = 0.0
        if (order.value_rs > 1000) and (not late):
            bonus = 0.10 * order.value_rs  # 10%
        fuel_cost = calc_fuel_cost(order.route.distance_km, order.route.traffic_level)
        order_profit = calc_order_profit(order.value_rs, bonus, penalty, fuel_cost)

        results_orders.append({
            "order_id": order.order_id,
            "assigned_driver": assigned_driver.name,
            "delivered_time_min": actual_time_min,
            "on_time": not late,
            "penalty": penalty,
            "bonus": bonus,
            "fuel_cost": fuel_cost,
            "order_profit": order_profit,
        })

        total_assigned += 1
        if late:
            total_late += 1
        else:
            total_on_time += 1
        total_profit += order_profit
        total_fuel_cost += fuel_cost

        driver_index += 1

    efficiency = (total_on_time / total_assigned * 100) if total_assigned > 0 else 0.0

    result_summary = {
        "total_profit": round(total_profit,2),
        "efficiency_score": round(efficiency,2),
        "on_time_deliveries": total_on_time,
        "late_deliveries": total_late,
        "unassigned_orders": [o["order_id"] for o in results_orders if o.get("status")=="unassigned"],
        "fuel_cost_total": round(total_fuel_cost,2),
        "orders": results_orders,
    }
    return result_summary
