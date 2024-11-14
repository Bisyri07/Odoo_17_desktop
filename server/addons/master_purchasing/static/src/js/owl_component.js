/* @odoo-module */
import { Component, xml, mount, whenReady, useState } from "@odoo/owl"
import { templates } from "@web/core/assets"

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


OwlMainComponent.template = "master_purchasing.owl_main_component";
OwlMainComponent.components = { OwlSubComponent, OwlSubComponentChild }

whenReady(
    ()=>{
        // const element = document.querySelector('.js_template_owl')
        // if (element){
        // // mount is used to attach a component to a specific DOM element
        // mount(OwlMainComponent, element, { templates })
        // }

        const element = document.querySelectorAll('.js_template_owl')
        if (element.length > 0){
            element.forEach(el => mount(OwlMainComponent, el, {templates}))
        }
    }
)







