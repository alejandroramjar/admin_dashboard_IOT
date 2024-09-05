import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        token: localStorage.getItem('token') || '',
        user: {},
    },
    mutations: {
        auth_success(state, token) {
            state.token = token;
        },
        auth_error(state) {
            state.token = '';
        },
        set_user(state, user) {
            state.user = user;
        },
    },
    actions: {
        async login({ commit }, user) {
            try {
                const response = await axios.post('http://localhost:8000/api/token/', user);
                const token = response.data.access;
                localStorage.setItem('token', token);
                axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
                commit('auth_success', token);
            } catch (error) {
                commit('auth_error');
                localStorage.removeItem('token');
            }
        },
        async getUser({ commit }) {
            try {
                const response = await axios.get('http://localhost:8000/api/user/');
                commit('set_user', response.data);
            } catch (error) {
                commit('auth_error');
            }
        },
    },
    getters: {
        isAuthenticated: state => !!state.token,
        user: state => state.user,
    },
});
