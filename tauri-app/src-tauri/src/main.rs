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
    
    let mut auth = AuthService::new(api_url.clone());
    let result = auth.login(&username, &password).await?;
    
    println!("✅ [cmd_login] 登录成功，保存Token到全局状态");
    println!("  - Token: {}...", &result.token[..20.min(result.token.len())]);
    println!("  - RefreshToken: {}...", &result.refresh_token[..20.min(result.refresh_token.len())]);
    
    // ✅ 保存 token 和 refresh_token 到全局状态
    *state.token.lock().unwrap() = Some(result.token.clone());
    *state.refresh_token.lock().unwrap() = Some(result.refresh_token.clone());
    *state.auth_service.lock().unwrap() = Some(auth);
    
    println!("✅ [cmd_login] Token已保存到全局状态");
    
    Ok(result)
}

#[tauri::command]
async fn cmd_get_project(
    state: tauri::State<'_, AppState>,
) -> Result<project::ProjectInfo, String> {
    println!("🔍 [cmd_get_project] Tauri命令被调用");
    
    let token = state
        .token
        .lock()
        .unwrap()
        .clone()
        .ok_or_else(|| {
            println!("❌ [cmd_get_project] Token为空，用户未登录");
            "未登录".to_string()
        })?;

    println!("✅ [cmd_get_project] Token已获取");

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
    state: tauri::State<'_, AppState>,
) -> Result<String, String> {
    let token = state
        .token
        .lock()
        .unwrap()
        .clone()
        .ok_or("未登录")?;

    let service = UploadService::new(state.api_base_url.clone(), token);
    service.upload_daily_report(file_path, project_id, reporter_id).await
}

#[tauri::command]
async fn cmd_parse_excel(file_path: String) -> Result<serde_json::Value, String> {
    excel::parse_excel_file(&file_path)
        .map(|data| serde_json::json!({"reports": data}))
}

#[tauri::command]
async fn cmd_refresh_token(
    state: tauri::State<'_, AppState>,
) -> Result<String, String> {
    println!("🔄 [cmd_refresh_token] Tauri命令被调用");
    
    // ✅ 先获取auth_service，在释放锁之前clone
    let mut auth_service = {
        let mut auth_service_lock = state.auth_service.lock().unwrap();
        auth_service_lock
            .take()
            .ok_or_else(|| {
                println!("❌ [cmd_refresh_token] AuthService未初始化");
                "未登录".to_string()
            })?
    }; // 锁在这里被释放

    let new_token = auth_service.refresh_token().await?;
    
    // 更新全局状态中的token和auth_service
    *state.token.lock().unwrap() = Some(new_token.clone());
    *state.auth_service.lock().unwrap() = Some(auth_service);
    
    println!("✅ [cmd_refresh_token] Token刷新成功并已更新全局状态");
    
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
            api_base_url: "http://localhost:3000".to_string(),
        })
        .invoke_handler(tauri::generate_handler![
            greet,
            cmd_login,
            cmd_refresh_token,
            cmd_get_project,
            cmd_upload_file,
            cmd_parse_excel,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
