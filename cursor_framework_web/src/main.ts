import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './styles/main.css'
import './styles/templates.css'

const app = createApp(App)
app.use(router)
app.mount('#app')