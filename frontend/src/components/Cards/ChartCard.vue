<template>
  <div class="card">
    <div class="card-header" v-if="$slots.header">
      <slot name="header"></slot>
    </div>
    <div class="card-body">
      <div :id="chartId" class="ct-chart"></div>
    </div>
    <div class="card-footer" v-if="$slots.footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>
<script>
  import Card from './Card.vue'

  export default {
    name: 'chart-card',
    components: {
      Card
    },
    props: {
      chartType: {
        type: String,
        default: 'Line' // Line | Pie | Bar
      },
      chartOptions: {
        type: Object,
        default: () => {
          return {}
        }
      },
      chartData: {
        type: Object,
        default: () => {
          return {
            labels: [],
            series: []
          }
        }
      },
      responsiveOptions: [Object, Array]
    },
    data () {
      return {
        chartId: 'no-id',
        $Chartist: null,
        chart: null,
         isChartInitialized: false // Agrega esta variable
      }
    },
    methods: {
      /***
       * Initializes the chart by merging the chart options sent via props and the default chart options
       */
      initChart () {

       var chartIdQuery = `#${this.chartId}`
        this.chart = this.$Chartist[this.chartType](chartIdQuery, this.chartData, this.chartOptions, this.responsiveOptions)
        this.$emit('initialized', this.chart)
        if (this.chartType === 'Line') {
          this.animateLineChart()
        }
        if (this.chartType === 'Bar') {
          this.animateBarChart()
        }
        if (!this.isChartInitialized) {
        this.renderChart(); // Llama a la función para renderizar el gráfico
          this.isChartInitialized = true; // Marca como inicializado
    }
      },
      renderChart() {
    const chartIdQuery = `#${this.chartId}`;
    this.chart = this.$Chartist[this.chartType](chartIdQuery, this.chartData, this.chartOptions, this.responsiveOptions);
    this.$emit('initialized', this.chart);
    if (this.chartType === 'Line') {
      this.animateLineChart();
    }
    if (this.chartType === 'Bar') {
      this.animateBarChart();
    }
  },
      /***
   * Actualiza el gráfico con los nuevos datos
   */

  updateChart() {
    if (this.chart) {
      this.chart.update(this.chartData); // Actualiza el gráfico con los nuevos datos
    }
    if (this.$refs.chart) {
        new Chartist.Line(
          this.$refs.chart,
          this.chartData,
          {
            ...this.chartOptions,
            updateOnScrool: false // Evita actualizaciones durante el scroll
          }
        );
      }


  },
      /***
       * Assigns a random id to the chart
       */
      updateChartId () {
        const currentTime = new Date().getTime().toString()
        const randomInt = this.getRandomInt(0, currentTime)
        this.chartId = `div_${randomInt}`
      },
      getRandomInt (min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min
      },
      animateLineChart () {
        let seq = 0
        let durations = 500
        let delays = 80
        this.chart.on('draw', (data) => {
          if (data.type === 'line' || data.type === 'area') {
            data.element.animate({
              d: {
                begin: 600,
                dur: 700,
                from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
                to: data.path.clone().stringify(),
                easing: this.$Chartist.Svg.Easing.easeOutQuint
              }
            })
          } else if (data.type === 'point') {
            seq++
            data.element.animate({
              opacity: {
                begin: seq * delays,
                dur: durations,
                from: 0,
                to: 1,
                easing: 'ease'
              }
            })
          }
        })
        seq = 0
      },
      animateBarChart () {
        let seq = 0
        let durations = 500
        let delays = 80
        this.chart.on('draw', (data) => {
          if (data.type === 'bar') {
            seq++
            data.element.animate({
              opacity: {
                begin: seq * delays,
                dur: durations,
                from: 0,
                to: 1,
                easing: 'ease'
              }
            })
          }
        })
      }
    },
    async mounted () {
      this.updateChartId()
      const Chartist = await import('chartist')
      this.$Chartist = Chartist.default || Chartist
      this.initChart()
    }
  }
</script>
<style>

</style>
