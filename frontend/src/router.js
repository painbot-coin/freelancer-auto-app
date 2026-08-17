import { createRouter, createWebHistory } from "vue-router";
import JobsView from "./views/JobsView.vue";
import ProfileView from "./views/ProfileView.vue";
import ChatView from "./views/ChatView.vue";
import DashboardView from "./views/DashboardView.vue";

const routes = [
  { path: "/", redirect: "/dashboard" },
  { path: "/dashboard", component: DashboardView },
  { path: "/jobs", component: JobsView },
  { path: "/profile", component: ProfileView },
  { path: "/chat", component: ChatView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

