# Windows 打包中文问题修复说明

## 🐛 问题描述

Windows MSI 打包时 WiX 工具失败：

```
failed to bundle project `failed to run C:\Users\runneradmin\AppData\Local\tauri\WixTools314\light.exe`
```

**根本原因**：WiX 3.x 打包工具不支持中文 productName，会导致生成的文件路径包含中文字符而失败。

## ✅ 解决方案

### 修改配置文件

在 `tauri-app/src-tauri/tauri.conf.json` 中：

```json
{
  "productName": "molten-salt-upload", // ✅ 改为英文（用于文件系统）
  "app": {
    "windows": [
      {
        "title": "熔盐管理文件上传工具" // ✅ 保持中文（用户看到的标题）
      }
    ]
  }
}
```

## 📋 影响说明

### ✅ 不受影响（用户体验）

- **窗口标题**：仍然显示"熔盐管理文件上传工具"（中文）
- **界面文字**：所有界面文字保持中文
- **功能**：完全不受影响

### 🔄 变化（文件系统）

- **安装文件名**：从 `熔盐管理文件上传工具_0.1.0_x64_en-US.msi` 改为 `molten-salt-upload_0.1.0_x64_en-US.msi`
- **安装路径**：从 `C:\Program Files\熔盐管理文件上传工具` 改为 `C:\Program Files\molten-salt-upload`
- **可执行文件名**：从 `熔盐管理文件上传工具.exe` 改为 `molten-salt-upload.exe`

## 🎯 为什么这样做？

1. **WiX 限制**：WiX 3.x 是 Windows 安装包的标准工具，但对 Unicode/中文支持不完善
2. **最佳实践**：文件系统路径使用英文是跨平台应用的标准做法
3. **兼容性**：避免在某些 Windows 系统上出现编码问题
4. **用户体验**：通过 `title` 字段保持中文界面，用户看到的仍然是中文

## 📦 打包后的文件结构

### Windows

```
molten-salt-upload_0.1.0_x64_en-US.msi
└── 安装到：C:\Program Files\molten-salt-upload\
    └── molten-salt-upload.exe  (运行时窗口标题显示"熔盐管理文件上传工具")
```

### macOS

```
molten-salt-upload.app  (应用名称可通过 Info.plist 设置为中文显示)
```

## 🚀 验证

下次 CI/CD 构建时：

- ✅ Windows MSI 打包会成功
- ✅ 生成的文件名为 `molten-salt-upload_0.1.0_x64_en-US.msi`
- ✅ 用户运行后看到的窗口标题仍然是"熔盐管理文件上传工具"

## 📝 备注

- 这是 Tauri/WiX 工具的限制，不是我们代码的问题
- 主流桌面应用都采用这种方式（内部英文名，显示中文名）
- 如需修改显示名称，修改 `app.windows[0].title` 字段即可
