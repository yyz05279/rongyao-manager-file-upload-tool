# Tauri 应用代码签名配置指南

## 📋 概述

本指南介绍如何为 Tauri 应用配置 macOS 代码签名，解决"无法打开应用程序"的问题。

## 🎯 问题现象

从 CI/CD 下载的 Tauri 应用无法打开，提示：

> "你无法打开应用程序'molten-salt-upload'，因为这台 Mac 不支持此应用程序"

## ✅ 已完成的配置

### 1. 本地签名配置

已更新 `tauri.conf.json` 添加签名身份：

```json
"macOS": {
  "minimumSystemVersion": "10.13",
  "signingIdentity": "Apple Development: yinzhen ye (B7U63QS5Y7)",
  "entitlements": null
}
```

### 2. 权限文件

已创建 `src-tauri/entitlements.plist`，包含必要的运行时权限：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>com.apple.security.cs.allow-jit</key>
  <true/>
  <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
  <true/>
  <key>com.apple.security.cs.disable-library-validation</key>
  <true/>
  <key>com.apple.security.network.client</key>
  <true/>
  <key>com.apple.security.network.server</key>
  <true/>
</dict>
</plist>
```

### 3. GitHub Actions 工作流

已创建 `.github/workflows/build-tauri.yml`，支持自动打包和签名。

## 🚀 快速修复已下载的应用

### 方法 1：使用项目根目录的修复脚本

```bash
# 从项目根目录运行
./fix-macos-app.sh auto
```

脚本会自动查找并修复 Tauri 应用。

### 方法 2：手动命令修复

```bash
# 进入 Tauri 应用目录
cd tauri-app/src-tauri/target/release/bundle/macos

# 移除隔离属性
xattr -cr "molten-salt-upload.app"

# 打开应用
open "molten-salt-upload.app"
```

### 方法 3：右键打开

1. 在 Finder 中找到应用
2. 按住 Control 键并点击应用
3. 选择"打开"
4. 在弹出的对话框中再次点击"打开"

## 🔧 本地开发时的签名

### 验证当前证书

```bash
# 查看可用的签名证书
security find-identity -v -p codesigning
```

输出应该包含：

```
1) 19954703843188B03F6C909CD2589C9ED406CD06 "Apple Development: yinzhen ye (B7U63QS5Y7)"
```

### 构建签名应用

```bash
cd tauri-app

# 构建并自动签名（使用 tauri.conf.json 中的配置）
npm run tauri build

# 或使用环境变量指定签名身份
APPLE_SIGNING_IDENTITY="Apple Development: yinzhen ye (B7U63QS5Y7)" npm run tauri build
```

### 验证签名

```bash
# 检查应用签名
codesign -dv --verbose=4 "src-tauri/target/release/bundle/macos/molten-salt-upload.app"

# 验证签名有效性
codesign --verify --deep --strict --verbose=2 "src-tauri/target/release/bundle/macos/molten-salt-upload.app"
```

## 🎬 CI/CD 自动签名配置

### 准备证书

#### 1. 导出开发证书

```bash
# 从钥匙串导出证书（会提示输入密码）
security find-identity -v -p codesigning
security export -k login.keychain -t identities -f pkcs12 -o certificate.p12
```

会生成 `certificate.p12` 文件。

#### 2. 转换为 Base64

```bash
# 将证书编码为 base64
base64 -i certificate.p12 -o certificate.p12.base64

# 查看内容（用于添加到 GitHub Secrets）
cat certificate.p12.base64
```

### 配置 GitHub Secrets

在 GitHub 仓库设置中添加以下 Secrets：

1. **APPLE_CERTIFICATE**

   - 值：`certificate.p12.base64` 的完整内容

2. **APPLE_CERTIFICATE_PASSWORD**

   - 值：导出证书时设置的密码

3. **KEYCHAIN_PASSWORD**

   - 值：用于 CI 临时钥匙串的密码（任意强密码）

4. **APPLE_SIGNING_IDENTITY**
   - 值：`Apple Development: yinzhen ye (B7U63QS5Y7)`

### 配置步骤

1. 进入 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 依次添加上述 4 个 secrets

### 触发自动打包

```bash
# 创建并推送标签
git tag v1.0.0
git push origin v1.0.0

