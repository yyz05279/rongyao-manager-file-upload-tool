# ✅ Tauri Invoke 错误修复指南

**错误信息**: `Cannot read properties of undefined (reading 'invoke')`  
**日期**: 2025-10-24  
**状态**: 🟢 已修复

---

## 🔍 问题原因

### 错误分析

当您看到这个错误时，通常是因为：

1. ❌ **使用了错误的启动命令**

   - 错误: `npm run dev` (只启动 Vite 前端服务器)
   - 正确: `npm run tauri:dev` (启动完整的 Tauri 应用)

2. ❌ **Tauri 后端未运行**
   - 前端代码尝试调用 `invoke()` 函数
   - 但 Tauri 后端没有运行，`window.__TAURI__` 未定义
   - 导致 `invoke` 函数不可用

---

## ✅ 解决方案

### 方法 1: 使用正确的启动命令（推荐）

```bash
# 1. 进入 Tauri 项目目录
cd tauri-app

# 2. 使用正确的命令启动
npm run tauri:dev

# ✅ 这会同时启动：
#   - Rust 后端服务器
#   - React 前端开发服务器
#   - Tauri 应用窗口
```

### 方法 2: 使用启动脚本（更简单）

```bash
# 在项目根目录运行
./START_TAURI_DEV.sh
```

---

## 🔧 已实施的修复

### 1. 添加了 `tauri:dev` 脚本

**文件**: `tauri-app/package.json`

```json
{
  "scripts": {
    "dev": "vite", // ❌ 只启动前端
    "tauri:dev": "tauri dev", // ✅ 启动完整应用（新增）
    "tauri:build": "tauri build"
  }
}
```

### 2. 添加了环境检查

**文件**: `tauri-app/src/services/api.js`

```javascript
// 检查 Tauri 环境
const checkTauriEnvironment = () => {
  if (typeof window.__TAURI__ === "undefined") {
    throw new Error(
      "❌ Tauri 环境未初始化！\n\n" +
        "请使用以下命令启动应用：\n" +
        "cd tauri-app\n" +
        "npm run tauri:dev\n\n" +
        "不要使用 npm run dev（这只会启动前端服务器）"
    );
  }
};

// 包装 invoke 函数，添加环境检查
const safeInvoke = async (cmd, args) => {
  checkTauriEnvironment();
  try {
    return await invoke(cmd, args);
  } catch (error) {
    console.error(`Tauri invoke error [${cmd}]:`, error);
    throw error;
  }
};
```

**改进点**:

- ✅ 在调用 `invoke` 前检查 Tauri 环境
- ✅ 提供清晰的错误提示
- ✅ 添加详细的日志输出

---

## 📋 启动步骤检查清单

在启动应用前，请确认：

### 前置条件

- [ ] 已安装 Rust (运行 `rustc --version` 检查)
- [ ] 已安装 Node.js (运行 `node --version` 检查)
- [ ] 已安装 Tauri CLI (运行 `npm list -g @tauri-apps/cli` 检查)
- [ ] 已安装项目依赖 (在 `tauri-app` 目录运行 `npm install`)

### 启动应用

```bash
# 方式 1: 使用 npm 脚本
cd tauri-app
npm run tauri:dev

# 方式 2: 使用启动脚本
cd /Users/yyz/Desktop/熔盐管理文件上传工具
./START_TAURI_DEV.sh

# 方式 3: 使用 Tauri CLI
cd tauri-app
npx tauri dev
```

### 验证启动成功

- [ ] 终端显示 "Rust 后端服务器已启动"
- [ ] 终端显示 "Vite 开发服务器已启动"
- [ ] 自动打开 Tauri 应用窗口
- [ ] 浏览器控制台无错误
- [ ] 点击登录按钮不再报错

---

## 🚫 常见错误对比

### ❌ 错误方式

```bash
# 在 tauri-app 目录
cd tauri-app
npm run dev

# 结果：
# - ✅ Vite 服务器启动成功
# - ❌ Rust 后端未启动
# - ❌ 浏览器中打开（不是应用窗口）
# - ❌ invoke() 不可用
# - ❌ 点击登录报错
```

### ✅ 正确方式

```bash
# 在 tauri-app 目录
cd tauri-app
npm run tauri:dev

# 结果：
# - ✅ Rust 后端启动成功
# - ✅ Vite 服务器启动成功
# - ✅ 应用窗口自动打开
# - ✅ invoke() 可用
# - ✅ 登录功能正常
```

