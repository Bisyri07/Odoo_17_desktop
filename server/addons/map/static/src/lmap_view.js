/* @odoo-module */

import { registry } from "@web/core/registry"
import { Component, xml } from "@odoo/owl"
import { standardViewProps } from "@web/views/standard_view_props"


// 1. membuat sebuah kelas
class LeafletMapController extends Component {
    static template = xml`
    <div><h1>Leaflet Map View</h1></div>
    `
    // 5. Mendefinisikan properti (atau data) yang dapat diterima oleh komponen dari induknya.
    static props = {
        ...standardViewProps,

    }

    // 4. untuk memuat state (data awal) ke dalam DOM
    setup(){
        console.log(this)
    }
}


// 2. membuat objek konstan
const leafletMapView = {
    type: "lmap",
    display_name: "Leaflet Map",
    icon: "fa fa-map-marker",
    multiRecord: true,
    Controller: LeafletMapController
}


// 3. Kode ini mendaftarkan tampilan baru (custom view) bernama lmap ke dalam kategori tampilan (views) di sistem Odoo
registry.category("views").add("lmap", leafletMapView)