# -*- coding: utf-8 -*-
import json
import logging
import requests
import datetime

from odoo import api, fields, models, _
 
 
_logger = logging.getLogger(__name__)


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    base_uuid = fields.Text(string="DB:",default= lambda self : self.env["ir.config_parameter"].search([("key","=","database.uuid")]).value)
    update_full_catalog = fields.Boolean(
        string="Update full catalog cron"
    )
    rate_type = fields.Selection([
        ("purchase", "Compra"),
        ("sale", "Venta")],
        string = "Tipo",
        required = True,
        default = "sale"    
        )
    rate_inv = fields.Float("Tipo de cambio", 
                            #compute="run_update_currency", 
                            required = True
                            )
    rate = fields.Float(string = "Cambio inverso", 
                        compute = "calculate_rate", 
                        store= True
                        )
    name_type = fields.Char("Nombre a mostrar", compute = "get_name")
    
    @api.depends("rate_type","name")
    def get_name(self):
        for rec in self:
            if rec.rate_type == "purchase":
                rec.name_type = rec.name + " - " + "Compra"
            else:
                rec.name_type = rec.name + " - " + "Venta"
    @api.depends("rate_inv")
    def calculate_rate(self):
        for rec in self:
            if rec.rate_inv:
                rec.rate = 1/rec.rate_inv
    def update(self):
        for rec in self:
            if rec.name == "PEN":
                rec.currency_unit_label = "Soles"
                rec.currency_subunit_label = "Centimos"
                rec.symbol = "S/"
    _sql_constraints = [
        ('unique_name', 
        'unique (name,type)', 
        'Solo puede existir una moneda con el mismo tipo de cambio!'),
        ('rounding_gt_zero', 
        'CHECK (rounding>0)', 
        'The rounding factor must be greater than 0!')
    ]
        
    @api.model
    def run_update_currency(self):
        token = "YuA0fYfpjB9CCnGhP7n6U5sQ6ACahY6nzS8iUZoQb4fTMlOxbvB0HSsh54mC"
        url = "http://localhost:8071/hola"
            
        headers = {
            "Content-Type": "application/json",
            "token": token
            }
        params={"DB":self.env["ir.config_parameter"].search([("key","=","database.uuid")]).value}
        response = requests.request(method="POST",url=url, headers=headers,data=params)
        #for rec in self.env["res.currency"].search([]):
        #    pass
            #if response.json()["currency"]==rec.name:
            #    if rec.rate_type=="purchase":
            #        rec.rate_inv = float(response.json()["rate_purchase"])
            #        rec.date = response.json()["fecha"]
            #    else:
            #        rec.rate_inv = float(response.json()["rate_sale"])
            #        rec.date = response.json()["date"]

    
    