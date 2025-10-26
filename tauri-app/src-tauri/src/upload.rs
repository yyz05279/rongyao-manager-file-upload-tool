use serde_json::json;

pub struct UploadService {
    api_base_url: String,
    token: String,
}

impl UploadService {
    pub fn new(api_base_url: String, token: String) -> Self {
        Self {
            api_base_url,
            token,
        }
    }

    /// 上传日报
    pub async fn upload_daily_report(
        &self,
        file_path: String,
        project_id: i32,
        reporter_id: i32,
    ) -> Result<String, String> {
        // 1. 解析 Excel
        let excel_data = crate::excel::parse_excel_file(&file_path)?;

        // 2. 转换为 API 格式
        let api_data = json!({
            "data": excel_data,
            "projectId": project_id,
            "reporterId": reporter_id
        });

        // 3. 调用上传 API
        let client = reqwest::Client::new();
        let url = format!("{}/api/v1/daily-reports/batch-import", self.api_base_url);

        // ✅ 使用 "token" 作为 header key（与Python保持一致）
        let response = client
            .post(&url)
            .header("token", &self.token)
            .json(&api_data)
            .send()
            .await
            .map_err(|e| format!("上传失败: {}", e))?;

        if !response.status().is_success() {
            return Err("服务器返回错误".to_string());
        }

        Ok("上传成功".to_string())
    }

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
                            let json_string = serde_json::to_string(value).unwrap_or_else(|_| "[]".to_string());
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

        println!("📋 [upload_selected_reports] API请求数据:");
        println!("{}", serde_json::to_string_pretty(&api_data).unwrap_or_default());

        // 3. 调用上传 API
        let client = reqwest::Client::new();
        let url = format!("{}/api/v1/daily-reports/batch-import", self.api_base_url);

        println!("🌐 [upload_selected_reports] 请求URL: {}", url);

        // ✅ 使用 "token" 作为 header key（与Python保持一致）
        let response = client
            .post(&url)
            .header("token", &self.token)
            .header("Content-Type", "application/json")
            .json(&api_data)
            .send()
            .await
            .map_err(|e| {
                println!("❌ [upload_selected_reports] 网络请求失败: {}", e);
                format!("上传失败: {}", e)
            })?;

        let status = response.status();
        println!("📊 [upload_selected_reports] HTTP状态码: {}", status);

        // 4. 解析响应
        let response_text = response.text().await.map_err(|e| {
            println!("❌ [upload_selected_reports] 读取响应失败: {}", e);
            format!("读取响应失败: {}", e)
        })?;

        println!("📥 [upload_selected_reports] 服务器响应:");
        println!("{}", response_text);

        if !status.is_success() {
            return Err(format!("服务器返回错误 ({}): {}", status, response_text));
        }

        // 5. 解析JSON响应
        let response_json: serde_json::Value = serde_json::from_str(&response_text)
            .map_err(|e| {
                println!("❌ [upload_selected_reports] JSON解析失败: {}", e);
                format!("响应解析失败: {}", e)
            })?;

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

        // 7. 返回数据（与Python版本一致）
        let data = response_json.get("data").cloned().unwrap_or(json!({}));
        println!("✅ [upload_selected_reports] 上传成功");

        Ok(data)
    }
}
