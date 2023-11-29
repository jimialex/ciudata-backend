from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from apps.contrib.utils.coordinates_conversor import coordinates_conversor
import pandas as pd


class ConversorApiView(APIView):
    """Class for converting coordinates in xls to GPS points"""

    def post(self, request, format=None):
        # Extract the Excel file from the request data
        excel_file = request.data['excel_file']

        # Read the Excel file using pandas
        df = pd.read_excel(excel_file)

        # Extract the latitude and longitude coordinates from the DataFrame
        coordinates = df[['POINT_X', 'POINT_Y']].values.tolist()

        # Convert the coordinates to GPS points using the specified UTM zone
        array_lat_long = coordinates_conversor(coordinates, utm_zone=19)  # utm_zone=19 es para nuestra region

        return Response(array_lat_long, status=status.HTTP_200_OK)
