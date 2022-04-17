from typing import Dict

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from driver.models import Driver
from .models import Vehicle
from .serializers import VehicleSerializer, GetVehicleSerializer
from carpark.constants import VALID_WITH_DRIVERS_VALUES


class VehicleView(APIView):
    def get(self, request, vehicle_id):
        vehicle: Vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        serializer = GetVehicleSerializer(vehicle, many=False)

        return Response({"vehicle": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, vehicle_id):
        vehicle: Vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        driver_id: int = request.data.get('driver_id', None)

        if driver_id:
            driver: QuerySet = Driver.objects.filter(id=driver_id)

            if not driver:
                return Response(
                    {"Error": f"Driver with specified id: {driver_id} not exists"}
                )

        serializer = VehicleSerializer(
            instance=vehicle,
            data=request.data,
            partial=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": "Vehicle updated successfully",
                    "new_vehicle": serializer.data
                }
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, vehicle_id):
        vehicle: Vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        vehicle.delete()

        return Response(
            {"message": f"Vehicle with id `{vehicle_id}` has been deleted."},
            status=status.HTTP_204_NO_CONTENT
        )


class VehicleListView(APIView):
    @staticmethod
    def is_valid_with_drivers_value(value: str) -> bool:
        return value in VALID_WITH_DRIVERS_VALUES

    def get(self, request):
        query_params: Dict = request.query_params.dict()
        if not query_params:
            vehicles: QuerySet = Vehicle.objects.all()

        else:
            with_drivers: str = query_params.pop('with_drivers', 'yes').lower()

            if not self.is_valid_with_drivers_value(with_drivers):
                return Response(
                    {"invalid_with_drivers":
                     "Argument 'with_driver' must be 'yes' or 'no'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if with_drivers == 'yes':
                vehicles: QuerySet = (Vehicle.objects.
                                      filter(driver_id__isnull=False))
            elif with_drivers == 'no':
                vehicles: QuerySet = (Vehicle.objects.
                                      filter(driver_id__isnull=True))
            else:
                vehicles: QuerySet = (Vehicle.objects.
                                     filter(**query_params))

        serializer = GetVehicleSerializer(vehicles, many=True)
        return Response(
            {"vehicles": serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": "Vehicle created successfully",
                    "driver": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class VehicleSetDriverView(APIView):

    def post(self, request, vehicle_id):
        vehicle: Vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        driver_id = request.data.get('driver_id')

        if not request.data and driver_id:
            return Response(
                {"Missing values": "No values exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if vehicle.driver_id:
            request.data['driver_id'] = None
        else:
            request.data['driver_id'] = driver_id

        serializer = VehicleSerializer(
            instance=vehicle,
            data=request.data,
            partial=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": "Vehicle change driver_id successfully",
                    "driver": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )