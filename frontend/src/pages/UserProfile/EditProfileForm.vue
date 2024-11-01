<template>
  <card>
    <h4 slot="header" class="card-title">Edit Profile</h4>
    <form @submit.prevent="updateProfile">
      <div class="row">
        <div class="col-md-6">
          <base-input type="text"
                      label="Carnet de Identidad"
                      placeholder="Carnet de Identidad"
                      v-model="user.carnet_identidad">
          </base-input>
        </div>
        <div class="col-md-6">
          <base-input type="text"
                      label="Teléfono"
                      placeholder="Teléfono"
                      v-model="user.phone">
          </base-input>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6">
          <base-input type="text"
                      label="First Name"
                      placeholder="First Name"
                      v-model="user.first_name">
          </base-input>
        </div>
        <div class="col-md-6">
          <base-input type="text"
                      label="Last Name"
                      placeholder="Last Name"
                      v-model="user.last_name">
          </base-input>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6">
          <base-input type="email"
                      label="Correo"
                      placeholder="Correo"
                      v-model="user.email">
          </base-input>
        </div>
        <div class="col-md-6">
          <base-input type="text"
                      label="Nombre Usuario"
                      placeholder="Nombre Usuario"
                      v-model="user.username">
          </base-input>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <label for="provincia" class="form-label">Provincia</label>
          <select class="form-control" id="provincia" v-model="provincia" @change="fetchMunicipios">
            <option selected value="">Seleccione una provincia</option>
            <option v-for="prov in provincias" :key="prov.id" :value="prov.id">{{ prov.nombre }}</option>
          </select>
        </div>
        <div v-if="provincia===''" class="col">
          <label for="municipio" class="form-label">Municipio</label>
          <select class="form-control" id="municipio" v-model="user.municipio" required>
            <option  :value="user.municipio">{{ municipio.nombre }}</option>
          </select>
        </div>
        <div v-else class="col">
          <label for="municipio" class="form-label">Municipio</label>
          <select class="form-control" id="municipio" v-model="user.municipio" required>
            <option v-for="mun in municipios" :key="mun.id" :value="mun.id">{{ mun.nombre }}</option>
          </select>
        </div>
      </div>

      <div class="text-center">
        <button type="submit" class="btn btn-info btn-fill float-right" :disabled="loading">
          Update Profile
        </button>
      </div>
      <div class="clearfix"></div>
    </form>
  </card>
</template>

<script>
import Card from 'src/components/Cards/Card.vue';
import axios from 'axios';

export default {
  components: {
    Card
  },
  data() {
    return {
      user: {
        username: '',
        carnet_identidad: '',
        phone: '',
        first_name: '',
        last_name: '',
        email: '',
        municipio: '',
      },
      municipio:'',
      provincia: '',
      provincias: [],
      municipios: [],
      loading: false
    };
  },
  created() {
    this.getUser();
    this.fetchProvincias();
        this.getMunicipio();
  },
  methods: {
    async getUser() {
      try {
        const response = await axios.get('http://localhost:8000/apis/userD/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.user = response.data;
        console.log(this.user);

        // Cargar municipios si se tiene una provincia
        if (this.user.provincia) {
          await this.fetchMunicipios();
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    async getMunicipio() {
      try {
        const response = await axios.get('http://localhost:8000/apis/userD/municipio', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.municipio = response.data;
        console.log(this.municipio);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    async fetchProvincias() {
      try {
        const response = await axios.get('http://localhost:8000/apis/provincias/');
        this.provincias = response.data;
      } catch (error) {
        console.error('Error fetching provincias:', error);
      }
    },
    async fetchMunicipios() {
      try {
        const response = await axios.get(`http://localhost:8000/apis/municipios/?provincia=${this.provincia}`);
        this.municipios = response.data;
      } catch (error) {
        console.error('Error fetching municipios:', error);
      }
    },
    async updateProfile() {
      this.loading = true; // Indica que la carga está en progreso
      try {
        await axios.put('http://localhost:8000/apis/userD/', this.user, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        alert('Profile updated successfully!');
      } catch (error) {
        console.error('Error updating profile:', error);
        alert('Failed to update profile. Please try again.');
      } finally {
        this.loading = false; // Restablece el estado de carga
      }
    }
  }
};
</script>

<style>
/* Estilos personalizados aquí */
</style>
