# API 错误处理优化说明

## 📋 问题描述

在 Tauri 版本的上传功能测试中，发现了两个关键问题：

### 问题 1: 请求体字段名错误

**现象**：服务器返回 `"reports: 日报数据列表不能为空"`

**原因**：

- Tauri 版本使用 `"data"` 字段名
- 后端 API 期望的是 `"reports"` 字段名

**终端日志**：

```
📥 [upload_selected_reports] 服务器响应:
{"code":0,"msg":"reports: 日报数据列表不能为空"}
```

### 问题 2: 数据格式不匹配

**现象**：后端无法解析列表数据

**原因**：

- Tauri 版本直接传递 JSON 对象数组
- 后端 API 期望列表字段为 JSON 字符串格式

**正确格式**（参考 Python 版本）：

```json
{
  "projectId": 9,
  "reporterId": 10,
  "overwriteExisting": true,
  "reports": [
    {
      "reportDate": "2025.10.7",
      "reporterName": "小目标测试项目",
      "taskProgressList": "[{\"taskNo\":\"2.1\",\"taskName\":\"设备调试\"}]", // ✅ JSON字符串
      "problemFeedbacks": "[{\"description\":\"现场问题\"}]", // ✅ JSON字符串
      "tomorrowPlans": "[{\"planNo\":\"3.1\",\"taskName\":\"维修基础\"}]" // ✅ JSON字符串
    }
  ]
}
```

### 问题 3: 错误消息未正确提取

**现象**：用户看到的错误信息是 "上传失败"，而不是服务器返回的具体错误

**原因**：

- 代码中查找 `"message"` 字段
- 服务器返回的是 `"msg"` 字段

## 🔧 解决方案

### 修复 1: upload.rs - 数据格式转换

```rust
/// ✅ 新增：上传勾选的日报（与Python版本一致）
pub async fn upload_selected_reports(
    &self,
    reports: Vec<serde_json::Value>,
    project_id: i32,
    reporter_id: i32,
    overwrite_existing: bool,
) -> Result<serde_json::Value, String> {
    // 1. 转换数据格式：将列表字段转换为JSON字符串（与Python版本一致）
    let converted_reports: Vec<serde_json::Value> = reports
        .iter()
        .map(|report| {
            let mut converted = report.clone();

            // 需要转换为JSON字符串的字段
            let array_fields = vec![
                "taskProgressList",
                "tomorrowPlans",
                "workerReports",
                "machineryRentals",
                "problemFeedbacks",
                "requirements"
            ];

            for field in array_fields {
                if let Some(value) = converted.get(field) {
                    // 如果是数组，转换为JSON字符串
                    if value.is_array() {
                        let json_string = serde_json::to_string(value)
                            .unwrap_or_else(|_| "[]".to_string());
                        converted[field] = json!(json_string);
                    }
                }
            }

            converted
        })
        .collect();

    // 2. 构建API请求数据（与Python版本一致）
    let api_data = json!({
        "projectId": project_id,
        "reporterId": reporter_id,
        "overwriteExisting": overwrite_existing,
        "reports": converted_reports  // ✅ 使用 reports 字段名
    });

    // ... 发送请求 ...
}
```

### 修复 2: 错误消息提取优化

#### upload.rs

```rust
// 6. 检查业务状态码
let code = response_json.get("code").and_then(|v| v.as_i64()).unwrap_or(0);
if code != 1 {
    // ✅ 优先使用 msg 字段，兼容 message 字段
    let message = response_json.get("msg")
        .and_then(|v| v.as_str())
        .or_else(|| response_json.get("message").and_then(|v| v.as_str()))
        .unwrap_or("上传失败");
    println!("❌ [upload_selected_reports] 业务错误: {}", message);
    return Err(message.to_string());
}
```

#### auth.rs

```rust
let status = response.status();
let result: serde_json::Value = response
    .json()
    .await
    .map_err(|e| format!("解析响应失败: {}", e))?;

// ✅ 检查HTTP状态码和业务状态码
if !status.is_success() {
    // 尝试从响应中提取错误信息
    let error_msg = result.get("msg")
        .and_then(|v| v.as_str())
        .or_else(|| result.get("message").and_then(|v| v.as_str()))
        .unwrap_or("登录失败: 用户名或密码错误");
    return Err(error_msg.to_string());
}
```

#### project.rs

