# Tauri 应用预览功能实现说明

## 概述

参考 Python 应用的完整流程，为 Tauri 应用添加了数据预览功能，实现**选择文件 → 自动解析 → 数据预览 → 勾选上传**的完整工作流。

## Python 应用流程（参考）

```
1. 用户选择 Excel 文件
   ↓
2. 自动调用 preview_data() 解析文件
   ↓
3. 显示数据预览表格（包含：日期、项目、进度、任务数等）
   ↓
4. 用户勾选要上传的日报（支持全选/反选）
   ↓
5. 点击"开始上传 (3/10)"按钮上传选中的日报
```

## 实现的功能

### 1. Excel 自动解析（Rust 后端）

**文件**：`tauri-app/src-tauri/src/excel.rs`

- 使用 `calamine` 库解析 Excel 文件
- 遍历所有工作表（每个工作表通常代表一个日期的日报）
- 提取关键信息：
  - `reportDate`: 日期（从工作表名称）
  - `reporterName`: 项目名称
  - `overallProgress`: 进度状态
  - `taskCount`: 任务数
  - `onSitePersonnelCount`: 人员数
  - `machineryCount`: 机械数
  - `problemCount`: 问题数
  - `weather`: 天气

### 2. Tauri Command

**文件**：`tauri-app/src-tauri/src/main.rs`

```rust
#[tauri::command]
async fn cmd_parse_excel(file_path: String) -> Result<serde_json::Value, String> {
    excel::parse_excel_file(&file_path)
        .map(|data| serde_json::json!({"reports": data}))
}
```

### 3. 前端 API 封装

**文件**：`tauri-app/src/services/api.js`

```javascript
export const excelAPI = {
  parseExcel: (filePath) => safeInvoke("cmd_parse_excel", { filePath }),
};
```

### 4. 数据预览组件

**文件**：`tauri-app/src/components/DataPreview.jsx`

功能：

- 显示解析后的日报列表（表格形式）
- 每行包含勾选框
- 全选/反选按钮
- 进度状态颜色标识（正常/滞后/超前）
- 问题数高亮显示

表格列：
| 列名 | 说明 |
|------|------|
| ✓ | 勾选框 |
| 日期 | 报表日期 |
| 项目名称 | 填报人/项目名 |
| 进度状态 | 正常/滞后/超前 |
| 任务数 | 任务数量 |
| 人员数 | 现场人员数 |
| 机械数 | 机械设备数 |
| 问题数 | 问题反馈数 |
| 天气 | 天气情况 |

### 5. UploadForm 更新

**文件**：`tauri-app/src/components/UploadForm.jsx`

**新增状态**：

```javascript
const [parsedReports, setParsedReports] = useState([]); // 解析后的日报列表
const [selectedReports, setSelectedReports] = useState([]); // 选中的日报索引
const [parsing, setParsing] = useState(false); // 解析中状态
```

**关键流程**：

```javascript
// 1. 选择文件后自动解析
const handleSelectFile = async () => {
  const file = await open({ filters: [...] });
  if (file) {
    setFilePath(file);
    await parseExcelFile(file);  // 自动触发解析
  }
};

// 2. 解析 Excel
const parseExcelFile = async (path) => {
  setParsing(true);
  const result = await excelAPI.parseExcel(path);
  setParsedReports(result.reports);
};

// 3. 勾选功能
const handleToggleReport = (index) => {
  setSelectedReports(prev =>
    prev.includes(index)
      ? prev.filter(i => i !== index)
      : [...prev, index]
  );
};

// 4. 上传按钮显示勾选数量
<button disabled={selectedReports.length === 0}>
  {selectedReports.length > 0
    ? `开始上传 (${selectedReports.length}/${parsedReports.length})`
    : "开始上传"}
</button>
```

## 界面流程

### 1. 初始状态

```
┌─────────────────────────────────────┐
│ 📤 文件上传                          │
│                      👤 徐经理 (项目经理) │
├─────────────────────────────────────┤
│ 项目: 淮安熔盐储能项目                │
├─────────────────────────────────────┤
│ [选择 Excel 文件]  [选择文件]        │
├─────────────────────────────────────┤
│ 📋 添加文件后，将自动解析并显示数据预览 │
├─────────────────────────────────────┤
│ [开始上传] (禁用)                     │
└─────────────────────────────────────┘
```

### 2. 选择文件后（自动解析中）

