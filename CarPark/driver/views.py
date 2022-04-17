from typing import Dict
from datetime import datetime

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Driver
from .serializers import DriversSerializer


class DriverView(APIView):
    def get(self, request, driver_id):
        driver: Driver = get_object_or_404(Driver, pk=driver_id)
        serializer = DriversSerializer(driver, many=False)

        return Response(
            {"driver": serializer.data},
            status=status.HTTP_200_OK
        )

    def patch(self, request, driver_id):
        driver: Driver = get_object_or_404(Driver, pk=driver_id)
        serializer = DriversSerializer(
            driver,
            data=request.data,
            partial=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": "Driver updated successfully",
                    "new_driver": serializer.data
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, driver_id):
        driver: Driver = get_object_or_404(Driver, pk=driver_id)
        driver.delete()

        return Response(
            {"message": f"Driver with id `{driver_id}` has been deleted."},
            status=status.HTTP_204_NO_CONTENT
        )


class DriverListView(APIView):
    @staticmethod
    def validate_query_params(query_params: Dict) -> Dict:
        greater_than, less_than = 'created_at__gte', 'created_at__lte'

        created_gte: str = query_params.get(greater_than, None)
        created_lte: str = query_params.get(less_than, None)

        if created_gte:
            query_params[greater_than] = datetime.strptime(created_gte, '%d-%m-%Y')

        if created_lte:
            query_params[less_than] = datetime.strptime(created_lte, '%d-%m-%Y')

        return query_params

    def get(self, request):
        query_params: Dict = self.validate_query_params(request.query_params.dict())
        drivers: QuerySet = (Driver.objects.filter(**query_params)
                             if query_params else Driver.objects.all())
        serializer = DriversSerializer(drivers, many=True)

        return Response(
            {"drivers": serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = DriversSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": "Driver created successfully",
                    "driver": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
