# 🚀 Tauri 迁移执行指南

## ✅ 第一阶段完成：环境配置

```
✅ Node.js: v24.4.0
✅ npm: 11.4.2
✅ Rust: 1.90.0 (via Homebrew)
✅ Cargo: 1.90.0
```

### 环境配置永久化

为了在后续会话中保持 Rust 环境可用，请运行以下命令：

```bash
# 添加 Rust 到 shell 配置
echo 'source $HOME/.cargo/env' >> ~/.zshrc
source ~/.zshrc
```

验证：
```bash
rustc --version && cargo --version
```

---

## 🎯 第二阶段：立即开始

### 选项 A: 创建新项目（推荐）

```bash
# 1. 运行初始化脚本
./INIT_TAURI_PROJECT.sh

# 2. 进入项目目录
cd tauri-app

# 3. 启动开发服务器
npm run dev
```

### 选项 B: 手动创建项目

```bash
# 使用 npm 官方工具创建
npm create tauri-app@latest my-app -- \
    --manager npm \
    --ui react \
    --skip-git

cd my-app
npm run dev
```

---

## 📚 迁移路线图

### Week 1: 原型验证

```
Day 1-2: 学习 Rust 基础
  - 阅读: https://www.rust-lang.org/learn
  - 教程: 20-30 分钟快速上手

Day 3-4: 实现登录功能
  - 参考: docs/Tauri迁移方案.md 第二阶段
  - 代码: src-tauri/src/auth.rs
  - 测试: 本地登录

Day 5: 实现上传功能
  - 参考: docs/Tauri迁移方案.md 第三阶段
  - 测试: 文件选择 + 上传
```

### Week 2-3: 功能完整

```
Week 2: Excel 解析迁移
  - 参考: docs/Tauri迁移方案.md 第四阶段
  - 库: calamine crate
  - 测试: Excel 文件解析

Week 3: 界面优化
  - React 组件打磨
  - CSS 样式优化
  - 用户交互测试
```

### Week 4: 发布准备

```
跨平台测试:
  - macOS: cargo tauri build
  - Windows: 如可用则测试
  
CI/CD 配置:
  - GitHub Actions 多平台打包
  - 自动化构建流程
```

---

## 💻 立即尝试的命令

### 方式 1: 快速体验

```bash
# 创建最小项目
npm create tauri-app@latest demo -- \
    --manager npm \
    --ui react \
    --skip-git

cd demo

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

**预期结果**:
- ✅ 应用窗口打开
- ✅ "Hello Tauri" 页面显示
- ✅ 下方有按钮和输入框可交互

### 方式 2: 从本项目迁移

1. 备份现有代码:
```bash
git checkout -b tauri-migration
```

2. 初始化 Tauri:
```bash
./INIT_TAURI_PROJECT.sh
```

3. 复制业务逻辑:
   - Python 代码 → Rust (src-tauri/src/)
   - PyQt UI 代码 → React (src/components/)

4. 修改 API 调用:
   - 直接 HTTP 改为 Tauri IPC
   - 参考 TAURI_QUICKSTART.md

---

## 🔧 常见命令速查

```bash
# 开发时使用
npm run dev              # 启动开发服务器 (热加载)
npm run build            # 构建前端资源
cargo tauri dev          # 等同于上面

# 生产时使用
cargo tauri build        # 编译生产版本
npm run tauri build      # npm 方式

# 代码检查
cargo check              # 检查 Rust 代码
cargo clippy             # Rust linter
npm run lint             # JavaScript linter

# 清理构建
cargo clean              # 清理 Rust 构建
rm -rf dist/             # 清理前端构建
```

---

## 📖 核心文档导航

| 文档 | 用途 | 阶段 |
|------|------|------|
| **TAURI_QUICKSTART.md** | 30 分钟快速上手 | Week 1 Day 1 |
| **docs/Tauri迁移方案.md** | 详细迁移指南 + 完整代码 | Week 1-4 |
| **docs/方案对比分析.md** | 技术对比和决策依据 | 决策阶段 |
| **CHECKLIST.md** | 逐步检查清单 | 全程 |

---

## 🆘 问题排查

### 问题 1: "command not found: rustc"

**解决**:
```bash
source $HOME/.cargo/env
rustc --version  # 应该输出版本号
```

### 问题 2: npm 依赖安装超时

**解决**:
```bash
# 使用国内镜像
npm config set registry https://registry.npmmirror.com
npm install
```

### 问题 3: Tauri 窗口不显示

**检查**:
- [ ] 是否运行了 npm run dev?
- [ ] 控制台有无错误信息?
- [ ] Rust 代码是否编译成功?

**解决**:
```bash
cargo clean
npm install
npm run dev
```

### 问题 4: IPC 通信失败

**检查**:
- [ ] Rust 函数是否有 #[tauri::command] 宏?
- [ ] 是否在 generate_handler! 中注册?
- [ ] JavaScript 中是否用 invoke() 调用?

**参考**: TAURI_QUICKSTART.md 的代码示例

---

## 🎯 今天就能完成

### 15 分钟版本
```bash
./INIT_TAURI_PROJECT.sh
cd tauri-app
npm run dev
```

### 1 小时版本
```bash
# 按上面命令启动后
# 修改 src/App.jsx 中的文本
# 看到自动刷新（热加载）
# 修改 src-tauri/src/main.rs 中的逻辑
# 看到 Rust 重新编译
```

### 3 小时版本
```bash
# 按 TAURI_QUICKSTART.md 完整步骤
# 实现登录功能
# 实现文件选择
# 运行 cargo tauri build 生成可执行文件
```

---

## 📊 预期时间表

| 任务 | 耗时 | 难度 |
|------|------|------|
| 环境配置 | ✅ 已完成 | 简单 |
| 创建项目 | 15 分钟 | 简单 |
| 学习 Rust 基础 | 1-2 天 | 中等 |
| 实现登录 | 1-2 天 | 中等 |
| 实现上传 | 2-3 天 | 中等 |
| Excel 解析 | 2-3 天 | 中等 |
| 优化打磨 | 1-2 天 | 简单 |
| **总计** | **1-2 周** | **可完成** |

---

## 🎉 下一步行动

### 现在就做（5 分钟）
```bash
# 1. 设置环境变量永久化
echo 'source $HOME/.cargo/env' >> ~/.zshrc

# 2. 创建你的第一个 Tauri 项目
./INIT_TAURI_PROJECT.sh

# 3. 启动开发服务器
cd tauri-app && npm run dev
```

### 第一天（1-3 小时）
- [ ] 完整阅读 TAURI_QUICKSTART.md
- [ ] 尝试修改示例代码
- [ ] 理解 IPC 通信机制
- [ ] 体验热加载开发流程

### 第一周（40-60 小时）
- [ ] 学习 Rust 基础（15-20h）
- [ ] 迁移认证模块（10-15h）
- [ ] 迁移上传模块（10-15h）
- [ ] 测试和优化（5-10h）

---

## 📞 卡住了怎么办

按优先级检查:
1. 本项目文档 (docs/ 目录)
2. TAURI_QUICKSTART.md 的"常见问题"部分
3. Tauri 官方文档: https://tauri.app
4. GitHub Issues: https://github.com/tauri-apps/tauri/issues
5. 社区论坛: https://github.com/tauri-apps/tauri/discussions

---

**准备好了吗？现在就运行 `./INIT_TAURI_PROJECT.sh` 开始吧！** 🚀
