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
// digunakan untuk mendapatkan referensi ke suatu service dalam komponen Owl
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
            // memanggil pustaka manipulasi tanggal dari moment.min.js
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.30.1/moment.min.js")

            // memanggil data tanggal sebelum dirender ke halaman
            await this.getDates()

            // memanggil data quotation sebelum dirender ke halaman
            await this.getQuotations()

        })
    }

    // 3. digunakan untuk mengambil data dari server menggunakan ORM
    async getQuotations(){
        let domain = [['state', 'in', ['sent', 'draft']]]

        // jika semua state.period tidak lebih dari 0 maka akan menghitung semua record sale.order
        if (this.state.period > 0) {
            domain.push(['date_order', '>', this.state.date])
        }

        const data = await this.orm.searchCount("sale.order", domain)

        this.state.quotations.value = data 
    }

    // 5. digunakan untuk mendapatkan quotation dengan cara merubah tanggalnya terlebih dahulu
    async onChangePeriod(){
        await this.getDates()
        await this.getQuotations()
    } 

    // 6. digunakan untuk mendapatkan data tanggal hari ini yang dikurangi tanggal period
    async getDates(){
        this.state.date = moment().subtract(this.state.period, 'days').format('L')
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

