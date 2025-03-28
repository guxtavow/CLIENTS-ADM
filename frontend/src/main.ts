import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
// PrimeVue
import 'primeicons/primeicons.css';
import PrimeVue from 'primevue/config'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Checkbox from 'primevue/checkbox'
import Listbox from 'primevue/listbox'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'


const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue)
app.use(ToastService)
app.use(ConfirmationService)


// Register components
app.component('Listbox', Listbox)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Button', Button)
app.component('Dialog', Dialog)
app.component('InputText', InputText)
app.component('Checkbox', Checkbox)


app.mount('#app')
