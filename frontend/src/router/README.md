# 创建页面

## 在 src/pages 目录下创建一个以 .tsx 结尾的文件，将自动生成一个独立页面

| 组件路径                     | 对应路由     | 页面路径                                          |
| :--------------------------- | :----------- | :------------------------------------------------ |
| src/pages/index.tsx          | /            | localhost:3000/                                   |
| src/pages/foo.tsx            | /foo         | localhost:3000/foo                                |
| src/pages/foo/index.tsx      | /foo         | localhost:3000/foo                                |
| src/pages/foo/bar.tsx        | /foo/bar     | localhost:3000/foo/bar                            |
| src/pages/detail/[id].tsx    | /detail/:id  | localhost:3000/detail/100                         |
| src/pages/detail/\[[id]].tsx | /detail/:id? | localhost:3000/detail or localhost:3000/detail/99 |

## 示例

### 在 src/pages 目录下创建一个文件： src/pages/myTest/index.tsx 自动生成对应路由：/myTest

```
export default function MyTestPage() {
  return <div>My test page.</div>
}
```
