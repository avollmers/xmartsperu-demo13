"use strict";
odoo.define('l10n_pe_edi_pos.screen_journal', function (require) {

    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;

    screens.PaymentScreenWidget.include({
        
        click_invoice_journal: function (journal_id) { // change invoice journal when create invoice
            var order = this.pos.get_order();
            order['invoice_journal_id'] = journal_id;
            this.$('.journal').removeClass('highlight');
            var $journal_selected = this.$("[journal-id='" + journal_id + "']");
            $journal_selected.addClass('highlight');
        },
        render_invoice_journals: function () { // render invoice journal, no use invoice journal default of pos
            var self = this;
            var methods = $(qweb.render('journal_list', {widget: this}));
            methods.on('click', '.journal', function () {
                self.click_invoice_journal($(this).data('id'));
            });
            return methods;
        },
        renderElement: function () {
            var self = this;
            this._super();
            if (this.pos.config.module_account && this.pos.config.invoice_journal_ids && this.pos.config.invoice_journal_ids.length > 0 && this.pos.journals) {
                var methods = this.render_invoice_journals();
                methods.appendTo(this.$('.invoice_journals'));

                var order = this.pos.get_order();
                if (order){
                    order['to_invoice'] = true;
                }
                
                
            }
            
        },
        validate_order: function (force_validation) {

            if (this.pos.config.module_account && this.pos.config.invoice_journal_ids && this.pos.config.invoice_journal_ids.length > 0 && this.pos.journals){
                var order = this.pos.get_order();
                var client = this.pos.get_order().get_client();
                var type_document ;
                _.each(order.pos.journals, function(doc) {
                    if (order.invoice_journal_id ==doc.id ){
                        type_document = doc.l10n_latam_document_type_id[0]
                    }
                })
                if (this.pos.config.module_account && !type_document && this.pos.config.module_account){
                    return this.pos.gui.show_popup('confirm', {
                        title: _t('ALERT'),
                        body: _t('Please select a Document type.'),
                    })
                }
            
                var type_document_model = this.pos.db.l10n_latam_document_by_id[type_document]
                if (client) {
                    var type_identification =client.l10n_latam_identification_type_id[0];
                    if (!type_identification){
                        return this.pos.gui.show_popup('confirm', {
                            title: _t('ALERT'),
                            body: _t('Select the Identification type of the client: ') + client['name'],
                        })
                    }
                    var type_identification_model = this.pos.db.l10n_latam_identification_by_id[type_identification]
                    if (type_document_model.code == "03"){
                
                        if(type_identification_model.l10n_pe_vat_code == '1'){
                            if (client['vat'].length != 8){
                                return this.pos.gui.show_popup('confirm', {
                                    title: _t('ALERT'),
                                    body: _t("The DNI of the client: ") + client['name'] + _t(', is not valid.'),
                                })
                            } 
                        }
                        
                    }
                    if (type_document_model.code == "01"){
                        if(type_identification_model.l10n_pe_vat_code != '6'){
                            return this.pos.gui.show_popup('confirm', {
                                title: _t('ALERT'),
                                body: _t('The document type \'Factura\' is valid only for clients with valid RUC.'),
                            })
                        }
                        else{
                            if (client['vat'].length != 11){
                                return this.pos.gui.show_popup('confirm', {
                                    title: _t('ALERT'),
                                    body: _t('The RUC of the client: ') + client['name'] + _t(', is not valid.'),
                                })
                            }
                        }
                        
                    }   
                }
                else{
                    if(order.is_to_invoice()== true && this.pos.config.module_account){
                        return this.pos.gui.show_popup('confirm', {
                            title: _t('ALERT'),
                            body: _t('Select a client for creating an Invoice.'),
                        })
                    }                
                }            
                
            }
            this._super();
        },
        
    });
    screens.ClientListScreenWidget.include({
        show: function(){
            this._super();
            var self = this;
            this.$('.new-customer').click(function(){
                self.display_client_details('edit',{
                    'country_id': self.pos.company.country_id,
                    'name': _t('New client'),
                });
            });
        },
    });
    
});
