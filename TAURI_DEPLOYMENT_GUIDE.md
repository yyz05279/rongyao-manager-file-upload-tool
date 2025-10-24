# 🚀 Tauri 项目部署和发布指南

**项目**: 熔盐管理文件上传工具 - Tauri 版本  
**版本**: v0.1.0  
**发布日期**: 2025-10-24

---

## 📋 目录

1. [部署前检查](#部署前检查)
2. [生产环境配置](#生产环境配置)
3. [构建打包](#构建打包)
4. [平台特定配置](#平台特定配置)
5. [签名和证书](#签名和证书)
6. [发布流程](#发布流程)
7. [更新管理](#更新管理)
8. [问题排查](#问题排查)

---

## 🔍 部署前检查

### 1. 代码质量检查

```bash
cd /Users/yyz/Desktop/熔盐管理文件上传工具/tauri-app

# 检查是否有 console.log
grep -r "console.log" src/
# 预期: 仅在需要的地方使用

# 检查是否有 TODO/FIXME
grep -r "TODO\|FIXME" src/ src-tauri/
# 预期: 无任何未完成的标记

# 检查代码格式
npm run lint  # 如果配置了
```

### 2. 功能完整性检查

- [ ] 登录功能正常
- [ ] 项目查询正常
- [ ] 文件上传正常
- [ ] 错误处理完善
- [ ] 状态管理正确
- [ ] UI 响应式设计
- [ ] 中文显示正确

### 3. 性能检查

```bash
# 前端构建大小
npm run build
ls -lh dist/

# 预期: 总大小 < 5MB
```

### 4. 依赖检查

```bash
# 检查依赖安全性
npm audit

# 检查过期依赖
npm outdated

# 更新依赖（如需要）
npm update
```

### 5. 配置检查

**检查项:**

- [ ] API 地址已正确配置
- [ ] 环境变量已设置
- [ ] 密钥已安全保存
- [ ] 版本号已更新

---

## ⚙️ 生产环境配置

### 1. 环境变量设置

创建 `.env.production` 文件：

```env
# API 配置
VITE_API_BASE_URL=https://api.example.com
VITE_APP_NAME=熔盐管理文件上传工具
VITE_APP_VERSION=0.1.0

# 功能开关
VITE_ENABLE_DEBUG=false
VITE_ENABLE_LOGGING=false
```

### 2. 更新 vite.config.js

```javascript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
  build: {
    outDir: "dist",
    sourcemap: false, // 关闭 SourceMap（生产环境）
    minify: "terser", // 最小化代码
    rollupOptions: {
      output: {
        manualChunks: {
          // 代码分割
          vendor: ["react", "react-dom", "zustand"],
        },
      },
    },
  },
  define: {
    __APP_VERSION__: JSON.stringify("0.1.0"),
  },
});
```

### 3. 更新 Cargo.toml（生产优化）

```toml
[profile.release]
opt-level = 3           # 优化级别
lto = true             # 链接时优化
codegen-units = 1      # 优化生成的代码单元
strip = true           # 删除调试符号
```

### 4. 配置应用信息

更新 `src-tauri/tauri.conf.json`：

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devPath": "http://localhost:5173",
    "frontendDist": "../dist"
  },
  "app": {
    "windows": [
      {
        "title": "熔盐管理文件上传工具",
        "width": 1200,
        "height": 800,
        "minWidth": 400,
        "minHeight": 600,
        "resizable": true,
        "fullscreen": false
      }
    ],
    "security": {
      "csp": "default-src 'self'"
    }
  },
  "package": {
    "productName": "熔盐管理文件上传工具",
    "version": "0.1.0"
  }
}
```

---

## 🏗️ 构建打包

### 1. 预构建清理

```bash
cd /Users/yyz/Desktop/熔盐管理文件上传工具/tauri-app

# 清除旧的构建
rm -rf dist/
rm -rf src-tauri/target/

# 清除依赖缓存（如需要）
rm -rf node_modules/
npm install
```

### 2. 前端构建

```bash
# 构建前端
npm run build

# 验证构建结果
ls -la dist/
du -sh dist/

# 预期: dist 大小 < 5MB
```

### 3. 后端编译

```bash
cd src-tauri

# 清除旧编译
cargo clean

# 完整编译
cargo build --release

# 验证
ls -la target/release/
```

### 4. 完整打包

```bash
# 返回项目根目录
cd ..

# 创建平台特定包
npm run tauri:build

# 这会生成:
# - macOS: .dmg 和 .app.tar.gz
# - Windows: .msi 和 .exe
# - Linux: .deb 和 .AppImage
```

---

## 🖥️ 平台特定配置

### macOS 配置

#### 1. 获取开发者证书

```bash
# 登录 Apple Developer 账号
# 创建 Signing Certificate

# 导入证书到钥匙串
# 从 Apple Developer 下载证书并导入
```

#### 2. 配置签名

编辑 `src-tauri/tauri.conf.json`:

```json
{
  "tauri": {
    "bundle": {
      "macOS": {
        "signingIdentity": "Apple Development: your-email@example.com (XXXXXXXXXX)"
      }
    }
  }
}
```

#### 3. 打包 macOS

```bash
# 通用二进制（Intel + Apple Silicon）
cargo tauri build --target universal-apple-darwin

# 仅 Apple Silicon
cargo tauri build --target aarch64-apple-darwin

# 仅 Intel
cargo tauri build --target x86_64-apple-darwin
```

**输出位置:**

```
src-tauri/target/universal-apple-darwin/release/bundle/
├── dmg/
│   └── 熔盐管理文件上传工具_0.1.0_universal.dmg
├── macos/
│   └── 熔盐管理文件上传工具.app
└── macos/
    └── 熔盐管理文件上传工具.app.tar.gz
```

### Windows 配置

#### 1. 安装工具

```bash
# 安装 Visual Studio Build Tools 或 Visual Studio Community
# 选择 "Desktop development with C++"

# 或使用 Rust 工具链
rustup target add x86_64-pc-windows-msvc
```

#### 2. 打包 Windows

```bash
# 32 位
cargo tauri build --target i686-pc-windows-msvc

# 64 位 (推荐)
cargo tauri build --target x86_64-pc-windows-msvc
```

**输出位置:**

```
src-tauri/target/x86_64-pc-windows-msvc/release/bundle/
├── msi/
│   └── 熔盐管理文件上传工具_0.1.0_x64_en-US.msi
└── nsis/
    └── 熔盐管理文件上传工具_0.1.0_x64-setup.exe
```

### Linux 配置

#### 1. 安装依赖

```bash
# Ubuntu/Debian
sudo apt-get install \
  libgtk-3-dev \
  libwebkit2gtk-4.0-dev \
  librsvg2-dev

# Fedora
sudo dnf install \
  gtk3-devel \
  webkit2gtk3-devel \
  libappindicator-gtk3-devel
```

#### 2. 打包 Linux

```bash
# 打包 .deb
cargo tauri build --target x86_64-unknown-linux-gnu

# 打包 AppImage
cargo tauri build --target x86_64-unknown-linux-gnu --bundles appimage
```

**输出位置:**

```
src-tauri/target/x86_64-unknown-linux-gnu/release/bundle/
├── deb/
│   └── 熔盐管理文件上传工具_0.1.0_amd64.deb
└── appimage/
    └── 熔盐管理文件上传工具_0.1.0_amd64.AppImage
```

---

## 🔐 签名和证书

### macOS 代码签名

```bash
# 使用开发者证书签名
codesign --deep --force --verify --verbose \
  --sign "Apple Development: your-email@example.com" \
  "src-tauri/target/universal-apple-darwin/release/bundle/macos/熔盐管理文件上传工具.app"

# 验证签名
codesign --verify --verbose \
  "src-tauri/target/universal-apple-darwin/release/bundle/macos/熔盐管理文件上传工具.app"
```

### Windows 代码签名

```bash
# 使用 SignTool 签名 (需要代码签名证书)
signtool sign /f certificate.pfx /p password \
  /t http://timestamp.verisign.com/scripts/timstamp.dll \
  "src-tauri/target/x86_64-pc-windows-msvc/release/bundle/msi/熔盐管理文件上传工具_0.1.0_x64_en-US.msi"
```

---

## 📦 发布流程

### 1. 版本管理

```bash
# 更新版本号
cd /Users/yyz/Desktop/熔盐管理文件上传工具/tauri-app

# 更新 package.json
# 更新 src-tauri/Cargo.toml
# 更新 src-tauri/tauri.conf.json

# 创建 Git 标签
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

### 2. 构建发布版本

```bash
# 完整清理
rm -rf dist node_modules src-tauri/target

# 重新安装依赖
npm install

# 构建前端
npm run build

# 构建所有平台
npm run tauri:build

# 验证输出
ls -la src-tauri/target/*/release/bundle/
```

### 3. 测试发布版本

```bash
# 测试 macOS
open src-tauri/target/universal-apple-darwin/release/bundle/dmg/\
  "熔盐管理文件上传工具_0.1.0_universal.dmg"

# 测试 Windows
cd src-tauri/target/x86_64-pc-windows-msvc/release/bundle/
# 双击 .msi 或 .exe 安装

# 测试 Linux
sudo dpkg -i src-tauri/target/x86_64-unknown-linux-gnu/release/bundle/deb/\
  "熔盐管理文件上传工具_0.1.0_amd64.deb"
```

### 4. 发布到平台

#### GitHub Releases

```bash
# 创建 Release
gh release create v0.1.0 \
  src-tauri/target/universal-apple-darwin/release/bundle/dmg/*.dmg \
  src-tauri/target/x86_64-pc-windows-msvc/release/bundle/msi/*.msi \
  src-tauri/target/x86_64-unknown-linux-gnu/release/bundle/deb/*.deb \
  --title "v0.1.0 Release" \
  --notes "Release notes here"
```

#### 官方网站

1. 上传文件到服务器
2. 更新下载链接
3. 发布公告

---

## 🔄 更新管理

### 1. 启用自动更新

在 `src-tauri/tauri.conf.json` 中配置:

```json
{
  "tauri": {
    "updater": {
      "active": true,
      "endpoints": [
        "https://updates.example.com/{{target}}/{{arch}}/update.json"
      ],
      "dialog": true,
      "pubkey": "YOUR_PUBLIC_KEY"
    }
  }
}
```

### 2. 生成更新清单

```bash
# 使用 tauri CLI 生成签名
cargo tauri signer generate --write-keys

# 这会生成:
# - private key (安全保存)
# - public key (添加到配置)
```

### 3. 创建更新服务器

```json
{
  "version": "0.2.0",
  "notes": "Bug 修复和性能改进",
  "pub_date": "2025-10-25T00:00:00Z",
  "platforms": {
    "darwin-universal": {
      "signature": "SIGNATURE",
      "url": "https://example.com/app-0.2.0-universal.dmg"
    },
    "win32": {
      "signature": "SIGNATURE",
      "url": "https://example.com/app-0.2.0.msi"
    },
    "linux": {
      "signature": "SIGNATURE",
      "url": "https://example.com/app-0.2.0.deb"
    }
  }
}
```

---

## 🔧 问题排查

### 常见问题

#### Q1: 构建失败 "could not find C++ preprocessor"

**解决方案 (Windows):**

```bash
# 安装 Visual Studio Build Tools
# 或使用 Rust MSVC 工具链
rustup target add x86_64-pc-windows-msvc
```

#### Q2: 签名验证失败 (macOS)

**解决方案:**

```bash
# 检查证书
security find-identity -v -p codesigning

# 重新下载证书
# 在 Apple Developer 重新获取证书
```

#### Q3: 文件过大

**解决方案:**

```bash
# 检查文件大小
du -sh src-tauri/target/release/

# 启用 LTO 和 strip
# 在 Cargo.toml 中配置:
[profile.release]
lto = true
strip = true
```

#### Q4: 应用启动缓慢

**解决方案:**

- 检查是否有大文件
- 检查是否有网络请求
- 使用分析工具找出瓶颈

---

## ✅ 发布前清单

在发布前检查以下所有项目：

### 代码质量

- [ ] 无 console.log 调试
- [ ] 无 TODO/FIXME 标记
- [ ] 无未使用的导入
- [ ] 所有错误已处理

### 功能完整性

- [ ] 所有功能已测试
- [ ] 错误处理完善
- [ ] 文档已更新
- [ ] 版本号已更新

### 性能

- [ ] 应用大小 < 100MB
- [ ] 启动时间 < 5s
- [ ] 内存占用合理
- [ ] 响应时间满足要求

### 安全性

- [ ] 敏感信息已移除
- [ ] API 密钥已隐藏
- [ ] 没有硬编码密码
- [ ] 代码已审计

### 部署

- [ ] 所有平台已构建
- [ ] 所有包已签名
- [ ] 包已测试
- [ ] 发布说明已准备

---

## 📞 支持和反馈

部署期间如有问题：

1. 查看 Tauri 官方文档
2. 检查项目日志
3. 查看 GitHub Issues
4. 联系开发团队

---

**最后更新**: 2025-10-24  
**发布版本**: v0.1.0
