/* @odoo-module */

import { useService } from "@web/core/utils/hooks"
import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
const { Component, onWillStart, useRef, onMounted } = owl


export class ChartRenderer extends Component {
    setup(){
        this.chartRef = useRef("chart")
        this.actionService = useService("action")
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js")
        });

        onMounted(()=>this.renderChart())
    }

    renderChart(){
        new Chart(
        this.chartRef.el,
            {
                type: this.props.type,
                data: this.props.config.data,
                options: {
                    // 18. configurasi onClick event
                    onClick: (e)=>{
                        const active = e.chart.getActiveElements()
                        if (active) {
                            const label = e.chart.data.labels[active[0].index]

                            let domain = this.props.config.domain ? this.props.config.domain : []

                            this.actionService.doAction({
                                type: "ir.actions.act_window",
                                name: this.props.title,
                                res_model: "sale.report",
                                domain: domain,
                                views: [
                                    [false, "list"],
                                    [false, "form"],
                                ]
                            })
                        }
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
                    scales: 'scales' in this.props.config ? this.props.config.scales : {},
                },
            }
        );
    }
}

ChartRenderer.template = "master_dashboard.ChartRenderer"
