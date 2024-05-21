import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { fetchCsrfToken } from './services/cstfService';
const app = createApp(App)

app.use(router)

// app.mount('#app')

async function initApp() {
  await fetchCsrfToken();
  app.mount('#app');
}

initApp();