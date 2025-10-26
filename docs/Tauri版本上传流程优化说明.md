# Tauri 版本上传流程优化说明

## 📋 概述

本次优化将 Tauri 版本的日报上传流程调整为与 Python 版本完全一致，实现了以下核心功能：

1. ✅ 覆盖旧记录选项始终可见
2. ✅ 只上传勾选的日报
3. ✅ 上传成功后清空所有数据和状态
4. ✅ 用户可以持续上传，无需重启应用

## 🔧 修改内容

### 1. 前端修改 (UploadForm.jsx)

#### 1.1 新增状态管理

```javascript
const [overwriteExisting, setOverwriteExisting] = useState(false); // 是否覆盖已存在的记录
```

#### 1.2 修改上传逻辑

- **只上传勾选的日报**：从 `parsedReports` 中筛选出用户勾选的日报
- **传递覆盖选项**：将 `overwriteExisting` 参数传递给后端
- **上传成功后清空数据**：清空 `filePath`、`parsedReports`、`selectedReports`、`uploadProgress`

```javascript
const handleUpload = async () => {
  // ✅ 检查是否有勾选的日报
  if (selectedReports.length === 0) {
    setMessage("❌ 请勾选要上传的日报");
    return;
  }

  // ... 省略验证代码 ...

  try {
    // ✅ 只上传勾选的日报
    const selectedReportData = selectedReports.map(
      (index) => parsedReports[index]
    );

    const result = await uploadAPI.uploadReports(
      selectedReportData,
      projectInfo.id,
      userInfo.id,
      overwriteExisting, // ✅ 传入覆盖选项
      token
    );

    // ✅ 显示上传结果
    const successCount = result.successCount || 0;
    const failedCount = result.failedCount || 0;
    const totalCount = result.totalCount || selectedReports.length;

    setMessage(
      `✅ 上传完成！总计: ${totalCount} 条, 成功: ${successCount} 条, 失败: ${failedCount} 条`
    );
    setUploadProgress(100);

    // ✅ 上传成功后清空所有数据（与Python版本一致）
    setFilePath("");
    setParsedReports([]);
    setSelectedReports([]);
    setUploadProgress(0);
  } catch (err) {
    setMessage(`❌ 上传失败: ${err.message || err}`);
    console.error("上传错误:", err);
  } finally {
    setLoading(false);
  }
};
```

#### 1.3 UI 界面优化

在上传按钮前添加"覆盖已存在的记录"复选框：

```jsx
<div
  style={{
    display: "flex",
    alignItems: "center",
    justifyContent: "flex-end",
    marginBottom: "10px",
    gap: "15px",
  }}
>
  <label
    style={{
      display: "flex",
      alignItems: "center",
      cursor: "pointer",
      fontSize: "14px",
      color: "#666",
    }}
  >
    <input
      type="checkbox"
      checked={overwriteExisting}
      onChange={(e) => setOverwriteExisting(e.target.checked)}
      style={{
        marginRight: "8px",
        width: "18px",
        height: "18px",
        cursor: "pointer",
      }}
    />
    <span>覆盖已存在的记录</span>
  </label>

  <button
    onClick={handleUpload}
    disabled={loading || selectedReports.length === 0}
    className="btn-upload"
  >
    {/* ... 按钮文本 ... */}
  </button>
</div>
```

### 2. API 层修改 (api.js)

新增 `uploadReports` 方法：

```javascript
export const uploadAPI = {
  uploadFile: (filePath, projectId, reporterId, token) =>
    safeInvoke("cmd_upload_file", { filePath, projectId, reporterId, token }),

  // ✅ 新增：上传勾选的日报（与Python版本一致）
  uploadReports: (reports, projectId, reporterId, overwriteExisting, token) =>
    safeInvoke("cmd_upload_reports", {
      reports,
      projectId,
      reporterId,
      overwriteExisting,
      token,
    }),
};
```

### 3. 后端 Rust 修改

#### 3.1 main.rs - 新增命令

```rust
// ✅ 新增：上传勾选的日报（与Python版本一致）
#[tauri::command]
async fn cmd_upload_reports(
    reports: Vec<serde_json::Value>,
    project_id: i32,
    reporter_id: i32,
    overwrite_existing: bool,
    token: String,
    state: tauri::State<'_, AppState>,
) -> Result<serde_json::Value, String> {
    println!("📤 [cmd_upload_reports] Tauri命令被调用");
    println!("  - 日报数量: {}", reports.len());
    println!("  - 项目ID: {}", project_id);
    println!("  - 填报人ID: {}", reporter_id);
    println!("  - 覆盖已存在记录: {}", overwrite_existing);

    if token.is_empty() {
        println!("❌ [cmd_upload_reports] Token为空");
        return Err("未登录".to_string());
    }

    println!("✅ [cmd_upload_reports] 收到Token，长度: {} 字符", token.len());

    let service = UploadService::new(state.api_base_url.clone(), token);
    service.upload_selected_reports(reports, project_id, reporter_id, overwrite_existing).await
}
```

