/* @odoo-module */
import { templates } from "@web/core/assets"

const { Component, whenReady, App} = owl


class MyOwlApp extends Component {
    static template = "master_purchasing.MyOwlApp"
}

whenReady(
    ()=>{
       const owl_app = new App(MyOwlApp, { templates })
       
       const owl_app_selector = document.querySelector('#owl_wrap')
       if (owl_app_selector){
           owl_app.mount(owl_app_selector)      
       }
    }
)












