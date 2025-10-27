# Gitee 快速开始

> 3 步配置 Gitee 仓库和双远程同步

**创建时间**: 2025 年 10 月 26 日  
**适用场景**: 国内用户，需要 Gitee 加速访问

---

## 🎯 目标

- ✅ 配置 Gitee 作为国内镜像
- ✅ 同时推送到 GitHub 和 Gitee
- ✅ 使用 GitHub Actions 自动打包
- ✅ （可选）同步 Release 到 Gitee

---

## 📋 前提条件

- ✅ 已有 GitHub 仓库
- ✅ 已配置 GitHub Actions（参考 [CI-CD 快速开始.md](./CI-CD快速开始.md)）
- ✅ 有 Gitee 账号

---

## 🚀 快速开始（3 步）

### 步骤 1: 在 Gitee 创建仓库

1. 访问 [Gitee](https://gitee.com)
2. 点击右上角 "+" → "新建仓库"
3. 填写仓库信息：
   - 仓库名称：`熔盐管理文件上传工具`（或其他名称）
   - 路径：自动生成
   - 开源：选择公开或私有
   - 初始化：**不要勾选**任何选项
4. 点击"创建"

### 步骤 2: 配置 Gitee 远程仓库

在项目根目录运行：

```bash
# 方式 A: 使用配置脚本（推荐）
./setup-gitee.sh

# 方式 B: 手动配置
git remote add gitee https://gitee.com/your-username/your-repo.git

# 验证配置
git remote -v
```

应该看到类似输出：

```
origin  https://github.com/your-username/your-repo.git (fetch)
origin  https://github.com/your-username/your-repo.git (push)
gitee   https://gitee.com/your-username/your-repo.git (fetch)
gitee   https://gitee.com/your-username/your-repo.git (push)
```

### 步骤 3: 推送代码到 Gitee

```bash
# 首次推送（推送所有内容）
git push gitee main --all --tags

# 日常推送（推送到所有远程仓库）
./push-all.sh --with-tags
```

---

## ✅ 验证

访问你的 Gitee 仓库，应该能看到：

- ✅ 所有代码文件
- ✅ 所有提交记录
- ✅ 所有标签

---

## 📝 日常使用

### 推送代码

```bash
# 推送到所有远程仓库（GitHub + Gitee）
./push-all.sh

# 推送并包含标签
./push-all.sh --with-tags

# 只推送到 GitHub
git push origin main

# 只推送到 Gitee
git push gitee main
```

### 发布新版本

```bash
# 1. 创建并推送标签（会触发 GitHub Actions）
./release.sh v1.0.0

# 2. 等待 GitHub Actions 构建完成
# 访问: https://github.com/your-username/your-repo/actions

# 3. （可选）同步 Release 到 Gitee
./sync-release-to-gitee.sh v1.0.0
```

---

## 🔄 工作流程

```
┌─────────────────────────────────────────────────┐
│  1. 本地开发                                    │
│     git commit -m "feat: 新功能"                │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  2. 推送到所有远程仓库                          │
│     ./push-all.sh                               │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
  ┌─────────┐         ┌─────────┐
  │ GitHub  │         │ Gitee   │
  │ (主仓库)│         │ (镜像)  │
  └────┬────┘         └─────────┘
       │
       ▼
  ┌─────────────────┐
  │ GitHub Actions  │
  │ (自动打包)      │
  └────┬────────────┘
       │
       ▼
  ┌─────────────────┐
  │ GitHub Release  │
  │ (下载地址)      │
  └─────────────────┘
```

---

## 💡 最佳实践

### 1. 推送策略

```bash
# ✅ 推荐：日常开发推送到所有仓库
./push-all.sh

# ✅ 发布版本时包含标签
./push-all.sh --with-tags

# ⚠️  不推荐：只推送到单个仓库（容易忘记同步）
git push origin main
```

### 2. CI/CD 策略

```
主 CI/CD: GitHub Actions（免费且强大）
   ├─ 自动构建所有平台
   ├─ 自动创建 Release
   └─ 自动上传构建产物

Gitee: 仅作为镜像
   ├─ 加速国内访问
   ├─ 备份代码
   └─ （可选）手动同步 Release
```

### 3. Release 策略

**方案 A: GitHub Release 为主（推荐）**

```bash
# 1. 使用 GitHub Actions 自动打包
./release.sh v1.0.0

# 2. 用户从 GitHub Release 下载
# 国内用户可能需要加速工具
```

**方案 B: 同步到 Gitee Release**

```bash
# 1. 自动打包（GitHub Actions）
./release.sh v1.0.0

# 2. 同步到 Gitee
./sync-release-to-gitee.sh v1.0.0

# 3. 用户可以选择：
#    - GitHub Release（国际用户）
#    - Gitee Release（国内用户）
```

---

## 🛠️ 高级配置

### 自动同步到 Gitee

创建 GitHub Action 自动同步：

```yaml
# .github/workflows/sync-to-gitee.yml
name: 同步到 Gitee

on:
  push:
    branches: [main]

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: 同步到 Gitee
        uses: wearerequired/git-mirror-action@v1
        env:
          SSH_PRIVATE_KEY: ${{ secrets.GITEE_PRIVATE_KEY }}
        with:
          source-repo: "git@github.com:your-username/your-repo.git"
          destination-repo: "git@gitee.com:your-username/your-repo.git"
```

配置步骤：

1. 生成 SSH 密钥：`ssh-keygen -t rsa -b 4096`
2. 将公钥添加到 Gitee SSH 设置
3. 将私钥添加到 GitHub Secrets（`GITEE_PRIVATE_KEY`）

---

## ❓ 常见问题

### Q1: 推送到 Gitee 失败？

```bash
# 错误: Permission denied
# 解决方案：
# 1. 检查 Gitee 地址是否正确
git remote -v

# 2. 检查是否有推送权限
# 访问 Gitee 仓库设置 → 成员管理

# 3. 尝试使用 HTTPS 地址
git remote set-url gitee https://gitee.com/your-username/your-repo.git
```

### Q2: 如何只在 Gitee 查看代码？

Gitee 是完整的镜像，可以：

- ✅ 查看所有代码
- ✅ 浏览提交记录
- ✅ 下载源代码
- ❌ 不要在 Gitee 上直接提交（会导致同步问题）

### Q3: 忘记推送到 Gitee 怎么办？

```bash
# 同步最新代码到 Gitee
git push gitee main --force
git push gitee --tags --force

# 或使用脚本
./push-all.sh --with-tags
```

### Q4: 如何删除 Gitee 配置？

```bash
# 删除 Gitee 远程仓库
git remote remove gitee

# 验证
git remote -v
```

---

## 📚 相关文档

- **[Gitee-CI-CD 配置指南.md](./Gitee-CI-CD配置指南.md)** - 详细的 Gitee CI/CD 方案
- **[CI-CD 快速开始.md](./CI-CD快速开始.md)** - GitHub Actions 配置
- **[打包指南.md](./打包指南.md)** - 本地打包方法

---

## 🎉 完成

现在你已经配置好了 Gitee 镜像！

**推荐的工作流程**:

```bash
# 1. 日常开发
git commit -m "feat: 新功能"

# 2. 推送到所有仓库
./push-all.sh

# 3. 发布新版本
./release.sh v1.0.0

# 4. （可选）同步到 Gitee
./sync-release-to-gitee.sh v1.0.0
```

---

**创建时间**: 2025 年 10 月 26 日  
**版本**: v1.0  
**维护者**: 熔盐管理项目团队