---

## 🔍 调试技巧

### 1. 检查 Tauri 环境

在浏览器开发者工具的控制台输入：

```javascript
// 检查 Tauri 是否已加载
console.log("Tauri 已加载:", typeof window.__TAURI__ !== "undefined");

// 检查 invoke 函数
console.log(
  "invoke 可用:",
  typeof window.__TAURI__?.core?.invoke === "function"
);
```

### 2. 查看详细日志

启动时添加环境变量查看详细日志：

```bash
RUST_LOG=debug npm run tauri:dev
```

### 3. 检查端口占用

确保必要的端口未被占用：

```bash
# 检查 5173 端口（Vite 默认端口）
lsof -i :5173

# 如果端口被占用，终止进程
kill -9 <PID>
```

---

## 📊 启动流程对比

| 启动命令               | 前端服务器 | Rust 后端 | 应用窗口 | invoke() | 推荐 |
| ---------------------- | ---------- | --------- | -------- | -------- | ---- |
| `npm run dev`          | ✅         | ❌        | ❌       | ❌       | ❌   |
| `npm run tauri:dev`    | ✅         | ✅        | ✅       | ✅       | ✅   |
| `./START_TAURI_DEV.sh` | ✅         | ✅        | ✅       | ✅       | ✅   |

---

## 🛠️ 故障排除

### 问题 1: `tauri: command not found`

**解决方案**:

```bash
# 安装 Tauri CLI
npm install -g @tauri-apps/cli

# 或使用 npx
npx tauri dev
```

### 问题 2: Rust 编译错误

**解决方案**:

```bash
# 更新 Rust
rustup update

# 清理并重新构建
cd tauri-app/src-tauri
cargo clean
cd ../..
npm run tauri:dev
```

### 问题 3: 窗口无法打开

**解决方案**:

```bash
# 检查 Tauri 配置
cat tauri-app/src-tauri/tauri.conf.json

# 确保 build.devUrl 指向正确的地址
# 默认应该是 "http://localhost:5173"
```

### 问题 4: 依赖安装失败

**解决方案**:

```bash
# 清理并重新安装
cd tauri-app
rm -rf node_modules package-lock.json
npm install

# 安装 Rust 依赖
cd src-tauri
cargo fetch
```

---

## ✅ 验证修复

运行以下命令验证修复是否成功：

```bash
# 1. 进入目录
cd tauri-app

# 2. 启动应用
npm run tauri:dev

# 3. 等待应用启动（约 10-30 秒）

# 4. 在应用中测试
#    - 输入用户名和密码
#    - 点击登录按钮
#    - 不应该再看到 invoke 错误
```

**预期结果**:

- ✅ 应用窗口成功打开
- ✅ 登录表单正常显示
- ✅ 点击登录后显示正确的错误或成功消息
- ✅ 不再出现 "Cannot read properties of undefined" 错误

---

## 📖 相关文档

- `START_TAURI_DEV.sh` - 一键启动脚本
- `TAURI_DEVELOPMENT_GUIDE.md` - 完整开发指南
- `TAURI_TESTING_GUIDE.md` - 测试指南
- `TAURI_2X_MIGRATION_SUMMARY.md` - Tauri 2.x 迁移总结

---

## 💡 最佳实践

### 开发环境

1. **总是使用 `tauri:dev` 启动**

   ```bash
   npm run tauri:dev  # ✅ 推荐
   ```

2. **使用启动脚本**

   ```bash
   ./START_TAURI_DEV.sh  # ✅ 更简单
   ```

3. **避免单独启动前端**
   ```bash
   npm run dev  # ❌ 不推荐（除非只开发 UI）
   ```

### 生产环境

```bash
# 构建生产版本
npm run tauri:build

# 输出位置
# macOS: tauri-app/src-tauri/target/release/bundle/macos/
# Windows: tauri-app/src-tauri/target/release/bundle/msi/
# Linux: tauri-app/src-tauri/target/release/bundle/deb/
```

---

**状态**: ✅ 问题已修复  
**下一步**: 使用 `npm run tauri:dev` 启动应用

---

## 🎉 快速开始

```bash
# 一行命令启动
cd tauri-app && npm run tauri:dev
```

就是这么简单！🚀
