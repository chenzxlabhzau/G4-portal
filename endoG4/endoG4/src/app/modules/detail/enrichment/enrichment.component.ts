import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {DetailApiService} from "../detail-api.service";
import * as Highcharts from 'highcharts';
import HC_more from 'highcharts/highcharts-more';
import HC_coloraxis from 'highcharts/modules/coloraxis';
HC_more(Highcharts);

@Component({
  selector: 'app-enrichment',
  templateUrl: './enrichment.component.html',
  styleUrls: ['./enrichment.component.css']
})
export class EnrichmentComponent implements OnInit {
  Highcharts: typeof Highcharts = Highcharts;
  KEGG: Highcharts.Options;
  GO: Highcharts.Options;
  sample_num:number
  constructor(private route: ActivatedRoute, private DataApiService: DetailApiService) {
    HC_coloraxis(Highcharts)
  }

  ngOnInit(): void {
    this.route.params.subscribe((params) => {
    this.DataApiService.findEnrichment(params.g_id).subscribe((res)=> {
      this.sample_num = res.total_tf
    this.KEGG = this.getBubbleChartOptions(res.kegg, "KEGG Enrichmet Analysis");
    this.GO = this.getBubbleChartOptions(res.go,"GO Enrichmet Analysis");
    });
  });
  }

  private getBubbleChartOptions(data: any[], tt:string): Highcharts.Options {
    const self = this;
  const transformedData = data.map((item, index) => ({
    x: item.GeneRatio, // 添加了 x
    y: index,
    z: Number(item.count), // 添加了 z，记住将字符串转换为数值
    pValue: item.padjust, // 保留了原始的 p 值
    name: item.pathway
  }));
  const pathway = transformedData.map(item => item.name)
  console.log(transformedData.map(item => item.name))
    // @ts-ignore
    const chartOptions: Highcharts.Options = {
      chart: {
            type: 'bubble',
            plotBorderWidth: 0,
          },
      title: {
        text: tt,
        x:20
      },
      xAxis: {
        lineWidth: 1,
        gridLineWidth: 0,
        tickWidth: 1,
        tickLength :5,
        title: {
          text: 'GeneRatio',
        },
      },
    colorAxis: {
        showInLegend: false,
      stops: [
        [0, '#0000ff'], // 蓝色对应 -log(p) = 0
        [0.65, '#ff8080'], // 中间色，对应 -log(p) = 1.3
        [1, '#800000'] // 深红色对应 -log(p) = 2
      ],
      min: 0,
      max: 2,
      startOnTick: false,
      endOnTick: false,
      labels: {
        formatter: function () {
            const pValue = Math.pow(10, -this.value);
            return Highcharts.numberFormat(pValue, 1); // Format p-value with precision
        }
      }
    },
        yAxis: {
        tickmarkPlacement :"on",
         categories: pathway,
          lineWidth: 1,
          gridLineWidth: 0,
          tickWidth: 1,
          tickLength :5,
          min: 0, // Y 轴的最小值
          max: transformedData.length - 1, // Y 轴的最大值
          title: null,

          // labels: {
          // useHTML: true,
          //     formatter: function() {
          //       console.log(this.value)
          //       // @ts-ignore
          //       return String(self.insertLineBreaks(this.value, 40));
          //       return "asf"
          //     }, // 注意这里，你需要将类的上下文（this）绑定到函数中
          // },
        },
        tooltip: { // 新添加的属性
          useHTML: true,
          headerFormat: '<table>',
          pointFormatter: function() {
              // @ts-ignore
            const p = Math.pow(10, -this.pValue);
              // @ts-ignore
            return `
                  <tr><th>Pathway:</th><td>${self.insertLineBreaks(pathway[this.y],40)}</td></tr>
                  <tr><th>Gene Ratio:</th><td>${this.x.toFixed(2)}</td></tr>
                  <tr><th>Count:</th><td>${this['z']}</td></tr>
                  <tr><th>P-adjust:</th><td>${p.toFixed(2)}</td></tr>
              `;
          },
          footerFormat: '</table>',
          followPointer: true
        },
      series: [{
        type: 'bubble',
        colorKey: 'pValue',
        data: transformedData,
        name: 'Enrichment',
        marker: {
          radius: 2,
        },

        showInLegend: false, // 添加这行代码
      }],
      credits: {
        enabled: false,
      },
        };
        return chartOptions;
  }

   insertLineBreaks(s: string, maxLength: number): string {
    if (s.length > maxLength) {
        let spaceIndex = s.lastIndexOf(' ', maxLength);
        if (spaceIndex === -1) {
            spaceIndex = maxLength;
        }
        return s.substring(0, spaceIndex) + '<br />' + this.insertLineBreaks(s.substring(spaceIndex + 1), maxLength);
    } else {
        return s;
    }
}

}
