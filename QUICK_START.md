# ⚡ 30秒快速开始指南

## 🎯 3 步启动

### 1️⃣ 启动前端 (当前终端)
```bash
cd /Users/yyz/Desktop/熔盐管理文件上传工具/tauri-app
npm run dev
```
等待输出: `➜  Local:   http://localhost:5173/`

### 2️⃣ 编译后端 (新终端)
```bash
cd /Users/yyz/Desktop/熔盐管理文件上传工具/tauri-app/src-tauri
cargo build
```
等待输出: `Finished`

### 3️⃣ 打开浏览器
访问 `http://localhost:5173`

---

## ✨ 你应该看到

```
🔐 熔盐管理文件上传工具

[API 服务器] http://localhost:3000
[用户名]     
[密码]       
[登录] 按钮
```

---

## 💡 常用命令

| 命令 | 说明 |
|------|------|
| `npm run dev` | 启动前端开发服务器 |
| `cargo build` | 编译 Rust 后端 |
| `cargo clean && cargo build` | 清理缓存后重新编译 |
| `npm run tauri:build` | 构建可执行文件 |

---

## 📚 更多文档

- **完整说明** → 阅读 `INDEX.md`
- **项目总结** → 阅读 `PROJECT_SUMMARY.md`
- **技术细节** → 阅读 `docs/Tauri迁移方案.md`

---

## 🆘 常见问题

❓ **前端不显示？**
- 检查 `npm run dev` 是否在运行
- 检查端口 5173 是否被占用

❓ **cargo build 失败？**
- 运行 `cargo clean` 后重试
- 检查网络连接

---

**现在就开始吧！** 🚀

