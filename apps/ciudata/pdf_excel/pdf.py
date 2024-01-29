#!/usr/bin/env python3
from datetime import date
# from fpdf import FPDF
# from apps.companies.pdf_excel.serializers import IncomeSerializer, OutcomeSerializer
# from apps.companies.models import Transaction
from functools import reduce
from apps.ciudata.models import AssignedRoute, Route


class FileReport:

    def __init__(self, title, initial_date, final_date, routes_travled):
        self.title = title
        self.initial_date = initial_date
        self.final_date = final_date
        self.routes_travled = routes_travled


"""
    @property
    def owner_name(self):
        if self.company:
            return self.company.owner.full_name
        return ''

    @property
    def company_name(self):
        if self.company:
            return self.company.name
        return ''

    @property
    def owner_email(self):
        if self.company:
            return self.company.owner.email
        return ''
"""

"""

class Income():

    def __init__(self, date, kind, detail, client, amount):
        self.date = str(date.date())
        self.kind = kind
        self.detail = detail
        self.client = client.get_full_name if client is not None else " "
        self.amount = amount


class IncomeProducts():

    def __init__(self, date, products, amount):
        self.date = date
        self.products = products
        self.amount = amount


class Outcome():

    def __init__(self, date, kind, detail, category, provider, amount):
        self.date = str(date.date())
        self.kind = kind
        self.detail = detail
        self.category = category
        self.provider = provider.get_name_provider if provider is not None else " "
        self.amount = amount

"""


class RoutesTraveledReport(FileReport):

    def __init__(self, title, initial_date, final_date, routes_travled):
        super(RoutesTraveledReport, self).__init__(
            title, initial_date, final_date, routes_travled)
        self.routes_travled = routes_travled
    """
    @property
    def collection_income(self):
        c_incomes = self.transactions.filter(label=Transaction.COBRANZA)
        # sales_income = reduce(lambda x, y: x+y, [t.payment if t.payment is not None else 0 for t in c_incomes], 0)
        sales_income = reduce(
            lambda x, y: x + y, [t.total_amount if t.total_amount is not None else 0 for t in c_incomes], 0)
        return sales_income

    @property
    def sales_income(self):
        incomes = self.transactions.filter(kind=Transaction.INGRESO)
        # sales_income = reduce(lambda x, y: x+y, [t.payment if t.payment is not None else 0 for t in incomes], 0)
        sales_income = reduce(
            lambda x, y: x + y, [t.total_amount if t.total_amount is not None else 0 for t in incomes], 0)
        return sales_income - self.collection_income

    @property
    def spendings(self):
        outcomes = self.transactions.filter(kind=Transaction.EGRESO)
        sales_outcome = reduce(
            lambda x, y: x + y, [t.payment if t.payment is not None else 0 for t in outcomes], 0)
        return sales_outcome
    """
    @property
    def total_utility(self):
        return self.collection_income + self.sales_income - self.spendings

    def get_products(self, products):
        """Return a string with products name"""
        if not products:
            return "--"

        products_count = products.count()
        if products_count <= 2:
            return ", ".join([p.product.name for p in products])

        first_two_products = [p.product.name for p in products[:2]]
        remaining_products_count = products_count - 2
        return f"{', '.join(first_two_products)}, (...{remaining_products_count}+)"


