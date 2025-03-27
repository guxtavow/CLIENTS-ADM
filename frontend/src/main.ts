import { createApp } from 'vue'
import App from './App.vue'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'
import router from './router'
import { Button } from 'primevue'
import  Dialog  from 'primevue/dialog'

import 'primeicons/primeicons.css'


const app = createApp(App)
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: true,
            cssLayer: false,
        }
    }
 })
app.component('Dialog', Dialog)
app.component('Button', Button)
app.use(router)
app.mount('#app')
