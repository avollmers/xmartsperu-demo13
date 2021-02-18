odoo.define('l10n_pe_edi_pos.ticket', function (require) {
    var screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var qweb = core.qweb;


    screens.ReceiptScreenWidget.include({

        render_receipt: function () {
            this._super();
            var self = this;
            var order = this.pos.get_order();
            
            
            if (!this.pos.config.iface_print_via_proxy  && order.is_to_invoice()) {
                var invoiced = new $.Deferred();
                rpc.query({
                    model: 'pos.order',
                    method: 'search_read',
                    domain: [['pos_reference', '=', order['name']]],
                    fields: ['account_move',]
                }).then(function (orders) {
                    if (orders.length > 0 && orders[0]['account_move'] && orders[0]['account_move'][1]) {
                        var invoice_number = orders[0]['account_move'][1].split(" ")[0];
                        self.pos.get_order()['invoice_number'] = invoice_number;
                        var document_invoice = rpc.query({
                                model: 'account.move',
                                method: 'search_read',
                                domain: [['name', '=', invoice_number]],
                                fields: ['name','l10n_latam_document_type_id','l10n_pe_edi_igv_percent','l10n_pe_edi_amount_in_words']
                            });   
                        document_invoice.then( function(invoice) {
                            var type_document = invoice[0]['l10n_latam_document_type_id'][0]
                            var type_document_model = order.pos.db.l10n_latam_document_by_id[type_document]
                            
                            if (type_document_model){
                                self.pos.get_order()['type_of_invoice_document'] = (type_document_model.name + " Electrónica").toUpperCase();
                            }
                            if (invoice[0]['l10n_pe_edi_igv_percent']){
                                self.pos.get_order()['igv_percent']= (invoice[0]['l10n_pe_edi_igv_percent']).toFixed(2)
                            }
                            if (invoice[0]['l10n_pe_edi_amount_in_words']){
                                self.pos.get_order()['amount_in_words']= (invoice[0]['l10n_pe_edi_amount_in_words']).toUpperCase()
                            }
                            self.$('.pos-receipt-container').html(qweb.render('OrderReceipt', self.get_receipt_render_env()));
                                 
                        })
                       
                        if (order.pos.currency.name){
                            var currency = {
                                'PEN': "SOLES",        
                                'USD': "DOLLARS",       
                                'EUR': "EUROS",        
                            }

                            var pos_currency = order.pos.currency.name.toString()
                            self.pos.get_order()['currency_name']=currency[pos_currency]
                        }
                       
                        var  qr_data = "";
                        if (order.pos.company.vat) {
                            qr_data += '|' + order.pos.company.vat;
                        }
                        if (invoice_number) {
                            qr_data += '|' + invoice_number.split("-")[0];
                            qr_data += '|' + invoice_number.split("-")[1];
                        }
                        if (order.get_total_discount()) {
                            qr_data += '|' + order.get_total_discount().toFixed(2);
                        }
                        if (order.get_total_with_tax()) {
                            qr_data += '|' + order.get_total_with_tax().toFixed(2);
                        }
                        if (order.formatted_validation_date) {
                            let formatted_date = order.validation_date.getFullYear() + "-" + (order.validation_date.getMonth() + 1) + "-" + order.validation_date.getDate()
                            qr_data += '|' + formatted_date;
                            let formatted_date_order =  order.validation_date.getDate() + "/" + (order.validation_date.getMonth() + 1) + "/" +  order.validation_date.getFullYear()
                            self.pos.get_order()['date']= formatted_date_order;    
                        }
                        if (order.get_client()['vat']) {
                            qr_data += '|' + order.get_client()['vat'];
                        }
                        var url_location = window.location.origin + '/report/barcode/QR/';
                        self.pos.get_order()['url_barcode'] = url_location + qr_data;

                        if (order.pos.company.l10n_pe_edi_ose['authorization_message']) {
                            self.pos.get_order()['authorization_message'] = $(order.pos.company.l10n_pe_edi_ose['authorization_message']).text();
                        }
                        if (order.pos.company.l10n_pe_edi_ose['control_url']) {
                            self.pos.get_order()['control_url']= order.pos.company.l10n_pe_edi_ose['control_url']
                        }
                        
                        self.$('.pos-receipt-container').html(qweb.render('OrderReceipt', self.get_receipt_render_env()));
                    }
                    invoiced.resolve();
                }).catch(function (error) {
                    invoiced.reject(error);
                });
                return invoiced;
            } else {
                this._super();
            }
        }
    })
});