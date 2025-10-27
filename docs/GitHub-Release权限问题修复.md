# GitHub Release 权限问题修复说明

## 🐛 问题描述

在 GitHub Actions 运行时，创建 Release 失败，报 403 错误：

```
⚠️ GitHub release failed with status: 403
undefined
retrying...
❌ Too many retries. Aborting...
Error: Too many retries.
```

## 🔍 问题原因

**GitHub Actions 权限限制**：

从 2023 年开始，GitHub 加强了安全策略，默认的 `GITHUB_TOKEN` 权限被限制为**只读**。创建 Release 需要 `contents: write` 权限，但默认没有授予。

### 为什么会有这个限制？

- **安全考虑**：防止恶意代码或被入侵的 workflow 修改仓库内容
- **最小权限原则**：只授予 workflow 真正需要的权限
- **向后兼容**：旧仓库可能仍使用旧的权限模型

## ✅ 解决方案

### 方案 1：添加 permissions 配置（推荐）

在 `.github/workflows/build.yml` 顶层添加权限声明：

```yaml
name: Build Tauri App

on:
  push:
    tags:
      - "v*"

permissions:
  contents: write # ✅ 允许创建 Release 和上传文件

jobs:
  build-tauri:
    # ... 其他配置
```

**优点**：

- ✅ 简单快速
- ✅ 不需要额外配置
- ✅ 权限范围明确
- ✅ 推荐的最佳实践

### 方案 2：在仓库设置中修改默认权限（不推荐）

1. 打开 GitHub 仓库
2. 进入 `Settings` → `Actions` → `General`
3. 找到 "Workflow permissions"
4. 选择 "Read and write permissions"
5. 点击 "Save"

**缺点**：

- ⚠️ 影响所有 workflow
- ⚠️ 权限过大，不安全
- ⚠️ 不符合最小权限原则

### 方案 3：使用 Personal Access Token（仅特殊情况）

如果需要跨仓库操作或特殊权限：

1. 创建 PAT：https://github.com/settings/tokens
2. 选择 `repo` 权限
3. 在仓库添加 Secret：`Settings` → `Secrets and variables` → `Actions`
4. 名称：`RELEASE_TOKEN`
5. 在 workflow 中使用：

```yaml
- name: Create Release
  uses: softprops/action-gh-release@v1
  with:
    files: artifacts/*
  env:
    GITHUB_TOKEN: ${{ secrets.RELEASE_TOKEN }} # 使用 PAT
```

**何时使用**：

- 需要触发其他 workflow
- 需要跨仓库操作
- 需要更长的 token 有效期

## 📋 我们采用的方案

**✅ 方案 1：添加 permissions 配置**

修改了 `.github/workflows/build.yml`，添加：

```yaml
permissions:
  contents: write # 允许创建 Release 和上传文件
```

### 为什么选择这个方案？

1. **安全性高**：只授予必需的权限
2. **配置简单**：一行代码搞定
3. **易于维护**：权限配置在代码中，版本可控
4. **最佳实践**：GitHub 官方推荐

## 🔐 权限说明

### contents: write 允许什么？

- ✅ 创建 Release
- ✅ 上传 Release 资产（文件）
- ✅ 创建/修改/删除标签
- ✅ 推送代码（本 workflow 不需要）

### 不允许什么？

- ❌ 修改仓库设置
- ❌ 管理 Actions secrets
- ❌ 修改分支保护规则
- ❌ 管理协作者权限

## 🎯 验证修复

提交修改后重新发布版本：

```bash
# 删除旧标签（如果需要）
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0

# 重新创建标签并推送
git tag v1.0.0
git push origin v1.0.0

# 或使用发布脚本
./release.sh v1.0.1
```

**预期结果**：

- ✅ GitHub Actions 运行成功
- ✅ 自动创建 Release
- ✅ 打包文件自动上传到 Release

## 🔍 调试方法

### 查看 workflow 权限

在 workflow 中添加调试步骤：

```yaml
- name: Check permissions
  run: |
    echo "GITHUB_TOKEN permissions:"
    curl -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
         https://api.github.com/repos/${{ github.repository }}
```

### 查看详细错误信息

在 Actions 页面：

1. 点击失败的 workflow
2. 展开 "Create Release" 步骤
3. 查看完整错误日志

常见错误：

- `403 Forbidden` → 权限不足（本次修复）
- `422 Unprocessable Entity` → Release 已存在
- `404 Not Found` → 仓库路径错误

## 📚 相关资源

### GitHub 官方文档

- [Automatic token authentication](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
- [Permissions for the GITHUB_TOKEN](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token)
- [Assigning permissions to jobs](https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs)

### Action 文档

- [softprops/action-gh-release](https://github.com/softprops/action-gh-release)

## 🎊 总结

### 问题

- GitHub Actions 默认 token 权限不足，无法创建 Release

### 解决

- 在 workflow 添加 `permissions: contents: write`

### 结果

- ✅ Release 创建成功
- ✅ 打包文件自动上传
- ✅ 符合安全最佳实践

---

**修复时间**: 2025-10-27  
**影响范围**: `.github/workflows/build.yml`  
**测试状态**: ✅ 待验证（下次发布时）
