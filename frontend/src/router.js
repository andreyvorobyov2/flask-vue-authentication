import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/chat",
      redirect: "/",
      meta: { requiresAuth: true },
    },
    {
      path: "/",
      name: "chat",
      component: () => import("@/components/PageChat.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/components/PageLogin.vue"),
    },
    {
      path: "/signup",
      name: "signup",
      component: () => import("@/components/PageSignup.vue"),
    },
  ],
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const username = store.state.username;
    if (username) {
      next();
    } else {
      next("/login");
    }
  } else {
    next();
  }
});

export default router;
