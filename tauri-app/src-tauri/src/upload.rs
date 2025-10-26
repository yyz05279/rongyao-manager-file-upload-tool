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
}
