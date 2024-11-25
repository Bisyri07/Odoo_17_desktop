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
            // memanggil data orders sebelum dirender ke halaman
            await this.getOrders()
        })
    }


    // 3. digunakan untuk mengambil data dari server menggunakan ORM
    async getQuotations(){
        // Memfilter pesanan dengan status sent atau draft.
        let domain = [['state', 'in', ['sent', 'draft']]]
        // jika semua state.period tidak lebih dari 0 maka akan menghitung semua record sale.order
        if (this.state.period > 0) {
            // filter tanggal
            domain.push(['date_order', '>', this.state.current_date])
        }
        const data = await this.orm.searchCount("sale.order", domain)
        this.state.quotations.value = data

        // Previous period
        let prev_domain = [['state', 'in', ['sent', 'draft']]]
        if (this.state.period > 0) {
            prev_domain.push(['date_order', '>', this.state.previous_date], ['date_order', '<=', this.state.current_date])
        }
        // menghitung previous quotation
        const prev_data = await this.orm.searchCount("sale.order", prev_domain)
        // menghitung persentase quotation dari sebelumnya
        const percentage = ((data - prev_data)/prev_data) * 100
        // menyimpan hasil persentase ke dalam state dengan 2 angka di belakang koma
        this.state.quotations.percentage = percentage.toFixed(2)
        // cek tanggal
        //console.log(this.state.previous_date, this.state.current_date)
    }


    // 7. menghitung jumlah order sama seperti quotation
    async getOrders(){
        let domain = [['state', 'in', ['sale', 'done']]]
        if (this.state.period > 0) {
            domain.push(['date_order', '>', this.state.current_date])
        }
        const data = await this.orm.searchCount("sale.order", domain)

        // Previous period
        let prev_domain = [['state', 'in', ['sale', 'done']]]
        if (this.state.period > 0) {
            prev_domain.push(['date_order', '>', this.state.previous_date], ['date_order', '<=', this.state.current_date])
        }

        // menghitung order
        const prev_data = await this.orm.searchCount("sale.order", prev_domain)
        const percentage = ((data - prev_data)/prev_data) * 100

        // 8. menghitung revenue
        const current_revenue = await this.orm.readGroup("sale.order", domain, ["amount_total:sum"], [])
        const prev_revenue = await this.orm.readGroup("sale.order", prev_domain, ["amount_total:sum"], [])
        const revenue_percentage = ((current_revenue[0].amount_total - prev_revenue[0].amount_total)/prev_revenue[0].amount_total)*100

        // 9. menghitung average order
        const current_avg = await this.orm.readGroup("sale.order", domain, ["amount_total:avg"], [])
        const prev_avg = await this.orm.readGroup("sale.order", prev_domain, ["amount_total:avg"], [])
        const avg_percentage = ((current_avg[0].amount_total - prev_avg[0].amount_total)/prev_avg[0].amount_total)*100

        this.state.orders = {
            value: data,
            percentage: percentage.toFixed(2),
            revenue: `Rp.${(current_revenue[0].amount_total/1000).toFixed(0)}K`,
            revenue_percentage: revenue_percentage.toFixed(2),
            average: `Rp.${(current_avg[0].amount_total/1000).toFixed(0)}K`,
            average_percentage: avg_percentage.toFixed(2),
        }
    }


    // 5. digunakan untuk mendapatkan quotation dengan cara merubah tanggalnya terlebih dahulu
    async onChangePeriod(){
        await this.getDates()
        await this.getQuotations()
        await this.getOrders()
    } 

    // 6. digunakan untuk mendapatkan data tanggal dikurangi tanggal period
    async getDates(){
        // Jika this.state.period = 90, maka tanggal dihitung menjadi 90 hari sebelum hari ini.
        this.state.current_date = moment().subtract(this.state.period, 'days').format('L')
        // Jika this.state.period = 90, maka tanggal dihitung menjadi 180 hari sebelum hari ini.
        this.state.previous_date = moment().subtract(this.state.period * 2, 'days').format('L')
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

