/* @odoo-module */
import { Component, xml, mount, whenReady, useState } from "@odoo/owl"
import { templates } from "@web/core/assets"

class OwlSubComponent extends Component {
    static template = "master_purchasing.owl_sub_component"
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

// template
// OwlMainComponent.template = xml`
// <div class="p-4 border">
//     <h3>This is rendered using OWL</h3>
// </div>
// `

OwlMainComponent.template = "master_purchasing.owl_main_component";
OwlMainComponent.components = { OwlSubComponent }

whenReady(
    ()=>{
        const element = document.querySelector('.js_template_owl')
        if (element){
        // mount is used to attach a component to a specific DOM element
        mount(OwlMainComponent, element, { templates })
        }
    }
)







