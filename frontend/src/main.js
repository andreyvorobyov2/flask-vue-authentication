import "./assets/main.css";
import router from "@/router";
import { createApp } from "vue";
import App from "./App.vue";
import store from "@/store";

import ToastPlugin from "vue-toast-notification";
//import 'vue-toast-notification/dist/theme-default.css';
import "vue-toast-notification/dist/theme-bootstrap.css";

const app = createApp(App);
// app.component("MemberList", MemberList);
app.use(router);
app.use(store);
app.use(ToastPlugin);
app.mount("#app");
