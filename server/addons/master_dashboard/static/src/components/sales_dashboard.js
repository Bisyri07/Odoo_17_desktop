/* @odoo-module */
// anotasi untuk memberi tahu Odoo bahwa file ini adalah modul JavaScript Odoo

// mengimpor registry dari modul inti Odoo
import { registry } from "@web/core/registry"
// import KpiCard dari kpi_card.js
import { KpiCard } from "./kpi_card/kpi_card"
// Fungsi ini digunakan untuk memuat file JavaScript secara dinamis pada runtime
import { loadJS } from "@web/core/assets"
// import ChartRenderer dari chart_renderer.js
import { ChartRenderer } from "./chart_renderer/chart_renderer"

// Component adalah library frontend untuk pembuatan UI di OWL 
const { Component, onWillStart, useRef, onMounted } = owl

// export: Membuat kelas ini dapat diimpor di file lain
export class OwlSalesDashboard extends Component {
    setup(){

    }
}

// Baris ini menghubungkan komponen OwlSalesDashboard dengan template XML-nya.
// ID template yang didefinisikan di file XML
OwlSalesDashboard.template = "master_dashboard.OwlSalesDashboard" 
OwlSalesDashboard.components = { KpiCard, ChartRenderer }


// registry.category("actions") => mengakses kategori actions dalam registry
// .add("master_dashboard.sales_dashboard", OwlSalesDashboard) menambahkan komponen OwlSalesDashboard 
// ke dalam kategori aksi dengan nama "master_dashboard.sales_dashboard"
registry.category("actions").add("master_dashboard.sales_dashboard", OwlSalesDashboard)

