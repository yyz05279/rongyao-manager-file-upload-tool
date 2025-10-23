# QSizePolicy 错误修复说明

## 修复日期

2025 年 10 月 23 日

## 问题描述

查看日报详情时出现 `AttributeError` 错误：

```
Traceback (most recent call last):
  File "/Users/yyz/Desktop/熔盐管理文件上传工具/ui/daily_report_detail_dialog.py", line 575, in _setup_table_style
    table.sizePolicy().Minimum)
AttributeError: 'QSizePolicy' object has no attribute 'Minimum'
```

## 根本原因

在设置表格的尺寸策略时，使用了错误的语法：

```python
# ❌ 错误的写法
table.setSizePolicy(table.sizePolicy().horizontalPolicy(),
                   table.sizePolicy().Minimum)
```

**问题分析**：

1. `sizePolicy()` 返回的是一个 `QSizePolicy` 对象实例
2. `Minimum` 是 `QSizePolicy.Policy` 枚举的一个值，不是实例的属性
3. 正确的方式应该是使用 `QSizePolicy.Policy.Minimum`

## 修复方案

### 1. 导入 QSizePolicy

**修改前**：

```python
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QGroupBox, QScrollArea, QHeaderView
)
```

**修改后**：

```python
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QGroupBox, QScrollArea, QHeaderView, QSizePolicy  # ✅ 新增
)
```

### 2. 修正尺寸策略设置

**修改前**：

```python
# ❌ 错误：试图从实例访问枚举值
table.setSizePolicy(table.sizePolicy().horizontalPolicy(),
                   table.sizePolicy().Minimum)
```

**修改后**：

```python
# ✅ 正确：使用枚举类型
table.setSizePolicy(QSizePolicy.Policy.Expanding,
                   QSizePolicy.Policy.Minimum)
```

## PyQt6 中的 QSizePolicy

### 枚举值访问方式

在 PyQt6 中，枚举值需要通过枚举类访问：

```python
# ✅ 正确的访问方式
QSizePolicy.Policy.Fixed         # 固定大小
QSizePolicy.Policy.Minimum       # 最小大小
QSizePolicy.Policy.Maximum       # 最大大小
QSizePolicy.Policy.Preferred     # 首选大小
QSizePolicy.Policy.Expanding     # 可扩展
QSizePolicy.Policy.MinimumExpanding  # 最小可扩展
QSizePolicy.Policy.Ignored       # 忽略

# ❌ 错误的访问方式
table.sizePolicy().Fixed         # AttributeError
table.sizePolicy().Minimum       # AttributeError
```

### setSizePolicy 方法

```python
setSizePolicy(horizontal_policy, vertical_policy)
```

**参数**：

- `horizontal_policy`：水平方向的尺寸策略（QSizePolicy.Policy 枚举值）
- `vertical_policy`：垂直方向的尺寸策略（QSizePolicy.Policy 枚举值）

**示例**：

```python
from PyQt6.QtWidgets import QSizePolicy

# 水平方向可扩展，垂直方向使用最小尺寸
widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                    QSizePolicy.Policy.Minimum)

# 固定大小
widget.setSizePolicy(QSizePolicy.Policy.Fixed,
                    QSizePolicy.Policy.Fixed)

# 首选大小
widget.setSizePolicy(QSizePolicy.Policy.Preferred,
                    QSizePolicy.Policy.Preferred)
```

## 修复效果

### 修复前

- ❌ 运行时错误：`AttributeError: 'QSizePolicy' object has no attribute 'Minimum'`
- ❌ 无法打开日报详情对话框
- ❌ 程序崩溃

### 修复后

- ✅ 正常打开日报详情对话框
- ✅ 表格高度正确自适应内容
- ✅ 滚动功能正常工作

## PyQt5 vs PyQt6 差异

在 PyQt5 中，枚举值可以直接通过类访问：

```python
# PyQt5
from PyQt5.QtWidgets import QSizePolicy
widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
```

在 PyQt6 中，需要通过 `.Policy` 访问枚举值：

```python
# PyQt6
from PyQt6.QtWidgets import QSizePolicy
widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
```

**注意**：这是 PyQt6 的重要变更之一，所有枚举类型都需要显式访问枚举成员。

## 修改文件

### 已修改

- `ui/daily_report_detail_dialog.py` - 日报详情对话框

### 修改内容

1. ✅ 导入 `QSizePolicy`
2. ✅ 修正 `setSizePolicy` 的参数为 `QSizePolicy.Policy.Expanding` 和 `QSizePolicy.Policy.Minimum`

## 相关知识

### 常用尺寸策略

| 策略               | 说明                 | 使用场景                 |
| ------------------ | -------------------- | ------------------------ |
| `Fixed`            | 固定大小，不能改变   | 按钮、图标等固定尺寸控件 |
| `Minimum`          | 最小大小，可以扩大   | 标签、最小高度的表格     |
| `Maximum`          | 最大大小，可以缩小   | 限制最大尺寸的控件       |
| `Preferred`        | 首选大小，可以缩放   | 大多数普通控件           |
| `Expanding`        | 可扩展，尽量占用空间 | 文本编辑框、列表等       |
| `MinimumExpanding` | 最小可扩展           | 需要最小尺寸但可扩展     |
| `Ignored`          | 忽略尺寸提示         | 特殊情况                 |

### 我们的使用场景

```python
table.setSizePolicy(QSizePolicy.Policy.Expanding,   # 水平方向可扩展
                   QSizePolicy.Policy.Minimum)      # 垂直方向最小尺寸
```

**解释**：

- **水平方向**：`Expanding` - 表格宽度可以根据窗口大小调整
- **垂直方向**：`Minimum` - 表格高度使用最小尺寸（根据内容计算的高度）

## 测试建议

1. **基本功能测试**

   - ✅ 测试打开日报详情对话框
   - ✅ 验证各个选项卡正常切换
   - ✅ 确认表格内容正确显示

2. **滚动测试**

   - ✅ 测试整体滚动是否流畅
   - ✅ 验证表格没有自己的滚动条
   - ✅ 确认可以滚动查看所有内容

3. **尺寸测试**
   - ✅ 测试窗口大小调整时表格的表现
   - ✅ 验证表格高度是否正确自适应
   - ✅ 确认没有多余的空白区域

## 预防措施

### 1. 代码审查

- 在使用 PyQt6 枚举时，确保通过正确的路径访问
- 查阅官方文档确认 API 变更

### 2. 单元测试

- 为 UI 组件添加基本的单元测试
- 测试关键功能的正常工作

### 3. 错误处理

- 添加适当的 try-except 块
- 提供友好的错误提示

## 参考资料

- [PyQt6 官方文档 - QSizePolicy](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QSizePolicy.html)
- [PyQt6 迁移指南](https://www.riverbankcomputing.com/static/Docs/PyQt6/pyqt5_differences.html)
- [Qt Documentation - QSizePolicy](https://doc.qt.io/qt-6/qsizepolicy.html)
