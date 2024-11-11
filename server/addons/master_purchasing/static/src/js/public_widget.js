/* @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.jsTemplate = publicWidget.Widget.extend({
    selector: '.js_template',
    template: 'master_purchasing.jsTemplate',
    start(){
        // console.log("JS Template activated!")
        this.renderElement();
    }
})
