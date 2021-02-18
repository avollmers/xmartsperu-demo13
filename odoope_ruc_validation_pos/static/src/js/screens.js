odoo.define('odoope_ruc_validation_pos.ruc_validation_screens', function (require) {
    "use strict";

    var pos_screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var _t = core._t;

    var CustomScreenWidget = pos_screens.ClientListScreenWidget.include({
        get_data_sunat:function(partner, contents){
            var self = this;
            var type_doc = $('.detail.type-doc').val();
            if (!type_doc){
                return this.pos.gui.show_popup('confirm', {
                    title: _t('ALERT'),
                    body: _t('Select the Identification type of the client and then write the number'),
                })
            }
            var type_doc_model = this.pos.db.l10n_latam_identification_by_id[type_doc]
            if (type_doc_model.l10n_pe_vat_code == '6') {
                var fields = {};
                var contents = this.$('.client-details-contents');

                this.$('.detail.vat').each(function (idx, el) {
                    fields[el.name] = el.value || false;
                });
                if (!fields.vat){
                    return this.pos.gui.show_popup('confirm', {
                        title: _t('ALERT'),
                        body: _t('You must enter the document number'),
                    })
                };
                if (type_doc_model.l10n_pe_vat_code === '6') {
                    if (fields.vat.length != 11){
                        return this.pos.gui.show_popup('confirm', {
                            title: _t('ALERT'),
                            body: _t('The RUC of the client is not valid'),
                        })
                    };
                    rpc.query({
                        model: 'res.partner',
                        method: 'sunat_connection',
                        args: [fields.vat]
                    }).then( function(result) {
                        contents.find('input[name="name"]').val(result['business_name']);
                        contents.find('input[name="street"]').val(result['residence']); 
                        contents.find('select[name="state_id"]').val(result['value']['state_id']);
                    });
                    
                };
            };
            
        },
        display_client_details: function(visibility,partner,clickpos){
            this._super(visibility,partner,clickpos);
            var self = this;
            var contents = this.$('.client-details-contents');
            contents.off('focusout','.detail.vat');
            contents.on('focusout','.detail.vat', function(){ self.get_data_sunat(partner, contents); });
            
        },

    });
   
});