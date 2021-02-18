"use strict";
odoo.define('l10n_pe_edi_pos.order', function (require) {

    var models = require('point_of_sale.models');
    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({

        init_from_JSON: function (json) {
            var res = _super_Order.init_from_JSON.apply(this, arguments);
            if (json.invoice_journal_id) {
                this.invoice_journal_id = json.invoice_journal_id;
                this.to_invoice = true;
            }            
            return res;
        },
        export_as_JSON: function () {
            var json = _super_Order.export_as_JSON.apply(this, arguments);
            
            if (this.invoice_journal_id) {
                json.invoice_journal_id = this.invoice_journal_id;
                this.to_invoice = true;
            }            
            return json;
        }
    });

});
    