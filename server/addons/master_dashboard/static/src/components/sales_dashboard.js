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
// digunakan untuk pengambilan warna dari skema warna default Odoo
import { getColor } from "@web/core/colors/colors"

// Component adalah library frontend untuk pembuatan UI di OWL 
const { Component, onWillStart, useRef, onMounted, useState } = owl

// export: Membuat kelas ini dapat diimpor di file lain
export class OwlSalesDashboard extends Component {

    // 14. Membuat chart interaktif mengambil data dari database
    // top products
    async getTopProducts(){
        // 15. tambahkan domain yg sama dari getOrders
        let domain = [['state', 'in', ['sale', 'done']]]
        if (this.state.period > 0) {
            domain.push(['date', '>', this.state.current_date])
        }
        // 16. lakukan agregasi dng menggunakan readGroup
        const data = await this.orm.readGroup(
            "sale.report",
            domain,
            ["product_tmpl_id", "price_total"],
            ["product_id"],
            { limit: 5, orderby: "price_total desc" }
        )
        // 17. configurasi data dan chart yg akan ditampilkan di halaman
        this.state.topProducts = {
            data: {
                labels: data.map(d => d.product_id[1]),
                datasets: [{
                    label: 'total',
                    data: data.map(d => d.price_total),
                    hoverOffset: 4,
                    backgroundColor: data.map((_, index) => getColor(index)),
                },
                {
                    label: 'Count',
                    data: data.map(d => d.product_id_count),
                    hoverOffset: 4,
                    backgroundColor: data.map((_, index) => getColor(index)),
                }]
            },
        }
    }

    // top sales people
    async getTopSalesPeople(){
        let domain = [['state', 'in', ['sale', 'done']]]
        if (this.state.period > 0) {
            domain.push(['date', '>', this.state.current_date])
        }

        const data = await this.orm.readGroup(
            "sale.report",
            domain,
            ["user_id", "price_total"],
            ["user_id"],
            { limit: 5, orderby: "price_total desc" }
        )

        this.state.topSalesPeople = {
            data: {
                labels: data.map(d => d.user_id[1]),
                datasets: [{
                    label: 'total',
                    data: data.map(d => d.price_total),
                    hoverOffset: 4,
                    backgroundColor: data.map((_, index) => getColor(index)),
                }]
            },
        }
    }

    // monthly sales
    async getMonthlySales(){
        let domain = [['state', 'in', ['draft', 'sent','sale', 'done']]]
        if (this.state.period > 0) {
            domain.push(['date', '>', this.state.current_date])
        }

        const data = await this.orm.readGroup(
            "sale.report",
            domain,
            ["date", "state", "price_total"],
            ["date", "state"],
            { orderby: "date desc" , lazy: false}
        )

        this.state.monthlySales = {
            data: {
                // yang akan diambil hanya data unique saja dgn menggunakan new Set()
                labels: [... new Set(data.map(d => d.date))],
                datasets: [{
                    label: 'Quotations',
                    data: data.filter(d => d.state == 'draft' || d.state == 'sent').map(d => d.price_total),
                    hoverOffset: 4,
                    backgroundColor: "red",
                },
                {
                    label: 'Count',
                    data: data.filter(d => ['sale', 'done'].includes(d.state)).map(d => d.price_total),
                    hoverOffset: 4,
                    backgroundColor: "#067dd1",
                }]
            },
        }
    }

