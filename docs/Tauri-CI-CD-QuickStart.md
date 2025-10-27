# Tauri 应用 CI/CD 快速开始

> 🎯 5 分钟配置自动打包和代码签名

## 📋 前置条件

- ✅ macOS 系统（用于本地开发和证书导出）
- ✅ Apple 开发者证书（免费 Apple ID 即可）
- ✅ GitHub 账号和仓库
- ✅ 已安装 Tauri 开发环境

## 🚀 快速配置流程

### 步骤 1: 验证本地证书 (1 分钟)

```bash
# 查看可用的签名证书
security find-identity -v -p codesigning
```

应该看到类似输出：

```
1) 19954703... "Apple Development: yinzhen ye (B7U63QS5Y7)"
```

如果没有证书，先在 Xcode 中登录 Apple ID 自动生成。

### 步骤 2: 配置本地签名 (1 分钟)

已完成 ✅ - 项目已配置好本地签名：

```json
// tauri-app/src-tauri/tauri.conf.json
"macOS": {
  "signingIdentity": "Apple Development: yinzhen ye (B7U63QS5Y7)"
}
```

### 步骤 3: 导出证书 (2 分钟)

```bash
# 导出证书（会提示输入密码）
security export -k login.keychain -t identities -f pkcs12 -o certificate.p12

# 转换为 Base64
base64 -i certificate.p12 -o certificate.p12.base64

# 查看内容（用于下一步）
cat certificate.p12.base64
```

### 步骤 4: 配置 GitHub Secrets (2 分钟)

1. 访问 GitHub 仓库 → **Settings** → **Secrets and variables** → **Actions**

2. 点击 **New repository secret**，添加以下 4 个 secrets：

   **Secret 1: APPLE_CERTIFICATE**

   - Value: 粘贴 `certificate.p12.base64` 的完整内容

   **Secret 2: APPLE_CERTIFICATE_PASSWORD**

   - Value: 导出证书时设置的密码

   **Secret 3: KEYCHAIN_PASSWORD**

   - Value: 任意设置一个强密码（例如：`CI_Key_2025`）

   **Secret 4: APPLE_SIGNING_IDENTITY**

   - Value: `Apple Development: yinzhen ye (B7U63QS5Y7)`

3. 清理本地证书文件：
   ```bash
   rm certificate.p12 certificate.p12.base64
   ```

### 步骤 5: 推送代码并测试 (1 分钟)

```bash
# 提交配置更改
git add .
git commit -m "配置 Tauri 代码签名和 CI/CD"
git push

# 创建测试标签
git tag v1.0.0
git push origin v1.0.0
```

### 步骤 6: 查看构建结果

1. 访问 GitHub 仓库 → **Actions** 标签
2. 查看 "Build Tauri App" 工作流运行状态
3. 等待约 15-20 分钟完成构建
4. 访问 **Releases** 页面下载安装包

## 🎉 完成！

现在每次推送标签时，GitHub Actions 会自动：

- ✅ 构建 macOS 和 Windows 版本
- ✅ 为 macOS 应用签名
- ✅ 生成安装包（DMG、MSI、EXE）
- ✅ 创建 GitHub Release
- ✅ 上传所有安装包

## 🔧 下载后无法打开应用？

使用项目提供的修复脚本：

```bash
# 方法 1: 自动查找并修复
./fix-macos-app.sh auto

# 方法 2: 手动修复下载的应用
./fix-macos-app.sh "path/to/molten-salt-upload.app"

# 方法 3: 直接命令修复
xattr -cr "molten-salt-upload.app"
```

## 📊 文件结构

```
熔盐管理文件上传工具/
├── .github/
│   └── workflows/
│       └── build-tauri.yml          # CI/CD 配置 ✅
├── tauri-app/
│   ├── src-tauri/
│   │   ├── tauri.conf.json          # Tauri 配置（已添加签名） ✅
│   │   └── entitlements.plist       # macOS 权限配置 ✅
│   └── docs/
│       └── TAURI_CODESIGN_GUIDE.md  # 详细签名指南 ✅
├── docs/
│   ├── GitHub-Secrets配置指南.md    # Secrets 配置详解 ✅
│   └── macOS应用无法打开解决方案.md  # 问题解决方案 ✅
└── fix-macos-app.sh                 # 快速修复脚本 ✅
```