注册命令：

```rust
.invoke_handler(tauri::generate_handler![
    greet,
    cmd_login,
    cmd_refresh_token,
    cmd_get_project,
    cmd_upload_file,
    cmd_upload_reports,  // ✅ 新增：上传勾选的日报
    cmd_parse_excel,
])
```

#### 3.2 upload.rs - 新增上传方法

```rust
/// ✅ 新增：上传勾选的日报（与Python版本一致）
pub async fn upload_selected_reports(
    &self,
    reports: Vec<serde_json::Value>,
    project_id: i32,
    reporter_id: i32,
    overwrite_existing: bool,
) -> Result<serde_json::Value, String> {
    println!("📤 [upload_selected_reports] 开始上传");
    println!("  - 日报数量: {}", reports.len());
    println!("  - 覆盖已存在记录: {}", overwrite_existing);

    // 1. 构建API请求数据（与Python版本一致）
    let api_data = json!({
        "data": reports,
        "projectId": project_id,
        "reporterId": reporter_id,
        "overwriteExisting": overwrite_existing
    });

    // 2. 调用上传 API
    let client = reqwest::Client::new();
    let url = format!("{}/api/v1/daily-reports/batch-import", self.api_base_url);

    let response = client
        .post(&url)
        .header("token", &self.token)
        .header("Content-Type", "application/json")
        .json(&api_data)
        .send()
        .await
        .map_err(|e| format!("上传失败: {}", e))?;

    // 3. 解析响应并返回结果
    // ... 省略详细代码 ...
}
```

## 📊 与 Python 版本对比

| 功能点             | Python 版本 | Tauri 版本  | 状态    |
| ------------------ | ----------- | ----------- | ------- |
| 覆盖旧记录选项     | ✅ 始终显示 | ✅ 始终显示 | ✅ 一致 |
| 只上传勾选日报     | ✅ 支持     | ✅ 支持     | ✅ 一致 |
| 上传成功后清空数据 | ✅ 清空所有 | ✅ 清空所有 | ✅ 一致 |
| 继续上传流程       | ✅ 可继续   | ✅ 可继续   | ✅ 一致 |
| 上传结果展示       | ✅ 详细统计 | ✅ 详细统计 | ✅ 一致 |
| 按钮状态控制       | ✅ 智能控制 | ✅ 智能控制 | ✅ 一致 |

## 🔄 上传流程

### 完整上传流程

1. **选择文件**

   - 用户点击"选择文件"按钮
   - 选择 Excel 文件
   - 自动解析并预览

2. **勾选日报**

   - 用户在预览表格中勾选要上传的日报
   - 可使用"全选"/"反选"按钮
   - 上传按钮显示勾选数量：`开始上传 (3/10)`

3. **设置覆盖选项**

   - 勾选"覆盖已存在的记录"（可选）
   - 默认不勾选（不覆盖）

4. **开始上传**

   - 点击"开始上传"按钮
   - 显示上传进度
   - 显示上传结果：总计、成功、失败数量

5. **清空数据**

   - 上传成功后自动清空文件路径
   - 清空解析的日报数据
   - 清空勾选状态
   - 重置进度条

6. **继续上传**
   - 点击"选择文件"按钮
   - 重复步骤 1-5

## 🧪 测试步骤

### 测试 1：基本上传流程

1. 启动应用并登录
2. 选择包含多条日报的 Excel 文件
3. 勾选部分日报（例如：3 条）
4. 不勾选"覆盖已存在的记录"
5. 点击"开始上传"
6. 验证：上传成功，显示正确的统计信息
7. 验证：数据已清空，可以继续选择文件

### 测试 2：覆盖选项

1. 上传一批日报（不覆盖）
2. 再次选择相同日期的日报
3. 勾选"覆盖已存在的记录"
4. 点击"开始上传"
5. 验证：旧记录被覆盖

### 测试 3：连续上传

1. 上传第一批日报
2. 等待上传完成
3. 立即选择新文件
4. 上传第二批日报
5. 验证：两次上传都成功，数据正确清空

### 测试 4：部分勾选

1. 解析包含 10 条日报的文件
2. 只勾选 3 条
3. 上传
4. 验证：只上传了 3 条日报

## 📝 注意事项

1. **数据清空时机**：只在上传成功后清空数据，上传失败时保留数据
2. **按钮禁用**：没有勾选日报时，上传按钮自动禁用
3. **覆盖选项**：默认不勾选，避免误操作
4. **日志输出**：保留详细的控制台日志，便于调试

## 🎯 优势

1. **与 Python 版本一致**：用户体验完全相同
2. **流程更清晰**：每次上传后自动清空，避免混淆
3. **操作更灵活**：可以选择性上传部分日报
4. **数据更安全**：覆盖选项需要用户主动勾选

## 📅 修改日期

2025-10-26

## 👨‍💻 修改人

AI Assistant
