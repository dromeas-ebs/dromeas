# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import requests
from datetime import datetime
from odoo.exceptions import ValidationError
import json


class ProductionCustom(models.Model):
    _inherit = 'mrp.production'

    def button_plan(self):
        res = super(ProductionCustom, self).button_plan()
        if res:
            self.call_api()
        return res

    def open_produce_product(self):
        action = super(ProductionCustom, self).open_produce_product()
        return action

    def call_api(self):
        url = "https://staging.epoptia.io/api/login"

        params = {
            "username": "api",
            "password": "12345678"
        }

        # get_token_request = requests.post(
        #     url=url,
        #     json=params
        # )
        # if get_token_request.status_code != 200:
        #     raise ValidationError(_("Connection Error"))
        # data = get_token_request.json()
        # token = data['token']
        array_list = []
        json_object = {
            "workorder_id": self.id,
            "remote_code": self.name,
            "from_plandate": self.date_planned_start.strftime("%d/%m/%Y"),
            "to_plandate": self.date_planned_finished.strftime("%d/%m/%Y"),
            "dealine_date": (self.date_deadline and self.date_deadline.strftime("%d/%m/%Y")) or "",
            "product": {
                "id": self.product_id.id,
                "name": self.product_id.name,
                "code": self.product_id.default_code,
            },
            "quantity": self.product_qty
        }
        bom = self.bom_id
        for line in bom.bom_line_ids:
            array_list.append({
                "product": {
                    "id": line.product_id.id,
                    "name": line.product_id.name,
                    "code": line.product_id.default_code,
                },
                "quantity": line.product_qty
            })

        json_object['bom'] = array_list
        # data = [json_object]
        # data_json = json.dumps(data)
        # print(data_json)
        url = "https://staging.epoptia.io/api/odoo/workorders"
        # url = "http://localhost:8069/ebs/api"
        param = {'params': json_object}

        print(json.dumps(json_object))
        send_data_request = requests.post(
            url,
            json=json_object,
        )
        # headers = {'Content-Type': 'application/json'}

        # send_data_request = requests.post(
        #     url,
        #     json=data_json,
        #     headers={'Authorization': 'Bearer '+token,'Content-Type': 'application/json'}
        # )

        if send_data_request.status_code != 200:
            raise ValidationError(_("Connection Error!"))
        print(send_data_request.text)

        data = send_data_request.json()
        if not data['message']:
            raise ValidationError("Connection Error with API, please try again.")
        # response_json = send_data_request.json()
        # wiz = self.env['message.wizard'].create({
        #     'message': "Success",
        # })
        # view_form_id = self.env.ref('ebs_dromeas_api.message_wizard_form').id
        # return {
        #     'name': _('Message'),
        #     'res_model': 'message.wizard',
        #     'type': 'ir.actions.act_window',
        #     'views': [(view_form_id, 'form')],
        #     'view_mode': 'form',
        #     'res_id': wiz.id,
        #     'target': 'new',
        # }


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    def do_produce(self):
        return_action = super(MrpProductProduce, self).do_produce()
        self.production_id.call_api()
        return return_action
