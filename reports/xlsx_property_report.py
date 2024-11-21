from ast import literal_eval
from odoo import http
from odoo.http import request
import io
import xlsxwriter


class PropertyXlsxReport(http.Controller):


    @http.route('/v1/property/excel/report/<string:property_id>', type='http', auth='user')
    def download_property_excel_report(self, property_id):
        property_ids = request.env['property'].browse(literal_eval(property_id))
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Properties')

        header_formate = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
        string_formate = workbook.add_format({'border': 1, 'align': 'center'})
        price_formate = workbook.add_format({'num_format': '$##,##00.00', 'border': 1, 'align': 'center'})

        headers = ['Name', 'Postcode', 'Selling Price', 'Garden']
        for cul_num, header in enumerate(headers):
            worksheet.write(0, cul_num, header, header_formate)
        row_num = 1
        for property in property_ids:
            worksheet.write(row_num, 0, property.name, string_formate)
            worksheet.write(row_num, 1, property.postcode, string_formate)
            worksheet.write(row_num, 2, property.selling_price, price_formate)
            worksheet.write(row_num, 3, 'Yes' if property.garden else 'No', string_formate)
            row_num += 1

        workbook.close()
        output.seek(0)
        file_name = 'Property Report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename={file_name}')
            ]
        )

