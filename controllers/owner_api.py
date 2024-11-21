from odoo import http
from odoo.http import request
import json


class OwnerApi(http.Controller):

    # @http.route("/v1/owner", methods=["POST"], auth="none", type="http", csrf=False)
    # def create_owner(self):
    #     print("inside create owner")
    #     args = request.httprequest.data.decode()
    #     vals = json.loads(args)
    #     res = request.env['owner'].sudo().create(vals)
    #     if not vals.get('name'):
    #         return request.make_json_response(
    #             {
    #                 "message": "please adding name"
    #             },
    #             status=400
    #         )
    #     try:
    #         if res:
    #             return request.make_json_response(
    #                 {
    #                     "message": "successful add owner",
    #                     "id": res.id,
    #                     "name": res.name,
    #                     "phone": res.phone,
    #                 },
    #                 status=201
    #             )
    #     except Exception as error:
    #         return request.make_json_response(
    #             {
    #                 "error": error
    #             },
    #             status=400
    #         )

    @http.route("/v1/owner", methods=["POST"], auth="none", type="http", csrf=False)
    def create_owner(self):
        print("inside create owner")
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        # res = request.env['owner'].sudo().create(vals)

        if not vals.get('name'):
            return request.make_json_response(
                {
                    "message": "please adding name"
                },
                status=400
            )
        try:
            # res = request.env['owner'].sudo().create(vals)
            cr = request.env.cr
            columns = ', '.join(vals.keys())
            values = ', '.join(['%s'] * len(vals))
            query = f"INSERT INTO owner ({columns}) VALUES ({values}) RETURNING id, name, phone"
            cr.execute(query, tuple(vals.values()))
            res = cr.fetchone()
            if res:
                return request.make_json_response(
                    {
                        "message": "successful add owner",
                        "id": res[0],
                        "name": res[1],
                        "phone": res[2],
                    },
                    status=201
                )
        except Exception as error:
            return request.make_json_response(
                {
                    "error": error
                },
                status=400
            )

