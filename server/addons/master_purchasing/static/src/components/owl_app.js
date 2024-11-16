/* @odoo-module */
import { templates } from "@web/core/assets"
import { makeEnv, startServices } from "@web/env"
import { useService } from "@web/core/utils/hooks"


const { Component, whenReady, App, useState, onWillStart } = owl


class MyOwlApp extends Component {
    static template = "master_purchasing.MyOwlApp"

    // method
    setup(){
        this.state = useState({
            partners : [],
        })
        this.orm = useService("orm")

        onWillStart(async ()=>{
            const data = await this.orm.searchRead("res.partner", [], ["name"], {
                limit: 10,
                order: "id desc",
            })
            // console.log(data)
            this.state.partners = data
        })
    }
}


whenReady(
    async()=>{
        const env = makeEnv()
        await startServices(env)
        
        const owl_app = new App(MyOwlApp, { templates, env })
        
        const owl_app_selector = document.querySelector('#owl_wrap')
        if (owl_app_selector){
            owl_app.mount(owl_app_selector)      
        }
    }
)












