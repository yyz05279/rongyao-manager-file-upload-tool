use serde::{Deserialize, Serialize};

#[derive(Clone, Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct ProjectInfo {
    pub id: i32,
    pub name: String,
    pub type_display_name: String,
    pub status_display_name: String,
    pub manager: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub completion_progress: Option<i32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub estimated_salt_amount: Option<i32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub actual_salt_amount: Option<i32>,
}

pub struct ProjectService {
    api_base_url: String,
    token: String,
}

impl ProjectService {
    pub fn new(api_base_url: String, token: String) -> Self {
        Self {
            api_base_url,
            token,
        }
    }

    /// 获取用户项目
    pub async fn get_my_project(&self) -> Result<ProjectInfo, String> {
        println!("🔍 [ProjectService] 开始获取项目信息");
        println!("  - URL: {}/api/v1/projects/my-project", self.api_base_url);
        println!("  - Token长度: {} 字符", self.token.len());
        println!("  - Token前20字符: {}", &self.token[..20.min(self.token.len())]);
        println!("  - Token后20字符: {}", &self.token[self.token.len().saturating_sub(20)..]);
        println!("  - 完整Token: {}", self.token);
        
        let client = reqwest::Client::new();
        let url = format!("{}/api/v1/projects/my-project", self.api_base_url);
        
        // ✅ 使用 "token" 作为 header key（与Python保持一致）
        println!("  - token Header: {}", self.token);

        let response = client
            .get(&url)
            .header("token", &self.token)
            .send()
            .await
            .map_err(|e| {
                let err_msg = format!("请求失败: {}", e);
                println!("❌ [ProjectService] {}", err_msg);
                err_msg
            })?;

        let status = response.status();
        println!("📡 [ProjectService] 响应状态: {}", status);

        let result: serde_json::Value = response
            .json()
            .await
            .map_err(|e| {
                let err_msg = format!("解析数据失败: {}", e);
                println!("❌ [ProjectService] {}", err_msg);
                err_msg
            })?;

        // ✅ 检查HTTP状态码
        if !status.is_success() {
            // 尝试从响应中提取错误信息
            let default_msg = format!("获取项目信息失败，状态码: {}", status);
            let error_msg = result.get("msg")
                .and_then(|v| v.as_str())
                .or_else(|| result.get("message").and_then(|v| v.as_str()))
                .unwrap_or(&default_msg);
            let err_msg = error_msg.to_string();
            println!("❌ [ProjectService] {}", err_msg);
            return Err(err_msg);
        }

        println!("📦 [ProjectService] API响应数据: {}", serde_json::to_string_pretty(&result).unwrap_or_default());

        let project_data = &result["data"];

        let project_info = ProjectInfo {
            id: project_data["id"].as_i64().unwrap_or(0) as i32,
            name: project_data["name"]
                .as_str()
                .unwrap_or("")
                .to_string(),
            type_display_name: project_data["typeDisplayName"]
                .as_str()
                .unwrap_or("")
                .to_string(),
            status_display_name: project_data["statusDisplayName"]
                .as_str()
                .unwrap_or("")
                .to_string(),
            manager: project_data["manager"]
                .as_str()
                .unwrap_or("")
                .to_string(),
            completion_progress: project_data["completionProgress"].as_i64().map(|v| v as i32),
            estimated_salt_amount: project_data["estimatedSaltAmount"].as_i64().map(|v| v as i32),
            actual_salt_amount: project_data["actualSaltAmount"].as_i64().map(|v| v as i32),
        };

        println!("✅ [ProjectService] 项目信息解析成功: {:?}", project_info);

        Ok(project_info)
    }
}
