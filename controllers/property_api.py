import math
from odoo import http
from odoo.http import request
from urllib.parse import parse_qs
import json


def invalid_response(error, status):
    response_body = {
        "message": "invalid process",
        "error": error,
    }
    return request.make_json_response(response_body, status=status)

def valid_response(data, status):
    response_body = {
        "message": "successful",
        "data": data
    }
    return request.make_json_response(response_body, status=status)

class PropertyApi(http.Controller):

    @http.route('/v1/property', methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        # validation for name
        if not vals.get('name'):
            return request.make_json_response(
                {
                    "message": "please adding name"
                },
                status=400
            )
        res = request.env['property'].sudo().create(vals)
        try:
            if res:
                print(res)
                return request.make_json_response(
                    {
                        "message": "property has been created successfully",
                        "name": res.name,
                        "id": res.id
                    },
                    status=201
                )
        except Exception as error:
            return request.make_json_response(
                {
                    "message": error
                },
                status=400
            )

# diff type json---------------------------------------------

    @http.route('/v1/property/json', methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        try:
            if res:
                print(res)
                return request.make_json_response(
                    {
                        "message": "property has been created successfully"
                    },
                    status=201
                )

        except Exception as error:
            return {
                    "message": error,
            }

# for update on property-----------------------------

    @http.route("/v1/property/<int:property_id>", methods=['PUT'], type="http", auth="none", csrf=False)
    def property_update(self, property_id):
        try:
            property_id = request.env['property'].search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response(
                    {
                        "message": "ID dose not exist"
                    },
                    status=400
                )
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return request.make_json_response(
                {
                    "message": "property has been updating successfully"
                },
                status=200
            )
        except Exception as error:
            return request.make_json_response(
                {
                    "message": error
                },
                status=400
            )

    @http.route("/v1/property/<int:property_id>", methods=['GET'], type="http", auth="none", csrf=False)
    def property_get_read(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make.json.response(

                    {
                        "error": "ID dose not exist"
                    },
                    status=400
                )
            return request.make_json_response(
                {
                    "id": property_id.id,
                    "name": property_id.name,
                    "postcode": property_id.postcode,
                    "owner": property_id.owner_id.name,
                    "garden_orientation": property_id.garden_orientation,
                    "bedrooms": property_id.bedrooms,
                    "selling_price": property_id.selling_price
                },
                status=200
            )
        except Exception as error:
            return request.make_json_response(
                {
                    "error": error
                },
                status=400
            )

    @http.route("/v1/property/<int:property_id>", methods=['DELETE'], type="http", auth="none", csrf=False)
    def property_delete(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make.json.response(

                    {
                        "error": "ID dose not exist"
                    },
                    status=400
                )
            property_id.unlink()
            return request.make_json_response(
                {
                    "message": "property has been deleted successfully",

                },
                status=200
            )
        except Exception as error:
            return request.make_json_response(
                {
                    "error": error
                },
                status=400
            )

    @http.route("/v1/property/<int:property_id>", methods=['GET'], type="http", auth="none", csrf=False)
    def property_get_read_list(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make.json.response(

                    {
                        "error": "ID dose not exist"
                    },
                    status=400
                )
            return request.make_json_response(
                {
                    "id": property_id.id,
                    "name": property_id.name,
                    "postcode": property_id.postcode,
                    "owner": property_id.owner_id.name,
                    "garden_orientation": property_id.garden_orientation,
                    "bedrooms": property_id.bedrooms,
                    "selling_price": property_id.selling_price
                },
                status=200
            )
        except Exception as error:
            return request.make_json_response(
                {
                    "error": error
                },
                status=400
            )

    @http.route("/v1/properties", methods=['GET'], type="http", auth="none", csrf=False)
    def property_get_read(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain = []
            page = offset = None
            limit = 0
            if params.get('page'):
                page = int(params.get('page')[0])
            else:
                page = 1

            if params.get('limit'):
                limit = int(params.get('limit')[0])
            else:
                limit = 0

            offset = (page * limit) - limit
            # print("offset = ", offset)
            # print("page = ", page)
            # print("limit = ", limit)

            # when search all for state
            if params.get('state'):
                property_domain += [('state', '=', params.get('state')[0])]
            property_ids = request.env['property'].sudo().search(property_domain, offset=offset, limit=limit, order='id DESC')
            property_count_ids = request.env['property'].sudo().search_count(property_domain)
            #  property_id = request.env['property'].sudo().search([])
            # print("property_count = ", property_count_ids)
            # print("property_ids = ", property_ids)
            # print("property_count_id = ", property_id)

            # if not property_domain:
            #     return request.make_json_response(
            #         {
            #             "error": "No valid search criteria provided"
            #         },
            #         status=400
            #     )

            if not property_ids:
                return request.make.json.response(

                    {
                        "error": "There are not record"
                    },
                    status=400
                )

            # return request.make_json_response([
            #     {
            #         "id": property_id.id,
            #         "name": property_id.name,
            #         "postcode": property_id.postcode,
            #         "owner": property_id.owner_id.name,
            #         "garden_orientation": property_id.garden_orientation,
            #         "bedrooms": property_id.bedrooms,
            #         "selling_price": property_id.selling_price
            #     } for property_id in property_ids],
            #     status=200
            # )

            return request.make_json_response(
                [
                    {
                        "data": {
                            "id": property_id.id,
                            "name": property_id.name,
                            "postcode": property_id.postcode,
                            "owner": property_id.owner_id.name,
                            "garden_orientation": property_id.garden_orientation,
                            "bedrooms": property_id.bedrooms,
                            "selling_price": property_id.selling_price
                        },
                        "pagination info": {
                            "page": page if page else 1,
                            "limit": limit if limit else 0,
                            "pages": math.ceil(property_count_ids/limit) if limit else 1,
                            "count record": property_count_ids,
                        }
                    }for property_id in property_ids
                ],
                status=200
            )

        except Exception as error:
            return request.make_json_response(
                {
                    "error": error,
                },
                status=400
            )

