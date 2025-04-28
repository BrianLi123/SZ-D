import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import axios from './plugins/axios'
import router from './router'

// 初始化Vue应用
const app = createApp(App)

// 安装插件
app.use(createPinia())
app.use(router)

// 全局配置
app.config.globalProperties.$http = axios

// 挂载应用
app.mount('#app')