## 📚 详细文档

- **完整配置**: [Tauri 代码签名配置指南](../tauri-app/docs/TAURI_CODESIGN_GUIDE.md)
- **Secrets 配置**: [GitHub Secrets 配置指南](./GitHub-Secrets配置指南.md)
- **问题解决**: [macOS 应用无法打开解决方案](./macOS应用无法打开解决方案.md)
- **开发指南**: [Tauri 开发指南](../tauri-app/docs/TAURI_DEVELOPMENT_GUIDE.md)

## 🎯 下一步

### 本地开发和测试

```bash
# 开发模式
cd tauri-app
npm run tauri dev

# 本地构建（会自动签名）
npm run tauri build

# 构建通用二进制（支持 Intel 和 Apple Silicon）
npm run tauri build -- --target universal-apple-darwin
```

### 发布新版本

```bash
# 使用发布脚本（推荐）
./release.sh v1.0.1

# 或手动操作
git tag v1.0.1
git push origin v1.0.1
```

### 版本号规范

遵循语义化版本：`v主版本.次版本.修订号`

- `v1.0.0` - 首个正式版本
- `v1.0.1` - Bug 修复
- `v1.1.0` - 新增功能
- `v2.0.0` - 重大变更

## ⚠️ 常见问题

### Q: 本地构建的应用可以打开，CI/CD 的不行？

**A:** CI/CD 打包的应用被标记为"从网络下载"，需要移除隔离属性：

```bash
./fix-macos-app.sh auto
```

### Q: GitHub Actions 构建失败？

**A:** 检查配置：

1. 确认所有 4 个 Secrets 都已正确添加
2. 验证 `APPLE_CERTIFICATE` 是完整的 Base64 字符串
3. 检查 `APPLE_SIGNING_IDENTITY` 与本地证书名称一致
4. 查看 Actions 日志获取详细错误信息

### Q: 需要分发给其他用户怎么办？

**A:** 当前使用的是开发签名，分发给他人时：

- 用户需要右键点击 → 打开
- 或使用 `xattr -cr` 命令移除隔离

如需无缝分发，建议升级到 Developer ID + 公证（需要 $99/年 Apple Developer 账号）。

### Q: 如何更新签名证书？

**A:** 当证书过期或需要更换时：

1. 删除旧证书文件
2. 重新执行步骤 3-4
3. 更新 `tauri.conf.json` 中的 `signingIdentity`
4. 更新 GitHub Secrets

### Q: 能不能不签名？

**A:** 可以，但：

- ❌ 每次打开都需要手动允许
- ❌ macOS 10.15+ 会严格限制
- ❌ 用户体验差
- ✅ 签名配置只需 5 分钟，强烈建议配置

## 🔐 安全提示

1. **立即删除导出的证书文件**：

   ```bash
   rm certificate.p12 certificate.p12.base64
   ```

2. **不要提交证书到 Git**：

   - 已在 `.gitignore` 中排除 `*.p12` 和 `*.p12.base64`

3. **定期更换密码**：

   - 每年更新证书时，同时更新 GitHub Secrets

4. **最小权限原则**：
   - 只在需要的 workflow 中使用 Secrets
   - 不要在日志中打印敏感信息

## 🎓 学习资源

### 官方文档

- [Tauri 官方指南](https://tauri.app/v1/guides/)
- [Apple 代码签名](https://developer.apple.com/support/code-signing/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

### 项目资源

- [项目 README](../README.md)
- [快速参考](../快速参考.md)
- [打包指南](../打包指南.md)

## 💡 提示

- 首次配置可能需要 10 分钟
- 之后每次发布只需 1 分钟（创建标签）
- CI/CD 构建时间约 15-20 分钟
- 可以同时构建多个平台（macOS、Windows）

---

**配置完成时间**: 5 分钟  
**首次构建时间**: 15-20 分钟  
**后续发布时间**: 1 分钟

🎉 **享受自动化带来的便利！**
