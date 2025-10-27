# GitHub Secrets 配置指南

本指南介绍如何配置 GitHub Secrets，以支持 Tauri 应用的自动签名和发布。

## 📋 需要配置的 Secrets

为了在 GitHub Actions 中自动签名 macOS 应用，需要配置以下 4 个 Secrets：

| Secret 名称                  | 用途                    | 是否必需 |
| ---------------------------- | ----------------------- | -------- |
| `APPLE_CERTIFICATE`          | 开发证书（Base64 编码） | ✅ 必需  |
| `APPLE_CERTIFICATE_PASSWORD` | 证书导出密码            | ✅ 必需  |
| `KEYCHAIN_PASSWORD`          | CI 临时钥匙串密码       | ✅ 必需  |
| `APPLE_SIGNING_IDENTITY`     | 签名身份名称            | ✅ 必需  |

## 🔧 步骤 1：导出开发证书

### 1.1 查看可用证书

```bash
# 列出所有可用的代码签名证书
security find-identity -v -p codesigning
```

输出示例：

```
1) 19954703843188B03F6C909CD2589C9ED406CD06 "Apple Development: yinzhen ye (B7U63QS5Y7)"
   1 valid identities found
```

记录完整的证书名称：`Apple Development: yinzhen ye (B7U63QS5Y7)`

### 1.2 从钥匙串导出证书

**方法 1：使用命令行（推荐）**

```bash
# 导出证书为 p12 格式（会提示输入密码）
security export -k login.keychain -t identities -f pkcs12 -o certificate.p12

# 按提示：
# 1. 输入钥匙串密码（Mac 登录密码）
# 2. 设置导出密码（记住这个密码，后续需要用）
# 3. 再次输入导出密码确认
```

**方法 2：使用钥匙串访问应用**

1. 打开 **钥匙串访问** (Keychain Access)
2. 在左侧选择 **登录** → **我的证书**
3. 找到 `Apple Development: yinzhen ye` 证书
4. 右键点击 → **导出**
5. 选择文件格式：**个人信息交换 (.p12)**
6. 保存为 `certificate.p12`
7. 输入导出密码（记住这个密码）

### 1.3 转换为 Base64 编码

```bash
# 将 p12 文件编码为 base64
base64 -i certificate.p12 -o certificate.p12.base64

# 查看编码后的内容
cat certificate.p12.base64
```

输出将是一长串 Base64 字符串，类似：

```
MIIKpAIBAzCCCl4GCSqGSIb3DQEHAaCCCk8EggpLMIIKRzCCBXcGCSqGSIb3DQEH...
(很长的字符串)
...
```

## 🔐 步骤 2：配置 GitHub Secrets

### 2.1 访问 GitHub 仓库设置

1. 打开你的 GitHub 仓库
2. 点击 **Settings** (设置)
3. 在左侧菜单找到 **Secrets and variables** → **Actions**
4. 点击 **New repository secret** (新建仓库密钥)

### 2.2 添加 Secret 1: APPLE_CERTIFICATE

- **Name**: `APPLE_CERTIFICATE`
- **Value**: 粘贴 `certificate.p12.base64` 的完整内容
  - 打开 `certificate.p12.base64` 文件
  - 复制所有内容（整个 Base64 字符串）
  - 粘贴到 Value 字段

点击 **Add secret** 保存。

### 2.3 添加 Secret 2: APPLE_CERTIFICATE_PASSWORD

- **Name**: `APPLE_CERTIFICATE_PASSWORD`
- **Value**: 导出 p12 证书时设置的密码
  - 例如：`YourP@ssw0rd123`

点击 **Add secret** 保存。

### 2.4 添加 Secret 3: KEYCHAIN_PASSWORD

- **Name**: `KEYCHAIN_PASSWORD`
- **Value**: 用于 CI 临时钥匙串的密码（任意设置）
  - 例如：`CI_Keychain_Pass_2025`
  - 这个密码只在 CI 环境中使用，可以随意设置

点击 **Add secret** 保存。

### 2.5 添加 Secret 4: APPLE_SIGNING_IDENTITY

- **Name**: `APPLE_SIGNING_IDENTITY`
- **Value**: 证书的完整名称
  - 复制步骤 1.1 中查到的完整名称
  - 例如：`Apple Development: yinzhen ye (B7U63QS5Y7)`

点击 **Add secret** 保存。

## ✅ 步骤 3：验证配置

### 3.1 检查 Secrets 列表

在 **Settings** → **Secrets and variables** → **Actions** 页面，应该看到 4 个 secrets：

- ✅ `APPLE_CERTIFICATE`
- ✅ `APPLE_CERTIFICATE_PASSWORD`
- ✅ `KEYCHAIN_PASSWORD`
- ✅ `APPLE_SIGNING_IDENTITY`

### 3.2 测试自动打包

```bash
# 创建测试标签
git tag v1.0.0-test

# 推送标签触发 CI/CD
git push origin v1.0.0-test
```

### 3.3 查看 Actions 运行状态

1. 在 GitHub 仓库点击 **Actions** 标签
2. 查看 "Build Tauri App" 工作流运行状态
3. 点击进入查看详细日志

#### 成功的标志

在 "Import Code Signing Certificate (macOS)" 步骤中，应该看到：

```
1) XXXX... "Apple Development: yinzhen ye (B7U63QS5Y7)"
   1 valid identities found
```

