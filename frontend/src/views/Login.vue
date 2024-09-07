<template>
  <div class="container mt-5">
    <div class="card shadow-sm">
      <span id="loader" style="display: none;"
                  class="loader">                                             </span>
      <div class="card-body">
        <h2 class="card-title text-center mb-4">Iniciar Sesión</h2>
        <form @submit.prevent="login">
          <div class="mb-3">
            <label for="username" class="form-label">Nombre de Usuario</label>
            <input type="text" class="form-control" id="username" v-model="username" required>
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Contraseña</label>
            <input type="password" class="form-control" id="password" v-model="password" required>
          </div>
          <div v-if="errorMessage" class="alert alert-danger" role="alert">
            {{ errorMessage }}
          </div>
          <div class="d-grid gap-2 align-content-center">
            <button type="submit" class="btn btn-outline-dark">Iniciar Sesión</button>
            <p class="text-center mt-3">
              ¿No tienes una cuenta?
              <router-link to="/register">Registrate aquí</router-link>
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
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async login() {
  try {
    document.getElementById('loader').style.display = 'block'; // Muestra el indicador de carga
    const response = await axios.post('http://localhost:8000/api/token/', {
    //const response = await axios.post('http://localhost:8000/api-token-auth/', {
      username: this.username,
      password: this.password
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    localStorage.setItem('token', response.data.access);
    console.log('Token guardado:', localStorage.getItem('token'));
    document.getElementById('loader').style.display = 'none'; // Ocultar el indicador de carga
    this.$router.push('admin/table-list');
  } catch (error) {
    //console.error(error);
    if (error.response && error.response.data) {
      this.showMessage(error.response.data.error || 'Error en la autenticación', 'danger');
    } else {
      this.showMessage('Error en la autenticación', 'danger');
    }
  }
},
    showMessage(message, type) {
      this.errorMessage = message;
      setTimeout(() => {
        this.errorMessage = '';
      }, 5000);
    }
  }
}
</script>

<style scoped>
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
</style>
