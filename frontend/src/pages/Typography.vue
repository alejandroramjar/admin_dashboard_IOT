<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <card class="strpied-tabled-with-hover"
                body-classes="table-full-width table-responsive"
          >
            <template slot="header">
              <h4 class="card-title">Dispositivos registrados en el sistema</h4>
              <p class="card-category">Lista de dispositivos registrados en el sistema</p>
            </template>
            <l-table class="table-hover table-striped"
                     :columns="tableColumns"
                     :data="tableData">
            </l-table>
            <p v-if="!tableData[0]" class="error-message">No hay dispositivos en el sistema</p>
            <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          </card>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios'
import LTable from 'src/components/Table.vue'
import Card from 'src/components/Cards/Card.vue'

export default {
  components: {
    LTable,
    Card
  },
  data() {
    return {
      tableColumns: ['id','Protocolo', 'Nombre_Identificador', 'Variables', 'Descripción', 'Coordenadas'],
      tableData: [],
      errorMessage: null
    }
  },
  created() {
    this.fetchDispositivos()
  },
  methods: {
  async fetchDispositivos() {
    try {
      // Cambia la URL para obtener todos los dispositivos
      const response = await axios.get('http://127.0.0.1:8000/apis/api/dispositivos/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      this.tableData = response.data.map(dispositivo => ({
        id: dispositivo.id,
        Protocolo: dispositivo.protocolo,
        Nombre_Identificador: dispositivo.nombre_identificador,
        Variables: Array.isArray(dispositivo.variables_dict)
          ? dispositivo.variables_dict.join(', ')
          : JSON.stringify(dispositivo.variables_dict),
        Descripción: dispositivo.descripcion,
        Latitud: dispositivo.latitud,
        Longitud: dispositivo.longitud,
        Coordenadas: `${dispositivo.latitud}, ${dispositivo.longitud}` // Combinar latitud y longitud
      }))
      this.errorMessage = null; // Resetear mensaje de error
    } catch (error) {
      console.error('Error fetching dispositivos:', error)
      this.errorMessage = 'Error al cargar la lista de dispositivos.'
    }
  },

},

  }


</script>

<style>
</style>
