/* @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToElement } from "@web/core/utils/render"


publicWidget.registry.jsTemplate = publicWidget.Widget.extend({
    selector: '.js_template',
    template: 'master_purchasing.jsTemplate',
    start(){
        // console.log("JS Template activated!")
        this.renderElement();
    }
})

publicWidget.registry.templateWithVariables = publicWidget.Widget.extend({
    selector: '.js_tmp_with_variables',
    template: 'master_purchasing.templateWithVariables',

    init(){
        this._super(...arguments);
        this.orm = this.bindService("orm");
    },

    async start(){
        const content = renderToElement(this.template, {
            string: "QWEB Tutorial using Javascript",
            array: [1,2,3,4,5],
            email: 'mbisyri33@gmail.com',
            model: await this.orm.searchRead("sales.order", [], ["item"]),
        })
        this.$target.html(content)
    }
})
