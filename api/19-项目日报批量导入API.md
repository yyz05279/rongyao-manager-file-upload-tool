# 项目日报批量导入 API 文档

## 概述

本文档说明项目日报的批量导入功能，支持从 Excel 解析后的数据批量导入到数据库。

## 完整流程

### 方式一：Excel 上传（仅保存文件）

**适用场景**: 需要保留原始 Excel 文件

```
用户 -> 上传Excel -> 服务器保存文件 -> 返回文件路径
```

### 方式二：Excel 解析 + 批量导入（推荐）

**适用场景**: 需要将 Excel 数据导入数据库

```
1. 用户上传Excel
2. 使用Python工具解析Excel
3. 转换为API格式
4. 调用批量导入API
5. 数据保存到数据库
```

## 接口信息

### 1. 上传 Excel 文件

#### 接口说明

上传 Excel 文件到服务器，仅保存文件，不解析数据。

#### 请求信息

- **路径**: `/api/v1/daily-reports/upload-excel`
- **方法**: `POST`
- **Content-Type**: `multipart/form-data`

#### 请求参数

| 参数名      | 类型   | 必填 | 说明           |
| ----------- | ------ | ---- | -------------- |
| file        | File   | 是   | Excel 文件     |
| projectId   | Long   | 是   | 项目 ID        |
| managerName | String | 是   | 项目经理名称   |
| phone       | String | 是   | 项目经理手机号 |

#### 响应示例

```json
{
  "code": 200,
  "message": "文件上传成功",
  "data": "/upload/2025/10/22/淮安项目_日报_2025-10-22-14:30:15_张三_13800138000.xlsx"
}
```

---

### 2. 批量导入日报数据

#### 接口说明

批量导入从 Excel 解析后的日报数据，一次可导入多条日报记录。

#### 请求信息

- **路径**: `/api/v1/daily-reports/batch-import`
- **方法**: `POST`
- **Content-Type**: `application/json`
- **认证**: 需要 JWT Token

#### 请求参数

**请求体结构**:

```json
{
  "projectId": 1,
  "reporterId": 1,
  "reports": [
    {
      "reportDate": "2025.10.19",
      "projectName": "淮安项目",
      "overallProgress": "normal",
      "progressDescription": "二期管道安装阶段",
      "taskProgressList": "[{\"taskNo\":\"2.1\",\"taskName\":\"管道安装\"}]",
      "tomorrowPlans": "[{\"planNo\":\"3.1\",\"taskName\":\"电伴热电源接线\"}]",
      "workerReports": "[{\"name\":\"张亚伟\",\"jobType\":\"电工\"}]",
      "machineryRentals": "[]",
      "problemFeedbacks": "[{\"description\":\"问题描述\"}]",
      "requirements": "[]",
      "weather": "晴",
      "temperature": "25℃",
      "onSitePersonnelCount": 3,
      "remarks": null
    }
  ]
}
```

**字段说明**:

| 字段名     | 类型  | 必填 | 说明         |
| ---------- | ----- | ---- | ------------ |
| projectId  | Long  | 是   | 项目 ID      |
| reporterId | Long  | 是   | 填报人 ID    |
| reports    | Array | 是   | 日报数据数组 |

**reports 数组元素**:

| 字段名               | 类型    | 必填 | 说明                             |
| -------------------- | ------- | ---- | -------------------------------- |
| reportDate           | String  | 是   | 日报日期（支持多种格式）         |
| projectName          | String  | 否   | 项目名称                         |
| overallProgress      | String  | 否   | 整体进度（normal/delayed/ahead） |
| progressDescription  | String  | 否   | 进度描述                         |
| taskProgressList     | String  | 否   | 任务进度列表（JSON 字符串）      |
| tomorrowPlans        | String  | 否   | 明日计划列表（JSON 字符串）      |
| workerReports        | String  | 否   | 工作人员报告（JSON 字符串）      |
| machineryRentals     | String  | 否   | 机械租赁列表（JSON 字符串）      |
| problemFeedbacks     | String  | 否   | 问题反馈列表（JSON 字符串）      |
| requirements         | String  | 否   | 需求列表（JSON 字符串）          |
| weather              | String  | 否   | 天气情况                         |
| temperature          | String  | 否   | 温度                             |
| onSitePersonnelCount | Integer | 否   | 现场总人数                       |
| remarks              | String  | 否   | 备注                             |

#### 请求示例

```bash
curl -X POST "http://42.192.76.234:8081
/api/v1/daily-reports/batch-import" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d @api_import.json
```

#### 响应示例

**成功响应**（200 OK）:

```json
{
  "code": 200,
  "message": "导入完成：成功18条，失败1条，跳过0条",
  "data": {
    "totalCount": 19,
    "successCount": 18,
    "failedCount": 1,
    "skippedCount": 0,
    "startTime": "2025-10-22T14:30:00",
    "endTime": "2025-10-22T14:30:05",
    "durationMs": 5000,
    "successReports": [
      {
        "id": 1,
        "reportDate": "2025.10.1",
        "projectName": "淮安项目"
      }
    ],
    "failedReports": [
      {
        "reportDate": "2025.10.10",
        "reason": "该项目在此日期已存在日报"
      }
    ]
  }
}
```

