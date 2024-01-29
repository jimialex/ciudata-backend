#!/usr/bin/env python3
from rest_framework.response import Response
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from io import BytesIO
from datetime import date
import xlwt
from datetime import datetime
from apps.contrib.api.viewsets import PermissionViewSet
from apps.ciudata.pdf_excel.excel import XLS
from apps.ciudata.pdf_excel.pdf import RoutesTraveledReport
from apps.ciudata.models import AssignedRoute
from apps.ciudata.api.v1.views.charts import DatedViewSet
from apps.ciudata.pdf_excel.serializers import RoutesTraveledSerializer
from apps.ciudata.api.v1.serializers import AssignedRouteReportSerializer


class ExportViewSet(PermissionViewSet, DatedViewSet):

    def xls_export(self, request, *args, **kwargs):
        init_date, final_date = map(lambda x: x.date(), self.get_dates())
        # cargar las asignaciones en el rango de fechas y mandar
        routes_travled = self.get_routes_travled()

        report = RoutesTraveledReport(
            'Reporte de rutas recorridas',
            init_date, final_date,
            routes_travled=AssignedRouteReportSerializer(routes_travled, many=True).data,
        )
        ser = RoutesTraveledSerializer(report)

        # Creamos el documento Excel
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename="Reporte_rutas_asignadas.xlsx"'

        file = XLS()
        file.set_response(response)
        file.set_data(ser.data)
        output = file.generate()

        return output

    """
    def pdf_export(self, request, *args, **kwargs):

        company = self.get_company()
        init_date, final_date = map(lambda x: x.date(), self.get_dates())
        transactions = self.get_transactions()
        rep = CashFlowReport(
            'Reporte flujo de efectivo general',
            init_date, final_date,
            company, transactions
        )
        ser = CashFlowSerializer(rep)

        file = PDF(orientation="P", unit="mm", format="Letter")
        file.set_data(ser.data)
        output = file.generate()
        pdfFile = BytesIO(output.encode('latin-1'))

        with open("testtest.pdf", "wb") as file:
            file.write(output.encode())

        return HttpResponse(FileWrapper(pdfFile), content_type="application/pdf")
    """
