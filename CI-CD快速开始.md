# 🚀 CI/CD 快速开始

只需 **3 个步骤**，即可实现自动化跨平台打包！

---

## ✅ 已完成的工作

- ✅ GitHub Actions 配置文件已创建
- ✅ 自动化脚本已准备就绪
- ✅ 支持同时推送到 Gitee 和 GitHub

---

## 📋 快速开始（3 步走）

### 步骤 1️⃣：设置 GitHub 仓库

运行交互式设置脚本：

```bash
./setup-github.sh
```

**脚本会引导您**：

- 输入 GitHub 用户名
- 输入仓库名
- 自动配置远程仓库

**然后在 GitHub 创建仓库**：

1. 访问 https://github.com/new
2. 仓库名：`rongyao-manager-file-upload-tool`
3. 设为 **Public**（公开才能免费使用 Actions）
4. 不要初始化任何文件
5. 点击 "Create repository"

### 步骤 2️⃣：推送代码到 GitHub

```bash
# 推送主分支
git push github main

# 如果分支名是 master
git push github master
```

**检查 Actions 是否启用**：
访问 https://github.com/你的用户名/rongyao-manager-file-upload-tool/actions

如果显示需要启用，点击 "I understand my workflows, go ahead and enable them"

### 步骤 3️⃣：发布版本（触发自动打包）

使用发布脚本：

```bash
./release.sh v1.0.0
```

**脚本会自动**：

- ✅ 检查未提交的更改
- ✅ 创建版本标签
- ✅ 推送到 Gitee 和 GitHub
- ✅ 触发自动打包
- ✅ 显示进度查看链接

---

## 🎉 完成！

### 查看打包进度

访问 GitHub Actions 页面：

```
https://github.com/你的用户名/rongyao-manager-file-upload-tool/actions
```

### 预计等待时间

- **首次打包**：15-20 分钟（需要下载和编译所有依赖）
- **后续打包**：5-10 分钟（有缓存加速）

### 下载打包文件

**方法 1：从 Actions 下载**

1. 打开完成的工作流
2. 滚动到底部 "Artifacts" 区域
3. 下载对应平台的安装包

**方法 2：从 Release 下载（推荐）**

```
https://github.com/你的用户名/rongyao-manager-file-upload-tool/releases
```

---

## 📦 生成的安装包

### macOS

- ✅ `熔盐管理文件上传工具_1.0.0_aarch64.dmg` - Apple Silicon 版本
- ✅ `熔盐管理文件上传工具_1.0.0_x64.dmg` - Intel Mac 版本
- ✅ `熔盐管理文件上传工具.app` - 应用包

### Windows

- ✅ `熔盐管理文件上传工具_1.0.0_x64.msi` - MSI 安装包（推荐）
- ✅ `熔盐管理文件上传工具_1.0.0_x64-setup.exe` - NSIS 安装包

---

## 🔄 日常使用

### 发布新版本

```bash
# 一键发布
./release.sh v1.0.1

# 或者手动操作
git tag v1.0.1
git push github v1.0.1  # 触发自动打包
```

### 推送日常代码

```bash
# 同时推送到 Gitee 和 GitHub
./push-all.sh

# 或者分别推送
git push gitee main
git push github main
```

### 手动触发打包

不想创建标签？直接在 GitHub 网页上触发：

1. 访问：https://github.com/你的用户名/rongyao-manager-file-upload-tool/actions
2. 点击左侧 "Build Tauri App"
3. 点击右上角 "Run workflow"
4. 选择分支，点击 "Run workflow"

---

## 🛠️ 可用脚本

### `setup-github.sh` - 设置 GitHub 仓库

```bash
./setup-github.sh
```

交互式配置 GitHub 远程仓库

### `release.sh` - 发布新版本

```bash
./release.sh v1.0.0
```

自动创建标签并推送，触发自动打包

### `push-all.sh` - 推送到所有仓库

```bash
./push-all.sh
```

同时推送到 Gitee 和 GitHub

---

## 📖 详细文档

- **完整指南**：`CI-CD使用指南.md`
- **打包指南**：`打包指南.md`
- **项目索引**：`INDEX.md`

---

## ❓ 常见问题

### Q: GitHub Actions 是免费的吗？

**公开仓库**：✅ 完全免费，无限制  
**私有仓库**：每月 2000 分钟免费额度

### Q: 可以只打包 macOS 或 Windows 吗？

可以！编辑 `.github/workflows/build.yml`：

```yaml
# 只打包 macOS
platform: [macos-latest]

# 只打包 Windows
platform: [windows-latest]

# 打包所有平台
platform: [macos-latest, windows-latest]
```

### Q: 能否在每次推送时自动打包？

可以，但不推荐（会消耗大量时间）。如需要，修改 `.github/workflows/build.yml`：

```yaml
on:
  push:
    branches:
      - main # 每次推送都打包
```

### Q: 打包失败了怎么办？

1. 查看 Actions 页面的错误日志
2. 检查 `tauri-app/package.json` 是否存在
3. 检查 `tauri-app/src-tauri/tauri.conf.json` 配置
4. 查看 `CI-CD使用指南.md` 的常见问题章节

**✅ 已修复的常见问题**：

- **图标找不到**：已添加 `icon` 配置到 `tauri.conf.json`
- **Windows WiX 打包失败**：已将 `productName` 改为英文（`molten-salt-upload`），避免中文路径问题
- **未使用的方法警告**：已移除 `auth.rs` 中的 `get_token` 方法

详见：`docs/Windows打包中文问题修复.md`

---

## 🎊 工作流程示意

```
开发代码
  ↓
./push-all.sh (日常推送)
  ↓
准备发布
  ↓
./release.sh v1.0.0 (发布版本)
  ↓
自动触发 GitHub Actions
  ├─ macOS 自动打包 (15 分钟)
  └─ Windows 自动打包 (15 分钟)
  ↓
自动创建 Release 并上传文件
  ↓
✅ 用户从 GitHub Release 下载
```

---

## 🎯 下一步

1. ✅ 运行 `./setup-github.sh` 设置 GitHub
2. ✅ 在 GitHub 创建公开仓库
3. ✅ 运行 `git push github main` 推送代码
4. ✅ 运行 `./release.sh v1.0.0` 发布第一个版本
5. ✅ 喝杯咖啡，等待 15 分钟
6. ✅ 在 GitHub Release 下载安装包

**就是这么简单！** 🎉

---

**最后更新**: 2025-10-26  
**配置状态**: ✅ 已完成  
**可以开始**: 立即使用！
