import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/login/LoginView.vue'),
      meta: { public: true },
    },
    {
      path: '/',
      component: () => import('@/layouts/AdminLayout.vue'),
      redirect: '/dashboard',
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: () => import('@/views/dashboard/DashboardView.vue'),
        },
        {
          path: 'regions',
          name: 'Regions',
          component: () => import('@/views/region/RegionListView.vue'),
        },
        {
          path: 'users',
          name: 'Users',
          component: () => import('@/views/user/UserListView.vue'),
        },
        {
          path: 'activities',
          name: 'Activities',
          component: () => import('@/views/activity/ActivityListView.vue'),
        },
      ],
    },
  ],
});

router.beforeEach((to) => {
  const token = localStorage.getItem('admin_token');
  if (!to.meta.public && !token) {
    return { name: 'Login' };
  }
  return true;
});

export default router;
