import pandas as pd
from django.core.management.base import BaseCommand
from logistics.models import Driver, Route, Order
from datetime import datetime

class Command(BaseCommand):
    help = 'Seed database from Excel files'

    def handle(self, *args, **kwargs):
        # Adjust paths to your Excel files
        drivers_df = pd.read_csv('drivers.csv')
        routes_df = pd.read_csv('routes.csv')
        orders_df = pd.read_csv('orders.csv')

        # Seed Drivers
        self.stdout.write("Seeding Drivers...")
        for _, row in drivers_df.iterrows():
            past_week = [float(x) for x in str(row['past_week_hours']).split('|')]
            Driver.objects.update_or_create(
                name=row['name'],
                defaults={
                    'shift_hours': row['shift_hours'],
                    'past_week_hours': past_week
                }
            )

        # Seed Routes
        self.stdout.write("Seeding Routes...")
        for _, row in routes_df.iterrows():
            Route.objects.update_or_create(
                route_id=row['route_id'],
                defaults={
                    'distance_km': row['distance_km'],
                    'traffic_level': row['traffic_level'],
                    'base_time_min': row['base_time_min']
                }
            )

        # Seed Orders
        self.stdout.write("Seeding Orders...")
        for _, row in orders_df.iterrows():
            route = Route.objects.get(route_id=row['route_id'])
            delivery_time = datetime.strptime(row['delivery_time'], '%H:%M').time()
            Order.objects.update_or_create(
                order_id=row['order_id'],
                defaults={
                    'value_rs': row['value_rs'],
                    'route': route,
                    'delivery_time': delivery_time,
                    'assigned_driver': None,
                    'status': 'pending'
                }
            )

        self.stdout.write(self.style.SUCCESS('Database seeding completed.'))