在 "Build Tauri App (macOS)" 步骤中，应该看到：

```
Finished release [optimized] target(s)
Signing with identity "Apple Development: yinzhen ye (B7U63QS5Y7)"
```

#### 常见错误

**错误 1**: `security: SecKeychainItemImport: The user name or passphrase you entered is not correct`

- **原因**: `APPLE_CERTIFICATE_PASSWORD` 不正确
- **解决**: 重新导出证书，确保密码正确

**错误 2**: `No signing identity found`

- **原因**: 证书导入失败或 `APPLE_SIGNING_IDENTITY` 不匹配
- **解决**: 检查 Base64 编码是否完整，验证身份名称

**错误 3**: `Code signing error`

- **原因**: 权限配置或证书类型问题
- **解决**: 确保使用的是开发证书，检查 entitlements.plist

## 📦 步骤 4：发布新版本

配置完成后，每次需要发布新版本时：

```bash
# 使用项目提供的发布脚本
./release.sh v1.0.0

# 或手动操作
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions 会自动：

1. ✅ 检出代码
2. ✅ 设置 Node.js 和 Rust 环境
3. ✅ 导入签名证书
4. ✅ 构建并签名应用
5. ✅ 上传构建产物
6. ✅ 创建 GitHub Release
7. ✅ 附加安装包到 Release

## 🔒 安全最佳实践

### 保护证书文件

```bash
# 导出证书后，立即删除本地文件
rm certificate.p12
rm certificate.p12.base64

# 或移动到安全位置
mv certificate.p12 ~/Documents/Certificates/
chmod 600 ~/Documents/Certificates/certificate.p12
```

### 定期更新证书

- Apple 开发证书有效期通常为 1 年
- 证书过期前需要重新生成和配置
- 设置日历提醒，在过期前 1 个月更新

### 最小权限原则

- Secrets 只在必要的 workflow 中使用
- 不要在日志中打印敏感信息
- 定期审查 Actions 使用情况

## 🆙 升级到 Developer ID（可选）

如果需要公开分发应用，建议升级到 Developer ID 签名：

### 前置条件

1. 注册 [Apple Developer Program](https://developer.apple.com/programs/) ($99/年)
2. 申请 Developer ID Application 证书

### 更新配置

**tauri.conf.json**:

```json
"macOS": {
  "minimumSystemVersion": "10.13",
  "signingIdentity": "Developer ID Application: Your Name (TEAM_ID)",
  "entitlements": null,
  "providerShortName": "TEAM_ID"
}
```

**GitHub Secrets**:

- 更新 `APPLE_SIGNING_IDENTITY` 为新的 Developer ID

### 添加公证支持

在 GitHub Actions 中添加公证步骤，需要额外的 Secrets：

| Secret 名称          | 值                    |
| -------------------- | --------------------- |
| `APPLE_ID`           | your@email.com        |
| `APPLE_TEAM_ID`      | TEAM_ID               |
| `APPLE_APP_PASSWORD` | App-Specific Password |

参考 [Tauri 代码签名指南](../tauri-app/docs/TAURI_CODESIGN_GUIDE.md) 了解详情。

## 📚 相关文档

- [Tauri 代码签名配置指南](../tauri-app/docs/TAURI_CODESIGN_GUIDE.md)
- [macOS 应用无法打开解决方案](./macOS应用无法打开解决方案.md)
- [CI-CD 快速开始](../CI-CD快速开始.md)

## ⚠️ 故障排除

### 问题 1: Base64 编码后文件太大

**现象**: GitHub Secrets 限制为 64KB

**解决方案**:

```bash
# 检查文件大小
ls -lh certificate.p12

# 如果太大，尝试只导出证书（不含私钥链）
security export -k login.keychain \
    -t identities \
    -f pkcs12 \
    -P "" \
    -o certificate.p12 \
    "Apple Development: yinzhen ye (B7U63QS5Y7)"
```

### 问题 2: 多个证书，不确定使用哪个

**解决方案**:

```bash
# 列出详细信息
security find-certificate -c "Apple Development" -p | openssl x509 -text

# 查看有效期
security find-certificate -c "Apple Development" -p | \
    openssl x509 -noout -dates
```

选择有效期最长、最近创建的证书。

### 问题 3: CI 中证书验证失败

**调试步骤**:

1. 在 workflow 中添加调试输出：

```yaml
- name: Debug Certificate
  run: |
    echo "Certificate length: $(echo $APPLE_CERTIFICATE | wc -c)"
    echo "Signing identity: $APPLE_SIGNING_IDENTITY"
  env:
    APPLE_CERTIFICATE: ${{ secrets.APPLE_CERTIFICATE }}
    APPLE_SIGNING_IDENTITY: ${{ secrets.APPLE_SIGNING_IDENTITY }}
```

2. 检查证书是否正确导入：

```yaml
- name: Verify Certificate Import
  run: |
    security find-identity -v -p codesigning $KEYCHAIN_PATH
```

## 📞 获取帮助

如果遇到问题：

1. 查看 [GitHub Actions 运行日志](https://github.com/你的用户名/仓库名/actions)
2. 参考 [Tauri 官方文档](https://tauri.app/v1/guides/distribution/sign-macos)
3. 查看 [Apple 代码签名文档](https://developer.apple.com/support/code-signing/)

---

**最后更新**: 2025-10-27
**适用于**: GitHub Actions + Tauri 2.x
