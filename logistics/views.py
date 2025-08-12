from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Driver, Route, Order, SimulationResult
from .serializers import DriverSerializer, RouteSerializer, OrderSerializer, SimulationResultSerializer
from .utils import run_simulation
from django.shortcuts import get_object_or_404

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class RunSimulationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            available_drivers = int(data.get("available_drivers"))
            route_start_time = data.get("route_start_time")
            max_hours_per_driver = float(data.get("max_hours_per_driver"))
        except Exception as e:
            return Response({"error":"InvalidParameter","message":"Check input types","detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Validate values
        total_drivers = Driver.objects.count()
        if available_drivers < 1 or available_drivers > total_drivers:
            return Response({"error":"InvalidParameter","message":f"available_drivers must be between 1 and {total_drivers}"}, status=status.HTTP_400_BAD_REQUEST)
        if max_hours_per_driver <= 0:
            return Response({"error":"InvalidParameter","message":"max_hours_per_driver must be positive"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            results = run_simulation(available_drivers, route_start_time, max_hours_per_driver)
        except ValueError as e:
            return Response({"error":"InvalidParameter","message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # persist
        sim = SimulationResult.objects.create(inputs={"available_drivers":available_drivers,"route_start_time":route_start_time,"max_hours_per_driver":max_hours_per_driver}, results=results)
        ser = SimulationResultSerializer(sim)
        return Response(ser.data, status=status.HTTP_200_OK)
    
    def get(self, request):
        # Return list of all simulation results, ordered by creation time
        sims = SimulationResult.objects.all().order_by('timestamp')
        serializer = SimulationResultSerializer(sims, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
