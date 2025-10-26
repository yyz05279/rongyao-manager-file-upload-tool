#![cfg_attr(all(not(debug_assertions), target_os = "windows"), windows_subsystem = "windows")]

mod auth;
mod project;
mod upload;
mod excel;

use auth::{AuthService, AuthResponse};
use project::ProjectService;
use upload::UploadService;
use std::sync::{Arc, Mutex};

type AuthServiceMutex = Arc<Mutex<Option<AuthService>>>;
type TokenMutex = Arc<Mutex<Option<String>>>;
type RefreshTokenMutex = Arc<Mutex<Option<String>>>;

struct AppState {
    auth_service: AuthServiceMutex,
    token: TokenMutex,
    refresh_token: RefreshTokenMutex,
    api_base_url: String,
}

#[tauri::command]
async fn cmd_login(
    username: String,
    password: String,
    api_url: String,
    state: tauri::State<'_, AppState>,
) -> Result<AuthResponse, String> {
    println!("🔐 [cmd_login] 开始登录流程");
    println!("  - 用户名: {}", username);
    println!("  - API URL: {}", api_url);
    
    let mut auth = AuthService::new(api_url.clone());
    let result = auth.login(&username, &password).await?;
    
    println!("✅ [cmd_login] 登录成功，准备保存Token到全局状态");
    println!("  - Token: {}...", &result.token[..20.min(result.token.len())]);
    println!("  - RefreshToken: {}...", &result.refresh_token[..20.min(result.refresh_token.len())]);
    
    // ✅ 保存 token 和 refresh_token 到全局状态
    *state.token.lock().unwrap() = Some(result.token.clone());
    *state.refresh_token.lock().unwrap() = Some(result.refresh_token.clone());
    *state.auth_service.lock().unwrap() = Some(auth);
    
    // ✅ 验证Token是否真的保存了
    let saved_token = state.token.lock().unwrap();
    if saved_token.is_some() {
        println!("✅ [cmd_login] Token已成功保存到全局状态");
        println!("  - 验证Token前缀: {}...", &saved_token.as_ref().unwrap()[..20.min(saved_token.as_ref().unwrap().len())]);
    } else {
        println!("❌ [cmd_login] Token保存失败！");
    }
    drop(saved_token); // 释放锁
    
    Ok(result)
}

#[tauri::command]
async fn cmd_get_project(
    token: String,
    state: tauri::State<'_, AppState>,
) -> Result<project::ProjectInfo, String> {
    println!("🔍 [cmd_get_project] Tauri命令被调用");
    
    // ✅ 验证token不为空
    if token.is_empty() {
        println!("❌ [cmd_get_project] Token为空");
        return Err("未登录".to_string());
    }
    
    println!("✅ [cmd_get_project] 收到Token");
    println!("  - Token长度: {} 字符", token.len());
    println!("  - Token前20字符: {}...", &token[..20.min(token.len())]);

    let service = ProjectService::new(state.api_base_url.clone(), token);
    let result = service.get_my_project().await;

    match &result {
        Ok(info) => println!("✅ [cmd_get_project] 项目信息获取成功: {:?}", info),
        Err(e) => println!("❌ [cmd_get_project] 项目信息获取失败: {}", e),
    }

    result
}

#[tauri::command]
async fn cmd_upload_file(
    file_path: String,
    project_id: i32,
    reporter_id: i32,
    token: String,
    state: tauri::State<'_, AppState>,
) -> Result<String, String> {
    println!("📤 [cmd_upload_file] Tauri命令被调用");
    
    if token.is_empty() {
        println!("❌ [cmd_upload_file] Token为空");
        return Err("未登录".to_string());
    }
    
    println!("✅ [cmd_upload_file] 收到Token，长度: {} 字符", token.len());

    let service = UploadService::new(state.api_base_url.clone(), token);
    service.upload_daily_report(file_path, project_id, reporter_id).await
}

#[tauri::command]
async fn cmd_parse_excel(file_path: String) -> Result<serde_json::Value, String> {
    excel::parse_excel_file(&file_path)
        .map(|data| serde_json::json!({"reports": data}))
}

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

#[tauri::command]
async fn cmd_refresh_token(
    refresh_token: String,
    state: tauri::State<'_, AppState>,
) -> Result<String, String> {
    println!("🔄 [cmd_refresh_token] Tauri命令被调用");
    
    if refresh_token.is_empty() {
        println!("❌ [cmd_refresh_token] RefreshToken为空");
        return Err("未登录".to_string());
    }
    
    println!("✅ [cmd_refresh_token] 收到RefreshToken，长度: {} 字符", refresh_token.len());
    
    // ✅ 使用refresh_token创建AuthService实例
    let mut auth_service = AuthService::with_refresh_token(
        state.api_base_url.clone(), 
        refresh_token
    );
    
    let new_token = auth_service.refresh_token().await?;
    
    println!("✅ [cmd_refresh_token] Token刷新成功");
    
    Ok(new_token)
}

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! Welcome to Tauri.", name)
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .manage(AppState {
            auth_service: Arc::new(Mutex::new(None)),
            token: Arc::new(Mutex::new(None)),
            refresh_token: Arc::new(Mutex::new(None)),
            api_base_url: "http://42.192.76.234:8081".to_string(),
        })
        .invoke_handler(tauri::generate_handler![
            greet,
            cmd_login,
            cmd_refresh_token,
            cmd_get_project,
            cmd_upload_file,
            cmd_upload_reports,  // ✅ 新增：上传勾选的日报
            cmd_parse_excel,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
