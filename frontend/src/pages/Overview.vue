<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">


        <div class="col-xl-3 col-md-6">
          <stats-card>
            <div slot="header" class="icon-danger">
              <i class="nc-icon nc-vector text-danger"></i>
            </div>
            <div slot="content">
              <p class="card-category">Dispositivos Asociados</p>
              <h4 class="card-title">{{ dispositivosCount }}</h4>
            </div>
            <div slot="footer">
              <i class="fa fa-clock-o"></i> Actual
            </div>
          </stats-card>
        </div>

      </div>

      <div class="row">
        <div class="col-md-12">
          <div>
            <div class="form-group" v-if="devices[0]">
              <label for="deviceSelect">Selecciona un dispositivo para monitorear:</label>
              <select id="deviceSelect" v-model="selectedDevice" @change="fetchDeviceData" class="form-control">
                <option value="" disabled selected>Elige un dispositivo</option>
                <option v-for="device in devices" :key="device.id" :value="device.id">
                  {{ device.identificador }}
                </option>
              </select>
            </div>
            <div class="form-group" v-if="!devices[0]">
              <p>No tienes dispositivos asociados</p>

            </div>
            <button class="btn btn-warning mt-3" @click="startMonitoring" :disabled="!selectedDevice">
              <i class="fa fa-play"></i> Monitorear
            </button>
            <!-- Botones de exportación -->
            <button class="btn btn-primary mt-3" @click="exportToExcel" :disabled="!variables">
              <i class="fa fa-file-excel-o"></i> Exportar a Excel
            </button>
            <button class="btn btn-danger mt-3" @click="exportToPDF" :disabled="!variables">
              <i class="fa fa-file-pdf-o"></i> Exportar a PDF
            </button>

            <chart-card :chart-data="lineChart.data"
                        :chart-options="lineChart.options"
                        :responsive-options="lineChart.responsiveOptions"
                        ref="chart">
              <template slot="header">
                <h4 class="card-title">Monitoreo en tiempo real</h4>
                <p class="card-category">Últimas 24 horas</p>
              </template>
              <template slot="footer">
                <div v-if="variables" class="legend">
                  <div v-for="(color, variable) in legendColors" :key="variable">
                    <i :class="`fa fa-circle ${color}`"></i> {{ variable }}
                  </div>
                </div>
                <hr>
                <div class="stats">
                  <i class="fa fa-history"></i> Actualizado hace {{ lastUpdate }} minutos
                </div>
              </template>
            </chart-card>
          </div>
        </div>

        <!--        <div class="col-md-4">
                  <chart-card :chart-data="pieChart.data" chart-type="Pie">
                    <template slot="header">
                      <h4 class="card-title">Email Statistics</h4>
                      <p class="card-category">Last Campaign Performance</p>
                    </template>
                    <template slot="footer">
                      <div class="legend">
                        <i class="fa fa-circle text-info"></i> Open
                        <i class="fa fa-circle text-danger"></i> Bounce
                        <i class="fa fa-circle text-warning"></i> Unsubscribe
                      </div>
                      <hr>
                      <div class="stats">
                        <i class="fa fa-clock-o"></i> Campaign sent 2 days ago
                      </div>
                    </template>
                  </chart-card>
                </div>-->
      </div>

      <!--      <div class="row">
              <div class="col-md-6">
                <chart-card
                  :chart-data="barChart.data"
                  :chart-options="barChart.options"
                  :chart-responsive-options="barChart.responsiveOptions"
                  chart-type="Bar">
                  <template slot="header">
                    <h4 class="card-title">2014 Sales</h4>
                    <p class="card-category">All products including Taxes</p>
                  </template>
                  <template slot="footer">
                    <div class="legend">
                      <i class="fa fa-circle text-info"></i> Tesla Model S
                      <i class="fa fa-circle text-danger"></i> BMW 5 Series
                    </div>
                    <hr>
                    <div class="stats">
                      <i class="fa fa-check"></i> Data information certified
                    </div>
                  </template>
                </chart-card>
              </div>

      &lt;!&ndash;        <div class="col-md-6">
                <card>
                  <template slot="header">
                    <h5 class="title">Tasks</h5>
                    <p class="category">Backend development</p>
                  </template>
                  <l-table :data="tableData.data" :columns="tableData.columns">
                    <template slot="columns"></template>
                    <template slot-scope="{ row }">
                      <td>
                        <base-checkbox v-model="row.checked"></base-checkbox>
                      </td>
                      <td>{{ row.title }}</td>
                      <td class="td-actions text-right">
                        <button type="button" class="btn-simple btn btn-xs btn-info" v-tooltip.top-center="editTooltip">
                          <i class="fa fa-edit"></i>
                        </button>
                        <button type="button" class="btn-simple btn btn-xs btn-danger" v-tooltip.top-center="deleteTooltip">
                          <i class="fa fa-times"></i>
                        </button>
                      </td>
                    </template>
                  </l-table>
                  <div class="footer">
                    <hr>
                    <div class="stats">
                      <i class="fa fa-history"></i> Updated 3 minutes ago
                    </div>
                  </div>
                </card>
              </div>&ndash;&gt;
            </div>-->
    </div>
  </div>
