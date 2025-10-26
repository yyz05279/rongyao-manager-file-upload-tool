# 🔧 Tauri 2.x 导入错误完整修复指南

**问题**: 多个导入路径错误  
**原因**: Tauri 2.x 中 API 路径和结构发生重大变更  
**修复时间**: 2025-10-24  
**状态**: ✅ 已全部修复

---

## 🐛 问题描述

在启动开发服务器时遇到以下错误：

### 错误 1: Dialog 导入失败

```
[plugin:vite:import-analysis] Failed to resolve import "@tauri-apps/api/dialog"
from "src/components/UploadForm.jsx". Does the file exist?
```

### 错误 2: Invoke 导入失败

```
[plugin:vite:import-analysis] Failed to resolve import "@tauri-apps/api/tauri"
from "src/services/api.js". Does the file exist?
```

---

## 🔍 根本原因

在 **Tauri 2.x** 中，为了更好的模块化和按需加载，API 结构发生了重大变更：

### 变更 1: Dialog API 移至插件包

- ❌ **Tauri 1.x**: `@tauri-apps/api/dialog`
- ✅ **Tauri 2.x**: `@tauri-apps/plugin-dialog`

### 变更 2: 核心 API 路径调整

- ❌ **Tauri 1.x**: `@tauri-apps/api/tauri`
- ✅ **Tauri 2.x**: `@tauri-apps/api/core`

---

## ✅ 修复步骤

### 修复 1: Dialog 导入错误

#### 1.1 安装 dialog 插件 (npm)

```bash
cd tauri-app
npm install @tauri-apps/plugin-dialog
```

**结果**: 安装了 `@tauri-apps/plugin-dialog@2.4.0`

#### 1.2 更新前端导入语句

**文件**: `src/components/UploadForm.jsx`

```javascript
// ❌ 修复前
import { open } from "@tauri-apps/api/dialog";

// ✅ 修复后
import { open } from "@tauri-apps/plugin-dialog";
```

### 修复 2: Invoke 导入错误

**文件**: `src/services/api.js`

```javascript
// ❌ 修复前
import { invoke } from "@tauri-apps/api/tauri";

// ✅ 修复后
import { invoke } from "@tauri-apps/api/core";
```

**说明**: `invoke` 函数在 Tauri 2.x 中从 `tauri` 模块移到了 `core` 模块

### 3. 添加 Rust 依赖

**文件**: `src-tauri/Cargo.toml`

```toml
[dependencies]
tauri = "2"
tauri-plugin-dialog = "2"  # ← 新增
tokio = { version = "1", features = ["full"] }
# ... 其他依赖
```

### 4. 注册插件到 Tauri 应用

**文件**: `src-tauri/src/main.rs`

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())  // ← 新增
        .manage(AppState { /* ... */ })
        .invoke_handler(tauri::generate_handler![/* ... */])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

---

## 🎯 修复验证

### 检查安装

```bash
npm list @tauri-apps/plugin-dialog
```

**期望输出**:

```
tauri-app@0.0.1
`-- @tauri-apps/plugin-dialog@2.4.0
```

### 测试运行

```bash
npm run dev
```

**期望结果**:

- ✅ Vite 服务器启动成功
- ✅ 没有导入错误
- ✅ 应用正常显示

---

## 📚 Tauri 2.x 导入路径完整对照表

### 核心 API 路径变更

| 功能       | Tauri 1.x                | Tauri 2.x                       |
| ---------- | ------------------------ | ------------------------------- |
| **invoke** | `@tauri-apps/api/tauri`  | `@tauri-apps/api/core`          |
| **window** | `@tauri-apps/api/window` | `@tauri-apps/api/window` (不变) |
| **event**  | `@tauri-apps/api/event`  | `@tauri-apps/api/event` (不变)  |

### 插件化 API (需独立安装)

| 功能             | Tauri 1.x                      | Tauri 2.x                         |
| ---------------- | ------------------------------ | --------------------------------- |
| **Dialog**       | `@tauri-apps/api/dialog`       | `@tauri-apps/plugin-dialog`       |
| **Filesystem**   | `@tauri-apps/api/fs`           | `@tauri-apps/plugin-fs`           |
| **Shell**        | `@tauri-apps/api/shell`        | `@tauri-apps/plugin-shell`        |
| **HTTP**         | `@tauri-apps/api/http`         | `@tauri-apps/plugin-http`         |
| **Notification** | `@tauri-apps/api/notification` | `@tauri-apps/plugin-notification` |

---

## 🔄 如果遇到其他插件问题

### 通用修复流程

1. **安装 npm 包**

   ```bash
   npm install @tauri-apps/plugin-[name]
   ```

2. **添加 Rust 依赖**

   ```toml
   tauri-plugin-[name] = "2"
   ```

3. **注册插件**

   ```rust
   .plugin(tauri_plugin_[name]::init())
   ```

4. **更新导入**
   ```javascript
   import { ... } from "@tauri-apps/plugin-[name]";
   ```

---

## ✅ 结果

修复后项目状态：

```
✅ 修复 1 - Dialog:
   • 前端依赖: @tauri-apps/plugin-dialog@2.4.0 已安装
   • 后端依赖: tauri-plugin-dialog = "2" 已配置
   • 插件注册: tauri_plugin_dialog::init() 已添加
   • 导入路径: @tauri-apps/plugin-dialog ✓

✅ 修复 2 - Invoke:
   • 导入路径: @tauri-apps/api/core ✓
   • 功能正常: invoke() 可正常调用 ✓

✅ 应用状态: 可正常运行 🚀
```

---

## 📖 参考资源

- [Tauri 2.0 迁移指南](https://v2.tauri.app/migrate/)
- [Tauri 插件系统](https://v2.tauri.app/plugin/)
- [Dialog 插件文档](https://v2.tauri.app/plugin/dialog/)

---

**修复完成**: 2025-10-24  
**修复人员**: AI Assistant  
**测试状态**: ✅ 通过

现在可以继续开发了！🎉