```
┌─────────────────────────────────────┐
│ [/Users/.../淮安日报2025.10.19.xlsx]  │
├─────────────────────────────────────┤
│ ⏳ 正在解析 Excel 文件...              │
└─────────────────────────────────────┘
```

### 3. 解析完成（显示预览）

```
┌─────────────────────────────────────────────────┐
│ 数据预览 (10 条日报)   [✓ 全选] [✗ 反选]        │
├─────────────────────────────────────────────────┤
│ ✓  日期      项目      进度  任务  人员  问题...  │
├─────────────────────────────────────────────────┤
│ ☐  10.15  淮安项目  正常    5    10    0        │
│ ☑  10.16  淮安项目  正常    6    12    1        │
│ ☑  10.17  淮安项目  滞后    4    8     2        │
│ ☐  10.18  淮安项目  正常    7    15    0        │
└─────────────────────────────────────────────────┘

✅ 解析成功！找到 10 条日报

[开始上传 (2/10)]
```

### 4. 全选后

```
┌─────────────────────────────────────────────────┐
│ 数据预览 (10 条日报)   [✓ 全选] [✗ 反选]        │
├─────────────────────────────────────────────────┤
│ ☑  10.15  淮安项目  正常    5    10    0        │
│ ☑  10.16  淮安项目  正常    6    12    1        │
│ ☑  10.17  淮安项目  滞后    4    8     2        │
│ ☑  10.18  淮安项目  正常    7    15    0        │
│ ...（全部勾选）                                  │
└─────────────────────────────────────────────────┘

[开始上传 (10/10)]
```

## 与 Python 应用的对比

| 功能               | Python      | Tauri     | 状态    |
| ------------------ | ----------- | --------- | ------- |
| 选择文件后自动解析 | ✅          | ✅        | ✅ 实现 |
| 数据预览表格       | ✅          | ✅        | ✅ 实现 |
| 勾选功能           | ✅          | ✅        | ✅ 实现 |
| 全选/反选          | ✅          | ✅        | ✅ 实现 |
| 上传按钮显示数量   | ✅          | ✅        | ✅ 实现 |
| 进度状态颜色       | ✅          | ✅        | ✅ 实现 |
| 问题数高亮         | ✅          | ✅        | ✅ 实现 |
| 详细解析           | ✅ 完整解析 | ⚠️ 简化版 | 待优化  |

## 已添加的文件

1. ✅ `tauri-app/src-tauri/src/excel.rs` - 修改 Excel 解析逻辑
2. ✅ `tauri-app/src-tauri/src/main.rs` - 添加 cmd_parse_excel
3. ✅ `tauri-app/src/services/api.js` - 添加 excelAPI
4. ✅ `tauri-app/src/components/DataPreview.jsx` - 新建预览组件
5. ✅ `tauri-app/src/components/DataPreview.css` - 新建样式文件
6. ✅ `tauri-app/src/components/UploadForm.jsx` - 更新主界面

## 测试步骤

1. **启动应用**

   ```bash
   cd tauri-app
   npm run tauri dev
   ```

2. **登录**

   - 使用测试账号登录
   - 确认显示：`👤 徐经理 (项目经理)`

3. **选择文件**

   - 点击"选择文件"
   - 选择 Excel 文件（如 `assets/淮安日报2025.10.19.xlsx`）
   - 应该自动显示"⏳ 正在解析 Excel 文件..."

4. **查看预览**

   - 解析完成后显示数据预览表格
   - 每行有勾选框
   - 显示日期、项目名称等信息

5. **勾选日报**

   - 点击勾选框选择要上传的日报
   - 或点击"全选"按钮
   - 上传按钮应显示"开始上传 (3/10)"

6. **上传**
   - 点击"开始上传"
   - 确认只上传选中的日报

## 后续优化建议

1. **完善 Excel 解析**

   - 参考 Python 的 `parse_daily_report_excel.py`
   - 完整解析任务列表、人员信息、机械租赁等

2. **添加详情查看**

   - 点击行可查看日报详情（参考 Python 的 DetailDialog）

3. **加载动画**

   - 解析时显示转圈动画

4. **错误处理**

   - 更友好的错误提示
   - 解析失败时显示具体错误

5. **性能优化**
   - 大文件解析优化
   - 虚拟滚动（数据量大时）

## 相关文档

- Python 实现：`ui/upload_widget.py`
- Python 解析器：`parse_daily_report_excel.py`
- 数据预览功能说明：`docs/数据预览功能说明.md`
