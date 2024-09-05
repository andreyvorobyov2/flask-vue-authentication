import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import router from './router';
import ToastService from 'primevue/toastservice';
import Vuex from 'vuex';
import store from './store.js';
import 'primeicons/primeicons.css'

const app = createApp(App);

app.use(PrimeVue, {theme: {preset: Aura}});
app.use(router);
app.use(ToastService);
app.use(store)
app.use(Vuex)

app.mount('#app');
