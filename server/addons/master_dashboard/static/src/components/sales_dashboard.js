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
// 
import { useService } from "@web/core/utils/hooks"


// Component adalah library frontend untuk pembuatan UI di OWL 
const { Component, onWillStart, useRef, onMounted, useState } = owl

// export: Membuat kelas ini dapat diimpor di file lain
export class OwlSalesDashboard extends Component {

    // 1. Inisialisasi properti dan hook dalam komponen Owl.
    setup(){
        this.state = useState({
            quotations: {
                value: 10,
                percentage: 6,
            },
            period:90,
        })
        
        // 2. fungsi hook owl untuk mengakses ORM service dan disimpan `this.orm` 
        // agar bisa digunakan di fungsi lain 
        this.orm = useService("orm")

        // 4. Memanggil fungsi getQuotations sebelum komponen ditampilkan di layar.
        onWillStart(async ()=> {
            await this.getQuotations()
        })
    }

    // 3. digunakan untuk mengambil data dari server menggunakan ORM
    async getQuotations(){
        const data = await this.orm.searchCount("sale.order", [['state', 'in', ['sent', 'draft']]])
        this.state.quotations.value = data
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

