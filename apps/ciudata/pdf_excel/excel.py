#!/usr/bin/env python3
from datetime import date
import xlwt
import xlsxwriter
from apps.ciudata.pdf_excel.serializers import IncomeSerializer, OutcomeSerializer
from apps.ciudata.models import AssignedRoute
from functools import reduce


class XLS():
    response = None
    workbook = None
    line = 0
    title_style = {
        'bold': True,
        'font_size': 20,
        'valign': 'vcenter',
    }
    subtitle_style = {
        'valign': 'vcenter',
        'bold': True
    }
    align_rigth = {
        'align': 'rigth'
    }
    align_left = {
        'align': 'left'
    }
    # font sizes

    def add_line(self, lines=1):
        self.line += lines

    def set_workbook(self):
        self.workbook = xlsxwriter.Workbook(self.response)

    def set_data(self, data):
        self.data = data

    def set_response(self, response):
        self.response = response

    data = {
        "title": "Reporte de rutas asignadas",
        "initial_date": "01/11/24",
        "final_date": "08/11/24",

        "sales_income": 2530.0,
        "collection_income": 485.0,
        "spendings": 1800.0,
        "total_utility": 1800,

        "incomes": [
            {
                "date": "11/10/21",
                "kind": "venta",
                "detail": "gaseosa",
                "client": "pepe",
                "amount": 2000.0
            },
            {
                "date": "11/10/21",
                "kind": "venta",
                "detail": "gaseosa",
                "client": "pepe",
                "amount": 2000.0
            },
            {
                "date": "11/10/21",
                "kind": "cobranza",
                "detail": "",
                "client": "juan",
                "amount": 485.0
            }
        ],

        "outcomes": [
            {
                "date": "11/10/21",
                "kind": "venta",
                "detail": "mercado",
                "category": "gastos personales",
                "provider": "ada",
                "amount": 1800.0
            },
            {
                "date": "11/10/21",
                "kind": "cobranza",
                "detail": "Luz",
                "category": "servicios básicos",
                "provider": "",
                "amount": 500.0
            }
        ]
    }

    def set_title(self, worksheet):
        worksheet.set_row(0, 50)  # Para dar una dimension a las celdas

        bold = self.workbook.add_format(self.title_style)
        worksheet.insert_image("A1", "apps/ciudata/pdf_excel/isotipo-md.png")
        worksheet.write(self.line, 1, self.data['title'], bold)

        self.add_line(lines=2)

    def write_user_data(self, worksheet):
        subtitle = self.workbook.add_format(self.subtitle_style)
        subtitle.set_font_color('#531699')
        # worksheet.set_row(0, 25)  # Para dar una dimension a las celdas

        worksheet.write(self.line, 1, "REPORTE:", subtitle)
        worksheet.write(self.line, 2, self.data["title"])
        self.add_line()

        worksheet.write(self.line, 1, "FECHA DE INICIO:", subtitle)
        worksheet.write(self.line, 2, self.data["initial_date"])
        self.add_line()

        worksheet.write(self.line, 1, "FECHA DE FIN:", subtitle)
        worksheet.write(self.line, 2, self.data["final_date"])
        self.add_line()

        worksheet.write(self.line, 1, "FECHA DE EMISIÓN:", subtitle)
        worksheet.write(self.line, 2, str(date.today().strftime("%d-%m-%Y")))

        self.add_line(lines=2)

    def write_row_incomes_header(self, array, worksheet, line):
        bold = self.workbook.add_format({'bold': 1, 'font_color': '#FF6600'})
        arr = ["A:A", "B:B", "C:C", "D:D", "E:E", "F:F", "G:G", "H:H", "I:I"]
        # Escribimos los encabezados
        for i, field in enumerate(array):
            if (i == len(array) - 1):
                worksheet.set_column(arr[i], len(field) + 5)
            elif (i == 0):
                worksheet.set_column(arr[i], len(field) + 10)
            else:
                worksheet.set_column(arr[i], len(field) + 20)
            worksheet.write(line, i, field, bold)

    def write_row_incomes(self, inc, worksheet, line):
        params = list(map(lambda x: str(x) if x is not None else "", [
                          inc['slug'],
                          inc['ciudad'],
                          inc['assigned_date'],
                          inc['user'],
                          inc['initial_date'],
                          inc['final_date'],
                          inc['total_time'],
                          inc['route']['metadata']['distance'],
                          inc['route']['slug']
                          ]))
        for j, field_data in enumerate(params):
            worksheet.write(line + 1, j, field_data)

    def generate(self):
        # Escribimos los datos en el documento Excel
        self.set_workbook()
        worksheet = self.workbook.add_worksheet()
        self.set_title(worksheet)

        subtitle = self.workbook.add_format(self.subtitle_style)
        subtitle.set_font_color('#531699')

        self.write_user_data(worksheet)
        # self.write_totales(worksheet)

        # Escribimos los Incomes
        worksheet.write(self.line, 0,
                        "RUTAS COMPLETADAS", subtitle)
        self.add_line()

        header_title = ["Código", "Ciudad", "Fecha asignado", "Driver",
                        "Hora inicio", "Hora final", "Tiempo recorrido",
                        "Longitud de ruta", "código de ruta"]

        self.write_row_incomes_header(header_title, worksheet, self.line)

        for i, inc in enumerate(self.data["routes_travled"]):
            self.write_row_incomes(inc, worksheet, i + self.line)


        self.add_line()

        self.workbook.close()
        return self.response