# 或使用 release.sh 脚本
./release.sh v1.0.0
```

## 📦 构建通用二进制（Universal Binary）

为了支持 Intel 和 Apple Silicon Mac：

```bash
# 本地构建通用二进制
cd tauri-app
npm run tauri build -- --target universal-apple-darwin
```

输出位置：

- DMG: `src-tauri/target/universal-apple-darwin/release/bundle/dmg/*.dmg`
- App: `src-tauri/target/universal-apple-darwin/release/bundle/macos/*.app`

## 🔒 分发级别签名（可选）

### 获取 Developer ID 证书

如果需要公开分发（不仅限于开发测试），需要：

1. **注册 Apple Developer Program**

   - 费用：$99/年
   - 网址：https://developer.apple.com/programs/

2. **申请 Developer ID Application 证书**

   - 在 Xcode → Preferences → Accounts
   - 或访问 https://developer.apple.com/account/resources/certificates/

3. **更新 tauri.conf.json**

```json
"macOS": {
  "minimumSystemVersion": "10.13",
  "signingIdentity": "Developer ID Application: Your Name (TEAM_ID)",
  "entitlements": null,
  "providerShortName": "TEAM_ID"
}
```

### 应用公证（Notarization）

公证后的应用可以在任何 Mac 上无缝运行：

```bash
# 构建应用
npm run tauri build -- --target universal-apple-darwin

# 打包为 DMG（如果还未生成）
cd src-tauri/target/universal-apple-darwin/release/bundle
hdiutil create -volname "熔盐管理文件上传工具" \
    -srcfolder macos/molten-salt-upload.app \
    -ov -format UDZO \
    molten-salt-upload.dmg

# 签名 DMG
codesign --sign "Developer ID Application: Your Name (TEAM_ID)" \
    molten-salt-upload.dmg

# 提交公证
xcrun notarytool submit molten-salt-upload.dmg \
    --apple-id "your@email.com" \
    --team-id "TEAM_ID" \
    --password "app-specific-password" \
    --wait

# 订阅公证票据
xcrun stapler staple molten-salt-upload.dmg

# 验证公证
spctl -a -vv -t install molten-salt-upload.dmg
```

### 生成 App-Specific Password

1. 访问 https://appleid.apple.com/account/manage
2. 登录 Apple ID
3. 在"安全"部分，点击"App-Specific Passwords"
4. 点击 "+" 生成新密码
5. 复制密码（仅显示一次）

## 📊 签名级别对比

| 特性         | 开发签名      | Developer ID  | Developer ID + 公证 |
| ------------ | ------------- | ------------- | ------------------- |
| 成本         | 免费          | $99/年        | $99/年              |
| 本地运行     | ✅ 需手动允许 | ✅ 需手动允许 | ✅ 无缝运行         |
| 分发给他人   | ❌ 不推荐     | ⚠️ 需手动允许 | ✅ 无缝安装         |
| macOS 10.15+ | ⚠️ 严格限制   | ⚠️ 需手动允许 | ✅ 完全支持         |
| 企业分发     | ❌ 不支持     | ⚠️ 有限支持   | ✅ 推荐             |
| 自动更新     | ❌ 不支持     | ⚠️ 有限支持   | ✅ 支持             |

## ⚠️ 常见问题

### Q1: 本地打包后还是无法打开？

**A:** 检查签名配置：

```bash
# 验证 tauri.conf.json 中的 signingIdentity 是否正确
cat tauri-app/src-tauri/tauri.conf.json | grep signingIdentity

# 验证证书是否在钥匙串中
security find-identity -v -p codesigning
```

### Q2: CI/CD 打包失败，提示找不到证书？

**A:** 检查 GitHub Secrets 配置：

1. 确认已添加所有必需的 secrets
2. 检查 `APPLE_CERTIFICATE` 是否是 base64 编码
3. 验证 `APPLE_SIGNING_IDENTITY` 格式正确

### Q3: 签名后应用运行出错？

**A:** 可能是权限配置问题：

```bash
# 检查权限文件
cat tauri-app/src-tauri/entitlements.plist

# 重新签名并指定权限文件
codesign --force --deep --sign "Your Identity" \
    --entitlements tauri-app/src-tauri/entitlements.plist \
    "path/to/app.app"
```

### Q4: Universal Binary 构建失败？

**A:** 确保安装了必要的 Rust targets：

```bash
rustup target add aarch64-apple-darwin
rustup target add x86_64-apple-darwin
```

### Q5: 从 GitHub Release 下载后还是被阻止？

**A:** 这是正常的，因为使用的是开发签名。解决方案：

1. 使用 `fix-macos-app.sh` 脚本
2. 或右键点击 → 打开
3. 或升级到 Developer ID + 公证

## 🔗 相关资源

### 官方文档

- [Tauri 代码签名](https://tauri.app/v1/guides/distribution/sign-macos)
- [Apple 代码签名指南](https://developer.apple.com/support/code-signing/)
- [Apple 公证流程](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)

### 项目文档

- [macOS 应用无法打开解决方案](../../docs/macOS应用无法打开解决方案.md)
- [Tauri 开发指南](./TAURI_DEVELOPMENT_GUIDE.md)
- [Tauri 部署指南](./TAURI_DEPLOYMENT_GUIDE.md)

## 📝 总结

### 当前配置（开发签名）

✅ 本地开发和测试
✅ 个人使用
⚠️ 需要手动允许运行

### 推荐升级（分发签名）

💰 需要 Apple Developer 账号 ($99/年)
🚀 无缝分发给其他用户
🔒 完整的安全保障
📦 支持应用商店分发

---

**最后更新**: 2025-10-27
**适用版本**: Tauri 2.x
