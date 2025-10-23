# API 字段映射修改说明

## 修改日期

2025 年 10 月 23 日

## 修改内容

### 字段映射更正

| 层级       | 原字段（错误）❌ | 新字段（正确）✅      | 说明             |
| ---------- | ---------------- | --------------------- | ---------------- |
| API 请求体 | `projectName`    | `reporterName`        | 填报人名称       |
| API 请求体 | -                | `progressDescription` | 项目整体进度描述 |

## 修改的文件

### 1. `convert_to_api_format.py`

**修改位置**：`convert_to_api_format()` 函数，API 请求体构建部分

**修改前**：

```python
api_report = {
    "reportDate": report.get("reportDate", ""),
    "projectName": report.get("projectName", ""),  # ❌ 错误
    "overallProgress": report.get("overallProgress", "normal"),
    "progressDescription": report.get("progressDescription", ""),
    ...
}
```

**修改后**：

```python
api_report = {
    "reportDate": report.get("reportDate", ""),
    "reporterName": report.get("reporterName", ""),  # ✅ 正确
    "overallProgress": report.get("overallProgress", "normal"),
    "progressDescription": report.get("progressDescription", ""),  # ✅ 保留
    ...
}
```

### 2. `parse_daily_report_excel.py`

**修改位置**：`parse_sheet()` 方法，解析结果初始化部分

**修改前**：

```python
report_data = {
    "reportDate": sheet_name if sheet_name else ws.title,
    "projectName": self._get_cell_value(ws, 1, 1).replace("项目工作日报", "").strip(),  # ❌ 错误
    "overallProgress": None,
    "progressDescription": None,
    ...
}
```

**修改后**：

```python
report_data = {
    "reportDate": sheet_name if sheet_name else ws.title,
    "reporterName": self._get_cell_value(ws, 1, 1).replace("项目工作日报", "").strip(),  # ✅ 正确
    "overallProgress": None,
    "progressDescription": None,
    ...
}
```

### 3. `ui/upload_widget.py`

**修改位置**：数据预览表格填充部分

**修改前**：

```python
# 项目名称
project_item = QTableWidgetItem(report.get('projectName', '-'))  # ❌ 错误
self.data_table.setItem(row, 1, project_item)
```

**修改后**：

```python
# 填报人名称（原项目名称）
reporter_item = QTableWidgetItem(report.get('reporterName', '-'))  # ✅ 正确
self.data_table.setItem(row, 1, reporter_item)
```

### 4. `ui/daily_report_detail_dialog.py`

**修改位置**：基本信息面板显示部分

**修改前**：

```python
# 项目信息（优先从全局状态获取）
project_name = self.report_data.get('projectName', '-')  # ❌ 错误
if self.project_info:
    project_name = self.project_info.get('name', project_name)
row1.addWidget(self._create_info_label("📁 项目:", project_name))
```

**修改后**：

```python
# 项目信息（优先从全局状态获取）
reporter_name = self.report_data.get('reporterName', '-')  # ✅ 正确
if self.project_info:
    project_name = self.project_info.get('name', reporter_name)
else:
    project_name = reporter_name
row1.addWidget(self._create_info_label("📁 项目:", project_name))
```

## 数据流向示例

### 修改前（错误）❌

```
Excel 第一行内容: "淮安项目工作日报"
                    ↓
parse_daily_report_excel.py 解析
                    ↓
report['projectName'] = "淮安项目"
                    ↓
convert_to_api_format.py 转换
                    ↓
API请求体: { "projectName": "淮安项目" }  ❌ 错误字段名
                    ↓
服务器接收失败或错误处理
```

### 修改后（正确）✅

```
Excel 第一行内容: "淮安项目工作日报"
                    ↓
parse_daily_report_excel.py 解析
                    ↓
report['reporterName'] = "淮安项目"
                    ↓
convert_to_api_format.py 转换
                    ↓
API请求体: { "reporterName": "淮安项目" }  ✅ 正确字段名
                    ↓
服务器成功接收处理
```

## 字段含义

### `reporterName`

- **中文含义**：填报人名称 / 报告方名称
- **来源**：从 Excel 第一行提取，格式为 "项目名工作日报"
- **处理**：去除 "项目工作日报" 文本后保留的项目/填报人名称
- **示例**：
  - Excel 中：`淮安项目工作日报` → `淮安项目`
  - Excel 中：`2025.10.19项目日报` → `2025.10.19项目`

### `progressDescription`

- **中文含义**：项目整体进度描述
- **来源**：从 Excel 第 3 行第 5 列提取
- **内容**：文本描述，如 "正常进行"、"有所延误"等
- **用途**：详细的进度说明信息

## 测试验证

### 验证 Excel 解析结果

```bash
# 运行解析脚本
python parse_daily_report_excel.py test_report.xlsx

# 检查输出是否包含 reporterName（而不是 projectName）
```

### 验证 API 请求格式

```bash
# 运行转换脚本
python convert_to_api_format.py parsed.json 1 1

# 检查输出的 JSON 中是否包含 reporterName 和 progressDescription
# 确保不再包含 projectName
```

### 验证 UI 显示

1. 在上传界面数据预览表格中

   - 第 2 列应显示 "填报人名称" 的值
   - 值应该是从 Excel 第一行提取的项目/填报人名称

2. 在日报详情对话框中
   - 基本信息区域应正确显示项目名称
   - 如果全局状态中有项目信息，显示项目名称，否则显示填报人名称

## 注意事项

### ⚠️ 重要

- ✅ 字段 `reporterName` 在整个数据处理链中一致使用
- ✅ `progressDescription` 字段在所有地方保留和使用
- ✅ UI 层的显示逻辑不变（仍显示为 "项目"）
- ✅ API 请求体中使用的是驼峰命名法（`reporterName`）

### 后向兼容性

- 如果有历史数据使用 `projectName` 字段，需要进行迁移
- 建议在 API 层进行字段映射处理

## 修改清单

- [x] `convert_to_api_format.py`：修改 API 请求体字段
- [x] `parse_daily_report_excel.py`：修改 Excel 解析结果字段
- [x] `ui/upload_widget.py`：更新数据预览表格字段引用
- [x] `ui/daily_report_detail_dialog.py`：更新日报详情显示字段引用
- [x] 所有文件 lint 检查通过 ✅

## 相关文档

- 数据预览功能说明.md - UI 层数据显示
- API 字段映射文档 - API 层字段定义
