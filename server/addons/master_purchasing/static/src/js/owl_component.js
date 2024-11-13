/* @odoo-module */
import { Component, xml, mount, whenReady} from "@odoo/owl"

class OwlMainComponent extends Component {

}

// template
OwlMainComponent.template = xml`
<div class="p-4 border">
    <h3>This is rendered using OWL</h3>
</div>
`

whenReady(
    ()=>{
        const element = document.querySelector('.js_template_owl')
        if (element){
        // mount is used to attach a component to a specific DOM element
        mount(OwlMainComponent, element)
        }
    }
)







