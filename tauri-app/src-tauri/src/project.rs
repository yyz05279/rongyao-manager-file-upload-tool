use serde::{Deserialize, Serialize};

#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct ProjectInfo {
    pub id: i32,
    pub name: String,
    pub type_display_name: String,
    pub status_display_name: String,
    pub manager: String,
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
        let client = reqwest::Client::new();
        let url = format!("{}/api/v1/projects/my-project", self.api_base_url);

        let response = client
            .get(&url)
            .header("Authorization", format!("Bearer {}", self.token))
            .send()
            .await
            .map_err(|e| format!("请求失败: {}", e))?;

        if !response.status().is_success() {
            return Err("获取项目信息失败".to_string());
        }

        let result: serde_json::Value = response
            .json()
            .await
            .map_err(|e| format!("解析数据失败: {}", e))?;

        let project_data = &result["data"];

        Ok(ProjectInfo {
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
        })
    }
}