## 完整使用流程

### 步骤 1: 解析 Excel 文件

使用 Python 工具解析 Excel 文件：

```bash
python3 scripts/parse_daily_report_excel.py docs/assets/淮安日报2025.10.19.xlsx parsed.json
```

**输出**: `parsed.json` - 包含解析后的数据

### 步骤 2: 转换为 API 格式

使用转换工具将解析结果转换为 API 格式：

```bash
python3 scripts/convert_to_api_format.py parsed.json 1 1 api_import.json
```

**参数说明**:

- `parsed.json`: 步骤 1 的输出文件
- `1`: 项目 ID
- `1`: 填报人 ID
- `api_import.json`: 输出文件

**输出**: `api_import.json` - API 格式的数据

### 步骤 3: 调用批量导入 API

```bash
curl -X POST "http://42.192.76.234:8081
/api/v1/daily-reports/batch-import" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d @api_import.json
```

### 步骤 4: 查看导入结果

API 会返回详细的导入结果，包括：

- 总数量
- 成功数量
- 失败数量
- 跳过数量（已存在的记录）
- 详细的成功和失败列表

## 日期格式支持

批量导入 API 支持多种日期格式：

| 格式     | 示例       | 说明               |
| -------- | ---------- | ------------------ |
| yyyy.M.d | 2025.10.19 | Excel 工作表名格式 |
| yyyy-M-d | 2025-10-19 | 标准日期格式       |
| yyyy/M/d | 2025/10/19 | 斜杠分隔格式       |

## 导入规则

### 1. 重复检查

- 系统会检查同一项目、同一日期是否已存在日报
- 如果已存在，该条记录会被跳过，计入 `skippedCount`

### 2. 事务处理

- 使用数据库事务确保数据一致性
- 单条记录失败不影响其他记录的导入
- 每条记录独立处理

### 3. 状态设置

- 所有导入的日报状态默认为 `submitted`（已提交）
- 自动设置提交时间为导入时间

### 4. JSON 字段

- 所有列表类型字段（如 taskProgressList）必须是 JSON 字符串格式
- 空数组使用 `"[]"` 或 `null`

## 错误处理

### 常见错误

| 错误信息                 | 原因                | 解决方案               |
| ------------------------ | ------------------- | ---------------------- |
| 项目不存在               | projectId 无效      | 检查项目 ID 是否正确   |
| 填报人不存在             | reporterId 无效     | 检查填报人 ID 是否正确 |
| 日期格式错误             | reportDate 格式错误 | 使用支持的日期格式     |
| 该项目在此日期已存在日报 | 重复导入            | 查看 skippedCount      |
| JSON 解析失败            | JSON 字符串格式错误 | 检查 JSON 格式         |

## 性能说明

### 导入速度

- 单条记录约 50-100ms
- 19 条记录约 5 秒
- 建议单次导入不超过 100 条

### 优化建议

1. **分批导入**: 大量数据分批次导入
2. **异步处理**: 前端使用异步方式调用
3. **进度提示**: 显示导入进度给用户

## 一键导入脚本

创建一个便捷脚本 `import_excel_to_db.sh`:

```bash
#!/bin/bash

# 日报 Excel 一键导入脚本

if [ $# -lt 4 ]; then
    echo "使用方法: ./import_excel_to_db.sh <excel文件> <项目ID> <填报人ID> <token>"
    exit 1
fi

EXCEL_FILE=$1
PROJECT_ID=$2
REPORTER_ID=$3
TOKEN=$4

echo "步骤 1: 解析 Excel..."
python3 scripts/parse_daily_report_excel.py "$EXCEL_FILE" /tmp/parsed.json

echo "步骤 2: 转换为 API 格式..."
python3 scripts/convert_to_api_format.py /tmp/parsed.json "$PROJECT_ID" "$REPORTER_ID" /tmp/api_import.json

echo "步骤 3: 调用批量导入 API..."
curl -X POST "http://42.192.76.234:8081
/api/v1/daily-reports/batch-import" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @/tmp/api_import.json

echo "清理临时文件..."
rm -f /tmp/parsed.json /tmp/api_import.json

echo "导入完成！"
```

## 相关文档

- [日报 Excel 解析工具使用指南](../guides/日报Excel解析工具使用指南.md)
- [日报 Excel 上传 API](./18-项目日报Excel上传API.md)
- [项目日报管理 API](./15-项目日报管理API.md)

## 更新日志

| 日期       | 版本  | 说明                       |
| ---------- | ----- | -------------------------- |
| 2025-10-22 | 1.0.0 | 初始版本，实现批量导入功能 |

---

**文档维护**: 开发团队  
**最后更新**: 2025-10-22
