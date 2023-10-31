// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import IntroSection from '@/components/IntroSection.vue';
import MapLayout from '@/components/MapLayout.vue';

const routes = [
  {
    path: '/',
    name: 'IntroSection',
    component: IntroSection,
  },
  {
    path: '/MapLayout',
    name: 'MapLayout',
    component: MapLayout,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;





