/* @odoo-module */
// anotasi untuk memberi tahu Odoo bahwa file ini adalah modul JavaScript Odoo

// mengimpor registry dari modul inti Odoo
import { registry } from "@web/core/registry"
// import KpiCard dari kpi_card.js
import { KpiCard } from "./kpi_card/kpi_card"
// Fungsi ini digunakan untuk memuat file JavaScript secara dinamis pada runtime
import { loadJS } from "@web/core/assets"

// Component adalah library frontend untuk pembuatan UI di OWL 
const { Component, onWillStart, useRef, onMounted } = owl

// export: Membuat kelas ini dapat diimpor di file lain
export class OwlSalesDashboard extends Component {
    setup(){
        // Referensi DOM elemen untuk chart
        this.chartRef = useRef("chart");
        // Memuat pustaka Chart.js sebelum komponen dimount
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js")
        });

        onMounted(()=>{
            const data = [
            { year: 2010, count: 10 },
            { year: 2011, count: 20 },
            { year: 2012, count: 15 },
            { year: 2013, count: 25 },
            { year: 2014, count: 22 },
            { year: 2015, count: 30 },
            { year: 2016, count: 28 },
          ];

          new Chart(
            this.chartRef.el,
            {
              type: 'bar',
              data: {
                labels: data.map(row => row.year),
                datasets: [
                  {
                    label: 'Acquisitions by year',
                    data: data.map(row => row.count)
                  }
                ]
              }
            }
          );
        })
    }
}

// Baris ini menghubungkan komponen OwlSalesDashboard dengan template XML-nya. ID template yang didefinisikan di file XML
OwlSalesDashboard.template = "master_dashboard.OwlSalesDashboard" 
OwlSalesDashboard.components = { KpiCard }


// registry.category("actions") => mengakses kategori actions dalam registry
// .add("master_dashboard.sales_dashboard", OwlSalesDashboard) menambahkan komponen OwlSalesDashboard 
// ke dalam kategori aksi dengan nama "master_dashboard.sales_dashboard"
registry.category("actions").add("master_dashboard.sales_dashboard", OwlSalesDashboard)

