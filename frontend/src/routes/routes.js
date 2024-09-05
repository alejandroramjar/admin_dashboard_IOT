import axios from 'axios';

export async function isAuthenticated() {
  const token = localStorage.getItem('token');
  if (!token) {
    console.log('Token not found!');
    return false;
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/token/verify/', { token });
    console.log(response.status === 200);
    return response.status === 200;
  } catch (error) {
    console.error('Token inválido:', error);
    return false;
  }
}

import DashboardLayout from '../layout/DashboardLayout.vue';
import NotFound from '../pages/NotFoundPage.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Overview from 'src/pages/Overview.vue';
import UserProfile from 'src/pages/UserProfile.vue';
import TableList from 'src/pages/TableList.vue';
import Typography from 'src/pages/Typography.vue';
import Icons from 'src/pages/Icons.vue';
import Maps from 'src/pages/Maps.vue';
import Notifications from 'src/pages/Notifications.vue';
import Upgrade from 'src/pages/Upgrade.vue';

const routes = [
  {
    path: '/',
    component: DashboardLayout,
    redirect: '/admin/overview',
    beforeEnter: async (to, from, next) => {
      if (await isAuthenticated()) {
        console.log('Usuario autenticado');
        next();
      } else {
        console.log('Usuario no autenticado, redirigiendo a login');
        next('/login');
      }
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/admin',
    component: DashboardLayout,
    redirect: '/admin/overview',
    children: [
      {
        path: 'overview',
        name: 'Overview',
        component: Overview,
        beforeEnter: async (to, from, next) => {
          if (await isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'user',
        name: 'User',
        component: UserProfile,
        beforeEnter: async (to, from, next) => {
          if (await isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'table-list',
        name: 'Table List',
        component: TableList,
        beforeEnter: async (to, from, next) => {
          if (await isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'typography',
        name: 'Typography',
        component: Typography,
        beforeEnter: async (to, from, next) => {
          if (await isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'icons',
        name: 'Icons',
        component: Icons,
        beforeEnter: async (to, from, next) => {
          if (await isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'maps',
        name: 'Maps',
        component: Maps,
        beforeEnter: async (to, from, next) => {
          if (await isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: Notifications,
        beforeEnter: async (to, from, next) => {
          if (await isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'upgrade',
        name: 'Upgrade to PRO',
        component: Upgrade,
        beforeEnter: async (to, from, next) => {
          if (await isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      }
    ]
  },
  { path: '*', component: NotFound }
];

export default routes;