    // partner orders
    async getPartnerOrders(){
        let domain = [['state', 'in', ['draft', 'sent','sale', 'done']]]
        if (this.state.period > 0) {
            domain.push(['date', '>', this.state.current_date])
        }

        const data = await this.orm.readGroup(
            "sale.report",
            domain,
            ["partner_id", "price_total", "product_uom_qty"],
            ["partner_id"],
            { orderby: "partner_id"}
        )

        this.state.partnerOrders = {
            data: {
                labels: data.map(d => d.partner_id[1]),
                datasets: [{
                    label: 'Total Amount',
                    data: data.map(d => d.price_total),
                    hoverOffset: 4,
                    backgroundColor: "#4bbfc9",
                    // Mengatur Sumbu Y untuk Data yang Berbeda
                    yAxisID: "Total",
                    // digunakan untuk menentukan urutan di mana dataset tersebut akan digambar.
                    // disini nilainya 1 yg berarti digambar setelah product_uom_qty dataset
                    order: 1,
                },
                {
                    label: 'ordered Qty',
                    data: data.map(d => d.product_uom_qty),
                    hoverOffset: 4,
                    backgroundColor: "#3238a8",
                    type: "line",
                    borderColor: "#3238a8",
                    yAxisID: "Qty",
                    order: 0,
                }]
            },
            // digunakan untuk menentukan pengaturan terkait sumbu (axis) pada grafik Anda
            scales:{
                Qty: {
                    position: 'right',
                }
            },
        }
    }

    // 1. Inisialisasi properti dan hook dalam komponen Owl.
    setup(){
        this.state = useState({
            quotations: {
                value: 10,
                percentage: 6,
            },
            period:90,

        })
        
        // 2. fungsi hook owl untuk mengakses ORM service dan disimpan `this.orm` agar bisa digunakan di fungsi lain
        this.orm = useService("orm");
        // 10. gunakan action service yg tersedia dari bawaan hook owl odoo
        this.actionService = useService("action");

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

            // 15. memanggil function / method chart
            await this.getTopProducts()
            await this.getTopSalesPeople()
            await this.getMonthlySales()
            await this.getPartnerOrders()
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
            revenue: `Rp${(current_revenue[0].amount_total/1000).toFixed(0)}K`,
            revenue_percentage: revenue_percentage.toFixed(2),
            average: `Rp${(current_avg[0].amount_total/1000).toFixed(0)}K`,
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

    // 11. mereferensikan tampilan untuk quotation KPI apabila diklik ke halaman yg ditentukan
    async viewQuotations(){
        let domain = [['state', 'in', ['sent', 'draft']]]
        if (this.state.period > 0) {
            domain.push(['date_order', '>', this.state.current_date])
        }

        // referensi view atau halaman yang dituju
        let list_view = await this.orm.searchRead(
            "ir.model.data",
            [['name', '=', 'view_quotation_tree_with_onboarding']],
            ['res_id']
        )

        this.actionService.doAction({
            type: 'ir.actions.act_window',
            name: 'Quotations',
            res_model: 'sale.order',
            domain: domain,
            views: [
                [list_view.length > 0 ? list_view[0].res_id : false, 'list'],
                [false, 'form'],
            ]
        })
    }

    // 12. mereferensikan tampilan untuk order KPI apabila diklik ke halaman yg ditentukan
    viewOrders(){
        let domain = [['state', 'in', ['sale', 'done']]]
        if (this.state.period > 0) {
            domain.push(['date_order', '>', this.state.current_date])
        }

        this.actionService.doAction({
            type: 'ir.actions.act_window',
            name: 'Quotations',
            res_model: 'sale.order',
            domain: domain,
            context: {group_by: ['date_order']},
            views: [
                [false, 'list'],
                [false, 'form'],
            ]
        })
    }

    // 13. mereferensikan tampilan untuk revenue KPI & rata2nya apabila diklik ke halaman yg ditentukan
    viewRevenues(){
        let domain = [['state', 'in', ['sale', 'done']]]
        if (this.state.period > 0) {
            domain.push(['date_order', '>', this.state.current_date])
        }

        this.actionService.doAction({
            type: 'ir.actions.act_window',
            name: 'Quotations',
            res_model: 'sale.order',
            domain: domain,
            context: {group_by: ['date_order']},
            views: [
                [false, 'graph'],
                [false, 'form'],
            ]
        })
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

