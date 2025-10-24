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

struct AppState {
    auth_service: AuthServiceMutex,
    token: TokenMutex,
    api_base_url: String,
}

#[tauri::command]
async fn cmd_login(
    username: String,
    password: String,
    api_url: String,
    state: tauri::State<'_, AppState>,
) -> Result<AuthResponse, String> {
    let mut auth = AuthService::new(api_url.clone());
    let result = auth.login(&username, &password).await?;
    
    // 保存 token
    *state.token.lock().unwrap() = Some(result.token.clone());
    *state.auth_service.lock().unwrap() = Some(auth);
    
    Ok(result)
}

#[tauri::command]
async fn cmd_get_project(
    state: tauri::State<'_, AppState>,
) -> Result<project::ProjectInfo, String> {
    let token = state
        .token
        .lock()
        .unwrap()
        .clone()
        .ok_or("未登录")?;

    let service = ProjectService::new(state.api_base_url.clone(), token);
    service.get_my_project().await
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
fn greet(name: &str) -> String {
    format!("Hello, {}! Welcome to Tauri.", name)
}

fn main() {
    tauri::Builder::default()
        .manage(AppState {
            auth_service: Arc::new(Mutex::new(None)),
            token: Arc::new(Mutex::new(None)),
            api_base_url: "http://localhost:3000".to_string(),
        })
        .invoke_handler(tauri::generate_handler![
            cmd_login,
            cmd_get_project,
            cmd_upload_file,
            greet
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
