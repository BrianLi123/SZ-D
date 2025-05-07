<h1 align="center">React Vite Template</h1>

<div align="center">中后台管理系统模板</div>

### ✨ 特性

- 🌈 采用 [Ant Design](https://ant.design/index-cn) 为您提供企业级中后台产品的交互语言和视觉风格。
- 💥 基于 [Vite](https://vitejs.dev/) 构建，可*[快速启动开发](https://vitejs.dev/guide/why.html)*。
- 🛡 使用 **TypeScript** 开发，提供完整的类型定义。
- 👍 强大的 [redux-toolkit](https://redux-toolkit.js.org/) 让您可以专注于应用所需的核心逻辑。
- 🌏 使用 [axios](https://www.axios-http.cn/) 搭配 [ahooks](https://ahooks.js.org/zh-CN/) 中的 `useRequest` 进行网络请求。
- 🔌 同时支持 **约定式路由** 和 **配置化路由**。
- 🖥 提供默认 `Layout` 组件。
- ☀ 支持 _亮/暗_ 主题，且提供多个主色调可任意切换。
- 🔨 antD 组件国际化和本地国际化。使用 [i18next-scanner](https://juejin.cn/post/7325132202970660873)自动化配置(扁平化、唯一 key、变量国际化)。
- ⚙️ 富文本编辑。使用 [wangeditor](https://www.wangeditor.com/)

### 📦 快速开始

#### 用pnpm启动项目
```
npm i pnpm -g

pnpm install

pnpm run dev
```

### 路由系统
实现了基于文件的路由系统，根据文件路径生成路由页面。
创建页面
在 src/pages 目录下创建一个以 .tsx 结尾的文件，将自动生成一个独立页面

查看文件router/index.tsx 
export const routes = generateRoutes(layoutConfigs, routeConfigs);

功能
1. 路由配置：每个文件路径对应一个路由页面配置
   ①lazy 路由；
   ②parsePath，根据文件路径解析路由path，并根据path设置config
   ②根据config.auth判断当前PageComponent是否用AuthRoute包裹
2. 布局配置，生成布局 type 和 component
3. generateRoutes：根据layoutConfigs和routeConfigs生成路由配置
    ①无布局的路由配置：根据routeConfigs过滤 无布局的路由
    ①有布局的路由配置：错误边界页面，布局组件，当前作为children
4. createBrowserRouter：根据路由配置创建路由器，404页面



