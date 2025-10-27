# Gitee CI/CD 配置指南

> 在 Gitee 上配置自动化打包和发布流程

**创建时间**: 2025 年 10 月 26 日  
**版本**: v1.0

---

## 📋 目录

- [方案对比](#方案对比)
- [方案一：Gitee Go（推荐）](#方案一gitee-go推荐)
- [方案二：Drone CI](#方案二drone-ci)
- [方案三：手动触发](#方案三手动触发)
- [常见问题](#常见问题)

---

## 🔍 方案对比

| 方案         | 优点               | 缺点            | 适用场景         |
| ------------ | ------------------ | --------------- | ---------------- |
| **Gitee Go** | 官方支持，配置简单 | 需要企业版      | 企业用户         |
| **Drone CI** | 开源免费，功能强大 | 需要自建服务器  | 有服务器的团队   |
| **手动触发** | 免费，无需额外配置 | 需要手动操作    | 个人项目，小团队 |
| **GitHub**   | 功能最强，完全免费 | 需要访问 GitHub | 推荐（主要方案） |

---

## 🎯 方案一：Gitee Go（推荐）

> **注意**: Gitee Go 是企业版功能，需要付费订阅

### 1. 开通 Gitee 企业版

访问 [Gitee 企业版](https://gitee.com/enterprises) 开通服务

### 2. 创建 Gitee Go 配置

在项目根目录创建 `.gitee/workflows/build.yml`:

```yaml
name: 自动打包

on:
  push:
    tags:
      - "v*"
  workflow_dispatch:

jobs:
  build-tauri:
    name: 打包 Tauri 应用
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]

    steps:
      - name: 检出代码
        uses: actions/checkout@v3

      - name: 安装 Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: 安装 Rust
        uses: dtolnay/rust-toolchain@stable

      - name: 安装依赖（Linux）
        if: matrix.os == 'ubuntu-latest'
        run: |
          sudo apt-get update
          sudo apt-get install -y libgtk-3-dev libwebkit2gtk-4.0-dev libappindicator3-dev librsvg2-dev patchelf

      - name: 安装前端依赖
        working-directory: tauri-app
        run: npm install

      - name: 构建应用
        working-directory: tauri-app
        run: npm run tauri build

      - name: 上传构建产物
        uses: actions/upload-artifact@v3
        with:
          name: app-${{ matrix.os }}
          path: |
            tauri-app/src-tauri/target/release/bundle/**/*
```

### 3. 配置说明

**触发条件**:

- 推送标签（如 `v1.0.0`）时自动触发
- 可手动触发

**构建平台**:

- ✅ Ubuntu（Linux 版本）
- ✅ macOS（Mac 版本）
- ✅ Windows（Windows 版本）

### 4. 使用方法

```bash
# 创建并推送标签触发构建
git tag v1.0.0
git push origin v1.0.0

# 或在 Gitee 网页手动触发
```

---

## 🚀 方案二：Drone CI

> **推荐**: 如果有自己的服务器，这是免费且功能强大的方案

### 1. 安装 Drone CI

#### 使用 Docker 安装

```bash
# 1. 创建 Docker Compose 配置
cat > docker-compose.yml <<EOF
version: '3'

services:
  drone-server:
    image: drone/drone:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/lib/drone:/data
    environment:
      - DRONE_GITEE_SERVER=https://gitee.com
      - DRONE_GITEE_CLIENT_ID=your_client_id
      - DRONE_GITEE_CLIENT_SECRET=your_client_secret
      - DRONE_RPC_SECRET=your_rpc_secret
      - DRONE_SERVER_HOST=drone.your-domain.com
      - DRONE_SERVER_PROTO=https

  drone-runner:
    image: drone/drone-runner-docker:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - DRONE_RPC_PROTO=http
      - DRONE_RPC_HOST=drone-server
      - DRONE_RPC_SECRET=your_rpc_secret
      - DRONE_RUNNER_CAPACITY=2
    depends_on:
      - drone-server
EOF

# 2. 启动服务
docker-compose up -d
```

### 2. 在 Gitee 创建 OAuth 应用

1. 访问 Gitee 设置 → 第三方应用
2. 创建新应用
3. 获取 `Client ID` 和 `Client Secret`
4. 设置回调地址: `https://drone.your-domain.com/login`

### 3. 创建 Drone 配置

在项目根目录创建 `.drone.yml`:

```yaml
kind: pipeline
type: docker
name: build

steps:
  # macOS 构建
  - name: build-macos
    image: ghcr.io/cirruslabs/macos-ventura-xcode:latest
    commands:
      - cd tauri-app
      - npm install
      - npm run tauri build
    when:
      event:
        - tag
      ref:
        - refs/tags/v*

  # Linux 构建
  - name: build-linux
    image: ubuntu:22.04
    commands:
      - apt-get update
      - apt-get install -y curl wget libgtk-3-dev libwebkit2gtk-4.0-dev
      - curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
      - apt-get install -y nodejs
      - curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
      - source $HOME/.cargo/env
      - cd tauri-app
      - npm install
      - npm run tauri build
    when:
      event:
        - tag

  # Windows 构建
  - name: build-windows
    image: mcr.microsoft.com/windows/servercore:ltsc2022
    commands:
      - choco install -y nodejs rust
      - cd tauri-app
      - npm install
      - npm run tauri build
    when:
      event:
        - tag

  # 上传到 Gitee Release
  - name: publish
    image: plugins/gitee-release
    settings:
      api_key:
        from_secret: gitee_token
      files:
        - tauri-app/src-tauri/target/release/bundle/**/*
    when:
      event:
        - tag

trigger:
  event:
    - tag
  ref:
    - refs/tags/v*
```

### 4. 配置 Gitee 仓库

在 Drone 管理界面中激活你的仓库，然后配置 Secret：

- `gitee_token`: Gitee 的私人令牌

### 5. 触发构建

```bash
# 创建标签触发构建
git tag v1.0.0
git push origin v1.0.0
```

---

## 🔧 方案三：手动触发（免费方案）

> 适合个人项目和小团队

### 1. 创建构建脚本

```bash
#!/bin/bash
# build-all.sh - 在本地构建所有平台

echo "🚀 开始构建所有平台..."

# 构建 Tauri 应用
cd tauri-app

echo "📦 安装依赖..."
npm install

echo "🔨 构建应用..."
npm run tauri build

echo "✅ 构建完成！"
echo "产物位置: tauri-app/src-tauri/target/release/bundle/"
```

### 2. 使用方法

```bash
# 本地构建
chmod +x build-all.sh
./build-all.sh

# 手动上传到 Gitee Release
# 1. 在 Gitee 创建 Release
# 2. 上传构建产物
```

### 3. 使用 Gitee Webhook 半自动化

创建一个简单的服务器监听 Gitee Webhook，在收到推送事件时触发构建：

```python
# webhook-server.py
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    # 检查是否是标签推送
    if data.get('ref', '').startswith('refs/tags/'):
        # 触发构建
        subprocess.Popen(['./build-all.sh'])
        return 'Build triggered', 200

    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 🔄 同时使用 GitHub 和 Gitee

### 1. 添加 Gitee 远程仓库

```bash
# 添加 Gitee 为远程仓库
git remote add gitee https://gitee.com/your-username/your-repo.git

# 查看远程仓库
git remote -v
```

### 2. 推送到两个仓库

方案 A: 手动推送

```bash
# 推送到 GitHub
git push origin main
git push origin --tags

# 推送到 Gitee
git push gitee main
git push gitee --tags
```

方案 B: 创建推送脚本

```bash
#!/bin/bash
# push-all.sh - 推送到所有远程仓库

echo "📤 推送到 GitHub..."
git push origin main
git push origin --tags

echo "📤 推送到 Gitee..."
git push gitee main
git push gitee --tags

echo "✅ 推送完成！"
```

### 3. 配置说明

- **GitHub**: 使用 GitHub Actions 进行 CI/CD（主要方案）
- **Gitee**: 作为国内镜像，可选择配置 Drone CI 或手动构建

---

## 📝 推荐方案

根据不同场景选择：

### 场景 1: 企业项目（有预算）

```
推荐: Gitee Go（企业版）
- ✅ 官方支持
- ✅ 配置简单
- ✅ 稳定可靠
```

### 场景 2: 有自己服务器

```
推荐: Drone CI
- ✅ 完全免费
- ✅ 功能强大
- ✅ 高度可定制
```

### 场景 3: 个人项目/小团队

```
推荐: GitHub Actions + Gitee 镜像
- ✅ GitHub Actions 免费且强大
- ✅ Gitee 作为国内镜像加速访问
- ✅ 手动同步代码即可
```

### 场景 4: 纯国内项目

```
推荐: 手动构建 + Gitee Release
- ✅ 完全免费
- ✅ 简单可控
- ✅ 适合小规模项目
```

---

## 🛠️ 配置步骤总结

### 方案：GitHub + Gitee 镜像（推荐）

```bash
# 1. 配置双远程仓库
git remote add origin https://github.com/your-username/your-repo.git
git remote add gitee https://gitee.com/your-username/your-repo.git

# 2. 创建 GitHub Actions 配置（已完成）
# 文件: .github/workflows/build.yml

# 3. 推送代码
./push-all.sh  # 同时推送到 GitHub 和 Gitee

# 4. 在 GitHub 创建标签触发构建
./release.sh v1.0.0

# 5. 构建完成后，从 GitHub Release 下载产物
# 6. （可选）手动上传到 Gitee Release
```

---

## ❓ 常见问题

### Q1: Gitee 免费版能用 CI/CD 吗？

**A**: Gitee 免费版没有内置 CI/CD 功能。推荐方案：

- 使用 GitHub Actions（免费且强大）
- Gitee 作为国内镜像
- 或使用 Drone CI（需要自己的服务器）

### Q2: 如何同步 GitHub 和 Gitee？

**A**: 使用我们提供的 `push-all.sh` 脚本：

```bash
#!/bin/bash
git push origin main --tags
git push gitee main --tags
```

### Q3: Drone CI 需要什么配置？

**A**: 最低配置：

- 2GB 内存
- 2 核 CPU
- 20GB 硬盘
- Docker 环境

### Q4: 能否在 Gitee 上自动同步 GitHub Release？

**A**: 可以使用 GitHub Actions：

```yaml
# .github/workflows/sync-to-gitee.yml
name: 同步到 Gitee

on:
  release:
    types: [published]

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: 下载 Release 资产
        # ... 下载逻辑

      - name: 上传到 Gitee
        # ... 使用 Gitee API 上传
```

---

## 📚 相关文档

- **[CI-CD 快速开始.md](./CI-CD快速开始.md)** - GitHub Actions 配置
- **[CI-CD 使用指南.md](./CI-CD使用指南.md)** - 详细使用说明
- **[打包指南.md](./打包指南.md)** - 本地打包方法

---

## 🔗 外部资源

- [Gitee Go 官方文档](https://gitee.com/help/articles/4378)
- [Drone CI 官方文档](https://docs.drone.io/)
- [Gitee API 文档](https://gitee.com/api/v5/swagger)

---

## 💡 最佳实践

1. **主仓库**: 使用 GitHub（CI/CD 强大且免费）
2. **国内镜像**: 使用 Gitee（加速访问）
3. **自动构建**: GitHub Actions
4. **手动同步**: 使用脚本推送到 Gitee
5. **Release**: 在 GitHub 发布，手动同步到 Gitee

---

**创建时间**: 2025 年 10 月 26 日  
**版本**: v1.0  
**维护者**: 熔盐管理项目团队
