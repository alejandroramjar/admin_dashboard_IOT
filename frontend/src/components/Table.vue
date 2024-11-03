<template>
  <table class="table">
    <thead>
      <tr>
        <th v-for="column in columns" :key="column">{{ column }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in data" :key="index">
        <td v-for="column in columns" :key="column" v-if="hasValue(item, column)">
          {{ itemValue(item, column) }}
        </td>
        <td>
          <router-link :to="{ name: 'Maps', params: { lat: item.latitud, lng: item.longitud } }"
                       class="btn btn-primary">Ver Ubicación</router-link>
        </td>
        <td>
          <router-link v-if="!checkifadmin" :to="{ name: 'Overview', params: { selectedDevice: item.id } }"
                       class="btn btn-outline-warning">Monitorear</router-link>
        </td>
        <td>
          <div v-if="checkifadmin" @click="goToEditPage(item.id)" class="btn btn-outline-warning">Editar
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      activeNotifications: false,
      checkifadmin: false,
    };
  },
  name: 'l-table',
  props: {
    columns: Array,
    data: Array,
  },
  async created() {
    const token = localStorage.getItem('token');
    this.checkifadmin = await this.checkIfAdmin(token);
  },
  methods: {
    async goToEditPage(id) {

      window.location.href = `http://localhost:8000/admin/accounts/dispositivo/${id}/change/`;
    },

    async checkIfAdmin(token) {
      try {
        const response = await axios.get('http://localhost:8000/apis/user/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        return response.data.is_admin;
      } catch (error) {
        console.error('Error al verificar el rol del usuario:', error);
        return false;
      }
    },
    hasValue(item, column) {
      return item[column] !== undefined;
    },
    itemValue(item, column) {
      return item[column];
    }
  }
};
</script>

<style>
/* Tu estilo aquí */
</style>
