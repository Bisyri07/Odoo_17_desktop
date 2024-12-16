/* @odoo-module */

import { registry } from "@web/core/registry"
import { Component, xml } from "@odoo/owl"


// 1. membuat sebuah kelas
class LeafletMapController extends Component {
    static template = xml`<div>Leaflet Map View</div>`
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