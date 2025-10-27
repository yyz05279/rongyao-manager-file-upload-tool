# 🚀 CI/CD 自动打包使用指南

本指南将帮助您设置自动化打包流程，实现推送代码后自动在 macOS 和 Windows 平台打包应用。

---

## 📋 目录

1. [方案选择](#方案选择)
2. [GitHub Actions 设置](#github-actions-设置)
3. [使用方法](#使用方法)
4. [常见问题](#常见问题)

---

## 🎯 方案选择

### 您当前的情况

您的项目目前托管在 **Gitee** 上：

```
git@gitee.com:yyz05279/rongyao-manager-file-upload-tool.git
```

### 推荐方案

**方案一：使用 GitHub Actions（强烈推荐）⭐⭐⭐⭐⭐**

**优势**：

- ✅ 免费：公开仓库完全免费
- ✅ 支持 macOS + Windows + Linux 同时打包
- ✅ 功能强大：自动创建 Release、上传产物
- ✅ 生态丰富：大量现成的 Actions 可用

**缺点**：

- ⚠️ 需要在 GitHub 创建仓库（可以同时推送到 Gitee 和 GitHub）

**方案二：使用 Gitee Go（备用方案）⭐⭐**

**优势**：

- ✅ 不需要额外创建 GitHub 仓库

**缺点**：

- ⚠️ 免费版功能受限
- ⚠️ 不支持 macOS 构建环境
- ⚠️ 只能在 Linux 上打包，无法生成原生应用

---

## 🔧 GitHub Actions 设置

### 步骤 1：创建 GitHub 仓库

#### 1.1 创建仓库

访问 https://github.com/new 创建新仓库：

- Repository name: `rongyao-manager-file-upload-tool`
- Description: 熔盐管理文件上传工具
- Public（公开仓库才能免费使用 Actions）
- 不要初始化 README、.gitignore 或 license

#### 1.2 添加 GitHub 远程仓库

```bash
# 进入项目目录
cd "/Users/yyz/Desktop/熔盐管理文件上传工具"

# 添加 GitHub 远程仓库（假设您的 GitHub 用户名是 yyz05279）
git remote add github git@github.com:yyz05279/rongyao-manager-file-upload-tool.git

# 查看远程仓库
git remote -v
```

现在您将有两个远程仓库：

```
gitee   git@gitee.com:yyz05279/rongyao-manager-file-upload-tool.git
github  git@github.com:yyz05279/rongyao-manager-file-upload-tool.git
```

### 步骤 2：推送代码到 GitHub

```bash
# 推送代码到 GitHub
git push github main

# 如果分支名是 master
git push github master
```

### 步骤 3：检查 GitHub Actions

#### 3.1 访问 GitHub Actions 页面

打开浏览器访问：

```
https://github.com/你的用户名/rongyao-manager-file-upload-tool/actions
```

您应该能看到 "Build Tauri App" 工作流。

#### 3.2 启用 Actions（如果需要）

如果 Actions 没有自动启用，点击 "I understand my workflows, go ahead and enable them" 按钮。

---

## 🚀 使用方法

### 方法一：通过标签触发自动打包（推荐）

```bash
# 1. 确保代码已提交
git add .
git commit -m "准备发布 v1.0.0"

# 2. 创建版本标签
git tag v1.0.0

# 3. 推送代码和标签到 GitHub
git push github main
git push github v1.0.0

# 可选：同时推送到 Gitee
git push gitee main
git push gitee v1.0.0
```

**自动执行的操作**：

1. ✅ 自动在 macOS 和 Windows 上打包
2. ✅ 生成 DMG、MSI 等安装包
3. ✅ 自动创建 GitHub Release
4. ✅ 上传所有打包文件到 Release

### 方法二：手动触发打包

如果您不想创建标签，也可以手动触发：

1. 访问 Actions 页面：

   ```
   https://github.com/你的用户名/rongyao-manager-file-upload-tool/actions
   ```

2. 点击左侧 "Build Tauri App"

3. 点击右上角 "Run workflow" 按钮

4. 选择分支，点击 "Run workflow"

---

## 📦 下载打包文件

### 方法一：从 GitHub Actions 下载

1. 访问 Actions 页面
2. 点击完成的工作流运行
3. 在页面底部 "Artifacts" 区域下载：
   - `macos-dmg` - macOS DMG 安装包
   - `macos-app` - macOS .app 应用
   - `windows-msi` - Windows MSI 安装包
   - `windows-nsis` - Windows NSIS 安装包

### 方法二：从 GitHub Release 下载（推荐）

如果通过标签触发，会自动创建 Release：

1. 访问 Release 页面：

   ```
   https://github.com/你的用户名/rongyao-manager-file-upload-tool/releases
   ```

2. 找到对应版本（如 v1.0.0）

3. 在 "Assets" 区域下载安装包

---

## ⚙️ 配置说明

### 工作流配置文件

已创建：`.github/workflows/build.yml`

**触发条件**：

- 推送 `v*` 开头的标签（如 v1.0.0, v2.1.3）
- 手动触发（通过 GitHub 网页界面）

**打包平台**：

- macOS（最新版本）
- Windows（最新版本）

**生成文件**：

- macOS: `.dmg` 和 `.app`
- Windows: `.msi` 和 `.exe`

---

## 🔄 同时使用 Gitee 和 GitHub

### 创建便捷的推送脚本

创建 `push-all.sh` 脚本：

```bash
#!/bin/bash
# 同时推送到 Gitee 和 GitHub

echo "推送到 Gitee..."
git push gitee main

echo "推送到 GitHub..."
git push github main

echo "✅ 推送完成！"
```

使用方法：

```bash
chmod +x push-all.sh
./push-all.sh
```

### 发布新版本脚本

创建 `release.sh` 脚本：

```bash
#!/bin/bash
# 发布新版本

if [ -z "$1" ]; then
  echo "用法: ./release.sh v1.0.0"
  exit 1
fi

VERSION=$1

echo "准备发布版本: $VERSION"

# 1. 提交所有更改
git add .
git commit -m "Release $VERSION"

# 2. 创建标签
git tag $VERSION

# 3. 推送到 Gitee
echo "推送到 Gitee..."
git push gitee main
git push gitee $VERSION

# 4. 推送到 GitHub（触发自动打包）
echo "推送到 GitHub..."
git push github main
git push github $VERSION

echo "✅ 发布完成！"
echo "访问以下链接查看打包进度："
echo "https://github.com/你的用户名/rongyao-manager-file-upload-tool/actions"
```

使用方法：

```bash
chmod +x release.sh
./release.sh v1.0.0
```

---

## 📊 工作流程图

```
本地开发
  ↓
提交代码 (git commit)
  ↓
创建标签 (git tag v1.0.0)
  ↓
推送到 GitHub (git push github v1.0.0)
  ↓
GitHub Actions 自动触发
  ├─→ macOS 构建机器
  │   ├─ 安装依赖
  │   ├─ 编译 Tauri 应用
  │   └─ 生成 .dmg 和 .app
  │
  └─→ Windows 构建机器
      ├─ 安装依赖
      ├─ 编译 Tauri 应用
      └─ 生成 .msi 和 .exe
  ↓
自动创建 GitHub Release
  ↓
上传所有打包文件
  ↓
✅ 完成！用户可以下载
```

---

## ❓ 常见问题

### Q1: GitHub Actions 构建失败了怎么办？

**查看错误日志**：

1. 访问 Actions 页面
2. 点击失败的工作流
3. 查看红色的步骤，点击查看详细日志

**常见错误**：

#### 错误：Rust not found

```yaml
# 已在配置中包含，无需修改
- name: Install Rust stable
  uses: dtolnay/rust-toolchain@stable
```

#### 错误：npm install 失败

```bash
# 检查 package.json 是否正确
# 确保 tauri-app/package.json 存在
```

#### 错误：找不到文件

```yaml
# 检查路径是否正确
# 确保在 tauri-app 目录下执行命令
```

### Q2: 构建时间太长了

- 首次构建：约 15-20 分钟（需要安装所有依赖）
- 后续构建：约 5-10 分钟（有缓存加速）

**优化建议**：

```yaml
# 在 build.yml 中添加缓存（已包含在 Rust Action 中）
- name: Cache cargo registry
  uses: actions/cache@v3
  with:
    path: ~/.cargo/registry
    key: ${{ runner.os }}-cargo-registry-${{ hashFiles('**/Cargo.lock') }}
```

### Q3: 我想只打包 macOS 或 Windows

编辑 `.github/workflows/build.yml`：

```yaml
# 只打包 macOS
platform: [macos-latest]

# 只打包 Windows
platform: [windows-latest]

# 打包所有平台（包括 Linux）
platform: [macos-latest, windows-latest, ubuntu-latest]
```

### Q4: 我想在每次推送时都打包

修改触发条件：

```yaml
on:
  push:
    branches:
      - main # 每次推送到 main 分支时打包
  pull_request:
    branches:
      - main # 每次 PR 时打包
```

⚠️ **注意**：这会消耗更多的 Actions 时间，虽然免费但有限制。

### Q5: GitHub Actions 免费吗？

**公开仓库**：

- ✅ 完全免费
- ✅ 无限制的构建时间

**私有仓库**：

- 免费额度：每月 2000 分钟
- macOS 构建：消耗 10 倍时间（1 分钟 = 10 分钟配额）
- Windows 构建：消耗 2 倍时间

**建议**：使用公开仓库，或者购买 GitHub Pro。

---

## 📞 获取帮助

### 文档资源

- **GitHub Actions 文档**: https://docs.github.com/actions
- **Tauri Actions**: https://github.com/tauri-apps/tauri-action
- **本项目文档**: 查看 `打包指南.md`

### 检查清单

在提交 Issue 前，请检查：

- [ ] 代码已成功推送到 GitHub
- [ ] GitHub Actions 已启用
- [ ] 工作流文件路径正确：`.github/workflows/build.yml`
- [ ] `tauri-app/package.json` 存在
- [ ] `tauri-app/src-tauri/tauri.conf.json` 配置正确

---

## 🎉 快速开始

### 最简单的流程

```bash
# 1. 在 GitHub 创建仓库（通过网页）

# 2. 添加 GitHub 远程仓库
cd "/Users/yyz/Desktop/熔盐管理文件上传工具"
git remote add github git@github.com:你的用户名/rongyao-manager-file-upload-tool.git

# 3. 推送代码
git push github main

# 4. 创建并推送标签（触发自动打包）
git tag v1.0.0
git push github v1.0.0

# 5. 访问 GitHub 查看打包进度
# https://github.com/你的用户名/rongyao-manager-file-upload-tool/actions

# 6. 等待 15-20 分钟后，在 Release 页面下载安装包
# https://github.com/你的用户名/rongyao-manager-file-upload-tool/releases
```

---

## 🎊 下一步

完成 CI/CD 设置后，您可以：

1. ✅ 专注于开发，不用担心打包问题
2. ✅ 每次发布新版本，只需创建标签
3. ✅ 自动生成适用于所有平台的安装包
4. ✅ 用户可以从 GitHub Release 直接下载

**享受自动化的便利吧！** 🚀

---

**最后更新**: 2025-10-26
**工作流状态**: ✅ 已配置
**下一步**: 创建 GitHub 仓库并推送代码