```rust
let status = response.status();
let result: serde_json::Value = response
    .json()
    .await
    .map_err(|e| format!("解析数据失败: {}", e))?;

// ✅ 检查HTTP状态码
if !status.is_success() {
    // 尝试从响应中提取错误信息
    let error_msg = result.get("msg")
        .and_then(|v| v.as_str())
        .or_else(|| result.get("message").and_then(|v| v.as_str()))
        .unwrap_or(&format!("获取项目信息失败，状态码: {}", status));
    let err_msg = error_msg.to_string();
    println!("❌ [ProjectService] {}", err_msg);
    return Err(err_msg);
}
```

## 📊 修改文件清单

| 文件                       | 修改内容                                            | 说明         |
| -------------------------- | --------------------------------------------------- | ------------ |
| `src-tauri/src/upload.rs`  | ✅ 数据格式转换<br>✅ 字段名修正<br>✅ 错误消息提取 | 核心修复     |
| `src-tauri/src/auth.rs`    | ✅ 错误消息提取                                     | 改进用户体验 |
| `src-tauri/src/project.rs` | ✅ 错误消息提取                                     | 改进用户体验 |

## 🔄 数据转换流程

### 前端 → Rust 后端 → API 服务器

```
前端数据 (JSON对象)
  ↓
{
  "taskProgressList": [
    {"taskNo": "2.1", "taskName": "设备调试"}
  ]
}
  ↓ [Rust转换]
  ↓
API格式 (JSON字符串)
  ↓
{
  "taskProgressList": "[{\"taskNo\":\"2.1\",\"taskName\":\"设备调试\"}]"
}
  ↓ [发送到API]
  ↓
后端解析并存储
```

## 🧪 测试验证

### 测试 1: 上传成功场景

```bash
# 预期结果
✅ 服务器返回 code: 1
✅ 前端显示详细的成功统计
✅ 数据成功写入数据库
```

### 测试 2: 数据验证失败

```bash
# 预期结果
❌ 服务器返回 code: 0, msg: "具体错误原因"
❌ 前端显示服务器返回的错误消息
❌ 用户能看到清晰的错误提示
```

### 测试 3: 网络错误

```bash
# 预期结果
❌ 捕获网络异常
❌ 显示 "网络请求失败: ..." 错误
❌ 用户能理解是网络问题
```

## 📝 API 响应格式

### 成功响应

```json
{
  "code": 1,
  "msg": "导入完成：成功18条，失败1条，跳过0条",
  "data": {
    "totalCount": 19,
    "successCount": 18,
    "failedCount": 1,
    "skippedCount": 0,
    "successReports": [...],
    "failedReports": [...]
  }
}
```

### 错误响应

```json
{
  "code": 0,
  "msg": "reports: 日报数据列表不能为空"
}
```

## 💡 关键要点

1. **字段名一致性**

   - ✅ 使用 `"reports"` 而不是 `"data"`
   - ✅ 与 Python 版本保持一致

2. **数据格式转换**

   - ✅ 列表字段必须转换为 JSON 字符串
   - ✅ 空数组转换为 `"[]"`

3. **错误消息提取**

   - ✅ 优先检查 `"msg"` 字段
   - ✅ 兼容 `"message"` 字段
   - ✅ 提供默认错误消息

4. **用户体验**
   - ✅ 显示服务器返回的具体错误
   - ✅ 而不是通用的错误提示

## 🎯 预期效果

| 场景         | 修复前                             | 修复后                             |
| ------------ | ---------------------------------- | ---------------------------------- |
| **字段错误** | ❌ "reports: 日报数据列表不能为空" | ✅ 正确传递数据                    |
| **格式错误** | ❌ 后端无法解析                    | ✅ 正确的 JSON 字符串格式          |
| **错误提示** | ❌ "上传失败"                      | ✅ "reports: 日报数据列表不能为空" |
| **登录失败** | ❌ "登录失败: 用户名或密码错误"    | ✅ 服务器返回的具体错误            |
| **项目错误** | ❌ "获取项目信息失败，状态码: 401" | ✅ 服务器返回的具体错误            |

## 📅 修改日期

2025-10-26

## 👨‍💻 修改人

AI Assistant

## 📚 相关文档

- [Tauri 版本上传流程优化说明.md](./Tauri版本上传流程优化说明.md)
- [项目日报批量导入 API.md](../api/19-项目日报批量导入API.md)
- [convert_to_api_format.py](../convert_to_api_format.py)
