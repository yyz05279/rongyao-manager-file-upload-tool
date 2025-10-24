use regex::Regex;
use serde::{Deserialize, Serialize};

#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct AuthResponse {
    pub token: String,
    pub refresh_token: String,
    pub user_info: UserInfo,
}

#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct UserInfo {
    pub id: i32,
    pub username: String,
    pub email: String,
    pub phone: String,
}

pub struct AuthService {
    api_base_url: String,
    token: Option<String>,
    refresh_token: Option<String>,
}

impl AuthService {
    pub fn new(api_base_url: String) -> Self {
        Self {
            api_base_url,
            token: None,
            refresh_token: None,
        }
    }

    /// 判断是否是手机号
    fn is_phone_number(value: &str) -> bool {
        // 去除空格和特殊字符
        let cleaned: String = value
            .chars()
            .filter(|c| !c.is_whitespace() && *c != '-' && *c != '(' && *c != ')')
            .collect();

        // 中国手机号：11位数字，以1开头
        let phone_regex = Regex::new(r"^1\d{10}$").unwrap();
        if phone_regex.is_match(&cleaned) {
            return true;
        }

        // 国际手机号
        let intl_regex = Regex::new(r"^\+?\d{10,15}$").unwrap();
        intl_regex.is_match(&cleaned)
    }

    /// 用户登录
    pub async fn login(&mut self, username: &str, password: &str) -> Result<AuthResponse, String> {
        let client = reqwest::Client::new();
        let login_url = format!("{}/api/v1/auth/login", self.api_base_url);

        // 构建请求数据
        let payload = if Self::is_phone_number(username) {
            serde_json::json!({
                "phone": username,
                "password": password
            })
        } else {
            serde_json::json!({
                "username": username,
                "password": password
            })
        };

        let response = client
            .post(&login_url)
            .json(&payload)
            .send()
            .await
            .map_err(|e| format!("网络请求失败: {}", e))?;

        if !response.status().is_success() {
            return Err("登录失败: 用户名或密码错误".to_string());
        }

        let result: serde_json::Value = response
            .json()
            .await
            .map_err(|e| format!("解析响应失败: {}", e))?;

        // 提取 token 和用户信息
        let token = result["data"]["token"]
            .as_str()
            .ok_or("token 不存在")?
            .to_string();

        let refresh_token = result["data"]["refresh_token"]
            .as_str()
            .unwrap_or("")
            .to_string();

        let user_info = UserInfo {
            id: result["data"]["user"]["id"].as_i64().unwrap_or(0) as i32,
            username: result["data"]["user"]["username"]
                .as_str()
                .unwrap_or("")
                .to_string(),
            email: result["data"]["user"]["email"]
                .as_str()
                .unwrap_or("")
                .to_string(),
            phone: result["data"]["user"]["phone"]
                .as_str()
                .unwrap_or("")
                .to_string(),
        };

        self.token = Some(token.clone());
        self.refresh_token = Some(refresh_token.clone());

        Ok(AuthResponse {
            token,
            refresh_token,
            user_info,
        })
    }

    pub fn get_token(&self) -> Option<&str> {
        self.token.as_deref()
    }
}
