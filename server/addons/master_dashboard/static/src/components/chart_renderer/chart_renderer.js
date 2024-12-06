/* @odoo-module */

import { useService } from "@web/core/utils/hooks"
import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
const { Component, onWillStart, useRef, onMounted, useEffect, onWillUnmount } = owl


export class ChartRenderer extends Component {
    setup(){
        this.chartRef = useRef("chart")
        this.actionService = useService("action")
        onWillStart(async ()=>{
            //await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js")
            await loadJS("web/static/lib/Chart/Chart.js")
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.30.1/moment.min.js")
        });

        // 21. merubah chart saat state diubah
        // useEffect() adalah hook OWL yang dipanggil setiap kali terjadi perubahan pada state atau props dalam komponen
        useEffect(()=>{
            // creating a new chart
            this.renderChart()
        }, ()=>[this.props.config])  // memastikan renderChart hanya dipanggil ketika nilai config berubah

        onMounted(()=>this.renderChart())

        // 23. Hook ini sangat berguna untuk membersihkan sumber daya, seperti event listeners, interval, atau data lain yang perlu dilepaskan ketika komponen tidak lagi diperlukan.
        onWillUnmount(()=>{
            if (this.chart){
                this.chart.destroy()
            }
        })
    }

    renderChart(){
        // 22. sebelum membuat chart baru maka chart lama harus dihapus terlebih dahulu
        if (this.chart){
            this.chart.destroy()
        }
        this.chart = new Chart(
        this.chartRef.el,
            {
                type: this.props.type,
                data: this.props.config.data,
                options: {
                    // 18. configurasi onClick event
                    onClick: (e)=>{
                        const [activeElement] = this.chart.getElementsAtEventForMode(
                            e,
                            "nearest",
                            { intersect: true },
                            false
                        );
                        if (!activeElement) {
                            return;
                        }
                        const { datasetIndex, index } = activeElement;

                        //const active = e.chart.getActiveElements()
                        // Pastikan ada elemen aktif, ketika mouse diklik di luar chart
                        // maka akan menghasilkan object kosong atau tidak terjadi apa2
                        //if (active.length > 0) {
                            //const label = e.chart.data.labels[active[0].index]
                            //const dataset = e.chart.data.labels[active[0].datasetIndex].label

                            const label = this.chart.data.labels[index]
                            const dataset = this.chart.data.labels[datasetIndex].label

                            const { label_field, domain } = this.props.config

                            let new_domain = domain ? domain : []

                            // 19. jika diklik dengan label yg sama dengan active element
                            if (label_field){
                                // convert label_field ke tanggal
                                if (label_field.includes('date')){
                                    const timeStamp = Date.parse(label)
                                    const selected_month =  moment(timeStamp)
                                    const month_start = selected_month.format('L') // MM/DD/YYYY
                                    const month_end = selected_month.endOf('month').format('L')
                                    new_domain.push(['date', '>=', month_start], ['date', '<=', month_end])
                                }
                                else {
                                    new_domain.push([label_field, '=', label])
                                }
                            }

                            if (dataset === 'Quotations'){
                                new_domain.push(['state', 'in', ['draft', 'sent']])
                            }
                            if (dataset === 'Orders'){
                                new_domain.push(['state', 'in', ['sale']])
                            }

                            this.actionService.doAction({
                                type: "ir.actions.act_window",
                                name: this.props.title,
                                res_model: "sale.report",
                                domain: new_domain,
                                views: [
                                    [false, "list"],
                                    [false, "form"],
                                ]
                            })
                        //}
                    },
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        },
                        title: {
                            display: true,
                            text: this.props.title,
                            position: 'bottom',
                        },
                    },
                    // memindahkan skala kedua ke kanan. (partner orders chart)
                    scales: 'scales' in this.props.config ? this.props.config.scales : {},
                },
            },
        )
    }
}

ChartRenderer.template = "master_dashboard.ChartRenderer"