"""
class PDF(FPDF):
    pdf_w = 210
    pdf_h = 297

    line_height = 6
    line_number = line_height
    left_margin = 20
    right_margin = 190
    line_limit = 215  # amount of lines in a page

    # font sizes
    title_size = 14
    subtitle_size = 11
    paragraph_size = 9

    def set_data(self, data):
        self.data = data

    data = {
        "title": "Reporte flujo de efectivo",
        "initial_date": "01/11/21",
        "final_date": "08/11/21",
        "company_name": "Empresa",
        "owner_name": "Propietario Apellido",
        "owner_email": "owner@applikate.io",

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

    def set_title(self):
        self.set_xy(0, self.line_number)
        self.line_number += self.line_height
        self.set_font("Arial", "B", self.title_size)
        self.set_text_color(0, 0, 0)
        self.cell(w=210.0, h=40.0, align="C", txt=self.data['title'], border=0)

    def set_subtitle(self):
        self.set_xy(0, self.line_number)
        self.line_number += self.line_height
        self.set_font("Arial", "", self.subtitle_size)
        self.set_text_color(0, 0, 0)
        self.cell(w=210.0, h=40.0, align="C",
                  txt=f"Periodo de reporte: {self.data['initial_date']} al {self.data['final_date']}".format(), border=0)

    def header_1(self, text):
        self.set_xy(self.left_margin, self.line_number)
        self.line_number += self.line_height
        self.set_font("Arial", "B", self.subtitle_size)
        self.set_text_color(0, 0, 0)
        self.cell(w=210.0, h=40.0, align="L", txt=text, border=0)

    def header_1_cols(self, text, cols=None):
        if cols is None:
            cols = len(text)
        width = int((self.right_margin - self.left_margin) / cols)
        for i in range(len(text)):
            x = self.left_margin + i * width
            self.set_xy(x, self.line_number)
            self.set_font("Arial", "B", self.subtitle_size)
            self.set_text_color(0, 0, 0)
            if (cols is not None and i == cols-1):
                self.cell(w=30.0, h=40.0, align="R", txt=text[i], border=0)
            else:
                self.cell(w=210.0, h=40.0, align="L", txt=text[i], border=0)

        self.line_number += self.line_height

    def header_resume_cols(self, text, cols=None):
        if cols is None:
            cols = len(text)
        width = int((self.right_margin - self.left_margin) / cols)
        for i in range(len(text)):
            x = self.left_margin + i * width + 10
            self.set_xy(x, self.line_number)
            self.set_font("Arial", "B", self.subtitle_size+1)
            self.set_text_color(0, 0, 0)
            self.cell(w=210.0, h=40.0, align="L", txt=text[i], border=0)

        self.line_number += self.line_height

    def header_incomes_cols(self, text, cols=None):
        if cols is None:
            cols = len(text)
        width = int((self.right_margin - self.left_margin) / cols)
        for i in range(len(text)):
            if (i == 1):
                x = self.left_margin + i * width-15
            else:
                x = self.left_margin + i * width

            self.set_xy(x, self.line_number)
            self.set_font("Arial", "B", self.subtitle_size)
            self.set_text_color(0, 0, 0)
            if (cols is not None and i == cols-1):
                self.cell(w=30.0, h=40.0, align="R", txt=text[i], border=0)
            else:
                self.cell(w=210.0, h=40.0, align="L", txt=text[i], border=0)

        self.line_number += self.line_height

    def header_outcomes_cols(self, text, cols=None):
        if cols is None:
            cols = len(text)
        width = int((self.right_margin - self.left_margin) / cols)
        for i in range(len(text)):
            if (i == 1):
                x = self.left_margin + i * width-10
            elif (i == 2):
                x = self.left_margin + i * width+30
            elif (i == 3):
                x = self.left_margin + i * width+20
            else:
                x = self.left_margin + i * width

            self.set_xy(x, self.line_number)
            self.set_font("Arial", "B", self.subtitle_size)
            self.set_text_color(0, 0, 0)
            if (cols is not None and i == cols-1):
                self.cell(w=30.0, h=40.0, align="R", txt=text[i], border=0)
            else:
                self.cell(w=210.0, h=40.0, align="L", txt=text[i], border=0)

        self.line_number += self.line_height

    def paragraph_1(self, text):
        self.set_xy(self.left_margin, self.line_number)
        self.line_number += self.line_height
        self.set_font("Arial", "", self.paragraph_size)
        self.set_text_color(0, 0, 0)
        self.cell(w=210.0, h=40.0, align="L", txt=text, border=0)

    def paragraph_1_cols(self, text):
        cols = len(text)
        width = int((self.right_margin - self.left_margin) / cols)
        # make columns in a row
        for i in range(cols):
            x = self.left_margin + i * width
            self.set_xy(x, self.line_number)
            self.set_font("Arial", "", self.paragraph_size)
            self.set_text_color(0, 0, 0)
            if (i == cols-1):
                self.cell(w=30.0, h=40.0, align="R", txt=text[i], border=0)
            else:
                self.cell(w=210.0, h=40.0, align="L", txt=text[i], border=0)

        self.line_number += self.line_height

    def paragraph_resume_cols(self, text):
        cols = len(text)
        width = int((self.right_margin - self.left_margin) / cols)
        # make columns in a row
        for i in range(cols):
            x = self.left_margin + i * width + 10
            self.set_xy(x, self.line_number)
            self.set_font("Arial", "", self.paragraph_size+5)
            self.set_text_color(0, 0, 0)
            self.cell(w=210.0, h=40.0,
                      align="L", txt=text[i], border=0)

        self.line_number += self.line_height

    def paragraph_incomes_cols(self, text):
        cols = len(text)
        width = int((self.right_margin - self.left_margin) / cols)
        # make columns in a row
        for i in range(cols):
            if (i == 1):
                x = (self.left_margin + i * width)-15
            else:
                x = self.left_margin + i * width

            self.set_xy(x, self.line_number)
            self.set_font("Arial", "", self.paragraph_size)
            self.set_text_color(0, 0, 0)

            if (i == cols-1):
                self.cell(w=30.0, h=40.0, align="R", txt=text[i], border=0)
            elif (i == 0):
                self.cell(w=20.0, h=40.0, align="R", txt=text[i], border=0)
            else:
                self.cell(w=210.0, h=40.0, align="L", txt=text[i], border=0)

        self.line_number += self.line_height

    def paragraph_outcomes_cols(self, text):
        cols = len(text)
        width = int((self.right_margin - self.left_margin) / cols)
        # make columns in a row
        for i in range(cols):
            if (i == 1):
                x = (self.left_margin + i * width)-10
            elif (i == 2):
                x = (self.left_margin + i * width)+30
            elif (i == 3):
                x = (self.left_margin + i * width)+20
            else:
                x = self.left_margin + i * width

            self.set_xy(x, self.line_number)
            self.set_font("Arial", "", self.paragraph_size)
            self.set_text_color(0, 0, 0)

            if (i == cols-1):
                self.cell(w=30.0, h=40.0, align="R", txt=text[i], border=0)
            elif (i == 0):
                self.cell(w=20.0, h=40.0, align="R", txt=text[i], border=0)
            else:
                self.cell(w=210.0, h=40.0, align="L", txt=text[i], border=0)

        self.line_number += self.line_height

    def resume_box(self):
        # >> Resume Line Box
        self.set_draw_color(r=83, g=22, b=153)  # rgb(83,22,153)
        self.line(20, 80, 210-20, 80)       # top line
        self.line(210-20, 97, 210-20, 80)   # left line
        self.line(20, 97, 210-20, 97)       # bottom line
        self.line(20, 97, 20, 80)           # right line

    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'Reporte generado por APPLIKATE para la empresa %s' %
                  self.data["company_name"], 0, 0, 'L')
        # self.cell(0, 10, 'Página %s' % self.page_no(), 0, 0, 'C')

    def generate(self):
        self.add_page()

        self.set_title()
        self.set_subtitle()
        self.image("apps/companies/pdf_excel/image1.png", 170, 21, 20, 20)
        self.header_1("")
        self.header_1_cols(
            ["Nombre de empresa:", self.data["company_name"]], 3)
        self.header_1_cols(["Nombre de usuario:", self.data["owner_name"]], 3)
        self.header_1_cols(
            ["Correo electrónico:", self.data["owner_email"]], 3)
        self.header_1_cols(["Fecha de emisión:", str(
            date.today().strftime("%d-%m-%Y"))], 3)
        self.header_1("")

        self.resume_box()
        self.header_1("Resumen")
        self.header_1("")
        self.header_resume_cols(
            ["Ingresos ventas:", "Gastos:", "UTILIDAD TOTAL:"])
        params = list(map(lambda x: str(x), [
                      self.data['sales_income'], self.data['spendings'],
                      self.data['total_utility']]))
        self.paragraph_resume_cols(params)

        # self.header_1("Ingresos ventas       Ingresos cobranzas      Gastos      UTILIDAD TOTAL")
        # self.header_1_cols(["Ingresos ventas", "Ingresos cobranzas", "Gastos", "UTILIDAD TOTAL"])
        # params = list(map(lambda x: str(x), [self.data['sales_income'], self.data['collection_income'], self.data['spendings'], self.data['total_utility']]))

        self.set_draw_color(r=255, g=166, b=26)  # rgb(255,166,26)

        self.header_1("")
        self.header_1("")
        self.header_1("INGRESOS (ventas - cobranzas)")
        self.header_incomes_cols(["Fecha", "Detalle", "Cliente", "Monto"])
        for inc in self.data["incomes"]:
            params = list(map(lambda x: str(x) if x is not None else "", [
                          inc['date'],
                          inc['detail'],
                          inc['client'],
                          "    "+str(inc['amount'])
                          ]))
            # print("\n", params)
            # self.paragraph_1_cols(params)
            self.paragraph_incomes_cols(params)
            self.line(self.left_margin, self.line_number+17,
                      self.right_margin, self.line_number+17)
            if self.line_number > self.line_limit:
                self.add_page()
                self.line_number = 6

        self.header_1("")
        self.header_1("")
        self.header_1("EGRESOS (gastos)")
        self.header_outcomes_cols(
            ["Fecha", "Detalle", "Categoría", "Proveedor", "Monto"])
        for out in self.data["outcomes"]:
            params = list(map(lambda x: str(x) if x is not None else "", [
                          out['date'], out['detail'], out['category'],
                          out['provider'], out['amount']]))
            self.paragraph_outcomes_cols(params)
            self.line(self.left_margin, self.line_number+17,
                      self.right_margin, self.line_number+17)
            if self.line_number > self.line_limit:
                self.add_page()
                self.line_number = 6

        # self.header_1("")
        # self.header_1("EGRESOS (gastos)")
        # self.footer()

        # self.output("test.pdf", "F")
        return self.output(dest="S")

"""
# pdf = PDF(orientation="P", unit="mm", format="Letter")
# pdf.generate()
