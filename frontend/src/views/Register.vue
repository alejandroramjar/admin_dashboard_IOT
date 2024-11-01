<template>
  <div class="container mt-5">
    <div class="card shadow-sm">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">Registrarse</h2>
        <form @submit.prevent="register">
          <div class="row mb-3">
            <div class="col">
              <label for="first_name" class="form-label">Nombre(s)</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fa fa-user"></i>
                </span>
                <input type="text" class="form-control" id="first_name" v-model="first_name" required>
              </div>
            </div>
            <div class="col">
              <label for="last_name" class="form-label">Apellidos</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fa fa-user"></i>
                </span>
                <input type="text" class="form-control" id="last_name" v-model="last_name" required>
              </div>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col">
              <label for="username" class="form-label">Nombre de Usuario</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fa fa-at"></i>
                </span>
                <input type="text" class="form-control" id="username" v-model="username" required>
              </div>
            </div>
            <div class="col">
              <label for="email" class="form-label">Correo Electrónico</label>
              <div class="input-group mb-3">
                <span class="input-group-text">
                  <i class="fa fa-envelope"></i>
                </span>
                <input type="email" class="form-control" id="email" v-model="email" required>
              </div>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col-5">
              <label for="carnet_identidad" class="form-label">Carnet de Identidad</label>
              <input type="number" class="form-control" id="carnet_identidad" v-model="carnet_identidad" required>
            </div>
            <div class="col-7">
              <label for="phone" class="form-label">Teléfono</label>
              <div class="input-group mb-3">
                <span class="input-group-text">
                  <i class="fa fa-phone"></i> +53
                </span>
                <input type="number" class="form-control" id="phone" v-model="phone" required>
              </div>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col">
              <label for="provincia" class="form-label">Provincia</label>
              <select class="form-control" id="provincia" v-model="provincia" @change="fetchMunicipios" required>
                <option v-for="prov in provincias" :key="prov.id" :value="prov.id" style="color: #0e0e0e">{{ prov.nombre }}</option>
              </select>
            </div>
            <div class="col">
              <label for="municipio" class="form-label">Municipio</label>
              <select class="form-control" id="municipio" v-model="municipio" required>
                <option v-for="mun in municipios" :key="mun.id" :value="mun.id">{{ mun.nombre }}</option>
              </select>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col">
              <label for="password" class="form-label">Contraseña</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fa fa-lock"></i>
                </span>
                <input type="password" class="form-control" id="password" v-model="password" required>
              </div>
            </div>
            <div class="col">
              <label for="password2" class="form-label">Confirmar Contraseña</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fa fa-lock"></i>
                </span>
                <input type="password" class="form-control" id="password2" v-model="password2" required>
              </div>
            </div>
          </div>
          <div class="d-grid gap-2">
            <button type="submit" @click="spiner()" class="btn btn-outline-dark">
              <div v-if="loading" class="spinner-border spinner-border-sm"></div>
              Registrarse
            </button>
            <p class="text-center mt-3">
              ¿Ya tienes una cuenta?
              <router-link to="/login">Inicia sesión aquí</router-link>
            </p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      first_name: '',
      last_name: '',
      password: '',
      password2: '',
      email: '',
      carnet_identidad: '',
      phone: '',
      provincia: '',
      municipio: '',
      provincias: [],
      municipios: [],
      loading: false
    };
  },
  created() {
    this.fetchProvincias();
  },
  methods: {
    async fetchProvincias() {
      console.log(this.provincias)
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
    async register() {
      if (this.password !== this.password2) {
        alert("Las contraseñas no coinciden");
        return;
      }
      else if (!/^\d{8}$/.test(this.phone)) {
        alert("El teléfono debe tener exactamente 8 dígitos.");
        return;
      }
      else if (!/^\d{11}$/.test(this.carnet_identidad)) {
        alert("El carnet de identidad debe tener exactamente 11 dígitos.");
        return;
      }

      const formData = {
        username: this.username,
        first_name: this.first_name,
        last_name: this.last_name,
        password: this.password,
        email: this.email,
        carnet_identidad: this.carnet_identidad,
        phone: this.phone,
        provincia: this.provincia,
        municipio: this.municipio,
      };

      try {
        this.loading = true;
        console.log(formData);
        const response = await axios.post('http://localhost:8000/apis/register/', formData);
        console.log(response);
        this.loading = false;

        alert('Registro exitoso. El admin tiene 72 hrs para activar tu cuenta.');
        this.$router.push('/login');
      } catch (error) {
        console.error(error);
        this.loading = false;
        alert(`Error en el registro: ${error.response.data.detail || error.message}`);
      }
    }
  }
}
</script>


<style scoped>
.loader {
  /*position: absolute;*/
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  /*position: relative;*/
  animation: rotate 1s linear infinite;
}

.loader::before, .loader::after {
  content: "";
  box-sizing: border-box;
  position: absolute;
  inset: 0px;
  border-radius: 50%;
  border: 5px solid #FFF;
  animation: prixClipFix 2s linear infinite;
}

.loader::after {
  border-color: #FF3D00;
  animation: prixClipFix 2s linear infinite, rotate 0.5s linear infinite reverse;
  inset: 6px;
}

.container {
  max-width: 400px;
}

.card {
  border-radius: 10px;
}

.card-title {
  font-weight: bold;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}

select {
  color: #000; /* Color del texto */
  background-color: #fff; /* Color de fondo */
  border: 1px solid #ced4da; /* Borde estándar */
}

</style>