</template>
<script>
import axios from 'axios';
import ChartCard from 'src/components/Cards/ChartCard.vue';
import StatsCard from 'src/components/Cards/StatsCard.vue';
import LTable from 'src/components/Table.vue';
import * as XLSX from  'xlsx';
import { saveAs } from 'file-saver';
import jsPDF from 'jspdf';
import Chartist from 'chartist';

export default {
  components: {
    LTable,
    ChartCard,
    StatsCard
  },
  data() {
    return {
      variableColors: {
        "Temperatura": "text-info",
        "Humedad Relativa": "text-danger",
        "Presión Atmosférica": "text-primary",
        "Velocidad del Viento": "text-secondary",
        "Dirección del Viento": "text-warning",
        "Precipitación": "text-success",
        "Radiación Solar": "text-light",
        "Temperatura del Punto de Rocío": "text-dark",
        "Evaporación": "text-muted",
        "Índice de Calor": "text-info",
        "Temperatura del Suelo": "text-danger",
        "Altitud": "text-primary"
      },
      variables: {},
      chartData: {}, // Datos del gráfico
      devices: [],  // Lista de dispositivos
      selectedDevice: null,

      // Dispositivo seleccionado
      dispositivosCount: 0,
      editTooltip: 'Edit Task',
      deleteTooltip: 'Remove',
      pieChart: {
        data: {
          labels: ['40%', '20%', '40%'],
          series: [40, 20, 40]
        }
      },
      lineChart: {
        data: {
          labels: [],
          series: [[]]
        },
        options: {
          low: 0,
          high: 1000,
          showArea: false,
          height: '245px',
          axisX: {
            showGrid: false
          },
          lineSmooth: true,
          showLine: true,
          showPoint: true,
          fullWidth: true,
          chartPadding: {
            right: 60
          }
        },
        responsiveOptions: [
          ['screen and (max-width: 640px)', {
            axisX: {
              labelInterpolationFnc(value) {
                return value[0];
              }
            }
          }]
        ]
      },
      lastUpdate: 0,
      barChart: {
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          series: [
            [542, 443, 320, 780, 553, 453, 326, 434, 568, 610, 756, 895],
            [412, 243, 280, 580, 453, 353, 300, 364, 368, 410, 636, 695]
          ]
        },
        options: {
          seriesBarDistance: 10,
          axisX: {
            showGrid: false
          },
          height: '245px'
        },
        responsiveOptions: [
          ['screen and (max-width: 640px)', {
            seriesBarDistance: 5,
            axisX: {
              labelInterpolationFnc(value) {
                return value[0];
              }
            }
          }]
        ]
      },
      tableData: {
        data: [
          {title: 'Sign contract for "What are conference organizers afraid of?"', checked: false},
          {title: 'Lines From Great Russian Literature? Or E-mails From My Boss?', checked: true},
          {
            title: 'Flooded: One year later, assessing what was lost and what was found when a ravaging rain swept through metro Detroit',
            checked: true
          },
          {title: 'Create 4 Invisible User Experiences you Never Knew About', checked: false},
          {title: 'Read "Following makes Medium better"', checked: false},
          {title: 'Unfollow 5 enemies from Twitter', checked: false}
        ]
      },
      intervalId: null // Para guardar el ID del intervalo
    };
  },
  created() {
    this.fetchDispositivosCount();
    this.fetchDevices(); // Cargar dispositivos al inicio

  },
  beforeDestroy() {
    clearInterval(this.intervalId); // Limpiar el intervalo al destruir el componente
  },
  methods: {
    async fetchDevices() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/apis/user/dispositivos/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.devices = response.data;

        // Asignar el dispositivo seleccionado desde los parámetros de la ruta
        if (this.$route.params.selectedDevice) {
          this.selectedDevice = this.$route.params.selectedDevice;
          await this.fetchDeviceData(); // Cargar los datos del dispositivo inmediatamente
        }

        console.log('Devices:', JSON.stringify(this.devices, null, 2));
      } catch (error) {
        console.error('Error fetching devices:', error);
      }
    },
    async fetchDeviceData() {
      console.log('Selected device in fetchDeviceData:', this.selectedDevice); // Verifica el valor
      if (!this.selectedDevice) return;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/apis/user/dispositivo/${this.selectedDevice}/data/`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        console.log('Device data:', response.data); // verifica en consola que halla datos
        if (response.data && response.data.data) {
          this.variables = response.data.data; // Accede al objeto de variables
          this.prepareColors(); // Llama a la función para preparar colores
        } else {
          console.error('No se encontraron datos válidos en la respuesta.');
        }
        this.updateChart(response.data); // Actualiza el gráfico con los nuevos datos
      } catch (error) {
        console.error('Error fetching device data:', error);
      }
    },
    prepareColors() {
      const presentVariables = Object.keys(this.variables);
      this.legendColors = {};

      presentVariables.forEach(variable => {
        if (this.variableColors[variable]) {
          this.legendColors[variable] = this.variableColors[variable];
        }
      });
    },
    updateChart(data) {
      console.log('Updating chart with data:', data);

      if (data.labels && data.data) {
        const lastTenLabels = data.labels.slice(-10); // Obtener los últimos 10 labels

        // Prepara las series para el gráfico
        const seriesData = Object.keys(data.data).map(variable => {
          return data.data[variable].values.slice(-10); // acceder a .values
        });

        // Combinar las series en un solo objeto para chartData
        this.lineChart.data = {
          labels: lastTenLabels,
          series: seriesData
        };

        console.log('Chart Data:', this.lineChart.data);

        // Si estás usando un ref para acceder al componente, puedes llamar a updateChart
        this.$refs.chart.updateChart();

        this.lastUpdate = 0;
      } else {
        console.error('Invalid data structure:', data);
      }
    },
    startMonitoring() {
      console.log('Starting monitoring for device:', this.selectedDevice); // Verifica el valor
      this.intervalId = setInterval(() => {
        console.log('Fetching device data...'); // Verifica si se llama a la función
        this.fetchDeviceData();
        this.lastUpdate += 1; // Incrementa el tiempo desde la última actualización
      }, 10000); // Actualizar cada 60 segundos
    },
    async fetchDispositivosCount() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/apis/user/dispositivos/count/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.dispositivosCount = response.data.count;
      } catch (error) {
        console.error('Error fetching dispositivos count:', error);
      }
    },
async exportToExcel() {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/apis/user/dispositivo/${this.selectedDevice}/data/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });

    const data = response.data.data; // Accede a los datos
    console.log('Data from API:', data); // Verifica la estructura de los datos

    // Verifica que data sea un objeto y no esté vacío
    if (typeof data !== 'object' || data === null || Object.keys(data).length === 0) {
      console.error('La respuesta no tiene la estructura esperada:', data);
      return;
    }

    const formattedData = this.formatDataForExport(data);

    const worksheet = XLSX.utils.json_to_sheet(formattedData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Datos Meteorológicos');
    const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
    saveAs(blob, 'datos_meteorologicos.xlsx');
  } catch (error) {
    console.error('Error exporting to Excel:', error);
  }
},

async exportToPDF() {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/apis/user/dispositivo/${this.selectedDevice}/data/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });

    const data = response.data.data; // Obtén los datos
    const formattedData = this.formatDataForExport(data);

    const doc = new jsPDF();
    doc.text('Informe de Variables Meteorológicas', 10, 10);
    let y = 20;

    formattedData.forEach(item => {
      for (const [key, value] of Object.entries(item)) {
        doc.text(`${key}: ${value}`, 10, y);
        y += 10; // Espaciado entre líneas
      }
      y += 10; // Espaciado entre dispositivos
    });

    doc.save('datos_meteorologicos.pdf');
  } catch (error) {
    console.error('Error exporting to PDF:', error);
  }
},

formatDataForExport(data) {
  const formattedData = [];

  // Obtiene las etiquetas de la primera variable
  const firstVariable = Object.values(data)[0];
  const labels = firstVariable.labels; // Asumimos que todas las variables tienen las mismas etiquetas

  // Itera sobre las etiquetas y crea un objeto para cada una
  labels.forEach((label, index) => {
    const row = { Label: label };

    for (const variable in data) {
      if (data[variable].values[index] !== undefined) {
        row[variable] = data[variable].values[index]; // Agrega el valor correspondiente
      } else {
        row[variable] = 'N/A'; // Manejo de valores nulos
      }
    }

    formattedData.push(row);
  });

  return formattedData;
}
  }
}
</script>
<style>
.text-info {
  color: #17a2b8; /* Color para Temperatura */
}

.text-danger {
  color: #dc3545; /* Color para Humedad */
}

</style>
