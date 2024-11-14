/* @odoo-module */
import { Component, xml, mount, whenReady, useState, onWillStart } from "@odoo/owl"
import { templates } from "@web/core/assets"
import { jsonrpc } from "@web/core/network/rpc_service"

class OwlSubComponent extends Component {
    static template = "master_purchasing.owl_sub_component"
}

class OwlSubComponentChild extends Component {
    static template = "master_purchasing.owl_sub_component_child"
}

class OwlMainComponent extends Component {
    setup(){
        this.state = useState({
            counter: 0,
        })

        this.date = new Date().toLocaleString()

    }
    increaseCounter(){
        this.state.counter++
    }
    get someList(){
        return [1,2,3,4,5]
    }
}


class OwlWithBackEndData extends Component {
    static template = "master_purchasing.with_backend_data"

    setup(){
        this.state = useState({
            orders: [],
            txtInput: "",
        })
        onWillStart(async ()=>{
            const data = await jsonrpc("web/dataset/call_kw/sales.order/search_read",{
                model: "sales.order",
                method: "search_read",
                args: [
                    [['status', 'in', ['confirmed', 'canceled']]], 
                    ['item', 'item_code', 'so_no', 'so_date', 'currency', 'qty', 'total']
                ],
                kwargs: {
                    limit: 3,
                    order: 'so_date DESC'
                }
            })
            this.state.orders = data;
        });
    }

}


OwlMainComponent.template = "master_purchasing.owl_main_component";
OwlMainComponent.components = { OwlSubComponent, OwlSubComponentChild }

// DoM
whenReady(
    ()=>{
        // const element = document.querySelector('.js_template_owl')
        // if (element){
        // // mount is used to attach a component to a specific DOM element
        // mount(OwlMainComponent, element, { templates })
        // }

        const element = document.querySelectorAll('.js_template_owl')
        if (element){
            element.forEach(el => mount(OwlMainComponent, el, {templates}))
        }

        const owlTemplateWithData = document.querySelector('.owl_template_data')
        if (owlTemplateWithData){
            mount(OwlWithBackEndData, owlTemplateWithData, { templates })
        }

    }
)







