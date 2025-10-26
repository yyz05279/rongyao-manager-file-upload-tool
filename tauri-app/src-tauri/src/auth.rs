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
    pub name: String,
    pub email: String,
    pub phone: String,
    pub role: String,
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

    /// 创建带有refresh_token的实例（用于刷新token场景）
    pub fn with_refresh_token(api_base_url: String, refresh_token: String) -> Self {
        Self {
            api_base_url,
            token: None,
            refresh_token: Some(refresh_token),
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

        // ✅ 打印完整的响应数据用于调试
        println!("📦 [AuthService] 登录响应数据: {}", serde_json::to_string_pretty(&result).unwrap_or_default());

        // 提取 token 和用户信息
        let token = result["data"]["token"]
            .as_str()
            .ok_or("token 不存在")?
            .to_string();

        let refresh_token = result["data"]["refresh_token"]
            .as_str()
            .unwrap_or("")
            .to_string();
        
        println!("✅ [AuthService] Token提取成功");
        println!("  - Token长度: {} 字符", token.len());
        println!("  - Token内容: {}", token);
        println!("  - RefreshToken长度: {} 字符", refresh_token.len());

        let user_info = UserInfo {
            id: result["data"]["user"]["id"].as_i64().unwrap_or(0) as i32,
            username: result["data"]["user"]["username"]
                .as_str()
                .unwrap_or("")
                .to_string(),
            name: result["data"]["user"]["name"]
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
            role: result["data"]["user"]["role"]
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

    /// 刷新Token
    pub async fn refresh_token(&mut self) -> Result<String, String> {
        println!("🔄 [AuthService] 开始刷新Token");
        
        let refresh_token = self.refresh_token
            .as_ref()
            .ok_or("RefreshToken不存在")?;

        let client = reqwest::Client::new();
        let refresh_url = format!("{}/api/v1/auth/refresh", self.api_base_url);

        let payload = serde_json::json!({
            "refreshToken": refresh_token
        });

        println!("🔄 [AuthService] 发送刷新请求到: {}", refresh_url);

        let response = client
            .post(&refresh_url)
            .json(&payload)
            .send()
            .await
            .map_err(|e| {
                let err_msg = format!("刷新Token请求失败: {}", e);
                println!("❌ [AuthService] {}", err_msg);
                err_msg
            })?;

        println!("📡 [AuthService] 刷新响应状态: {}", response.status());

        if !response.status().is_success() {
            let err_msg = "刷新Token失败: Token已过期".to_string();
            println!("❌ [AuthService] {}", err_msg);
            return Err(err_msg);
        }

        let result: serde_json::Value = response
            .json()
            .await
            .map_err(|e| {
                let err_msg = format!("解析刷新响应失败: {}", e);
                println!("❌ [AuthService] {}", err_msg);
                err_msg
            })?;

        println!("📦 [AuthService] 刷新响应数据: {}", serde_json::to_string_pretty(&result).unwrap_or_default());

        let new_token = result["data"]["token"]
            .as_str()
            .ok_or("刷新后的token不存在")?
            .to_string();

        self.token = Some(new_token.clone());

        println!("✅ [AuthService] Token刷新成功");

        Ok(new_token)
    }
}
