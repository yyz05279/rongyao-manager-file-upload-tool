import { invoke } from "@tauri-apps/api/core";

// 检查 Tauri 环境
const checkTauriEnvironment = () => {
  if (typeof window.__TAURI__ === 'undefined') {
    throw new Error(
      '❌ Tauri 环境未初始化！\n\n' +
      '请使用以下命令启动应用：\n' +
      'cd tauri-app\n' +
      'npm run tauri:dev\n\n' +
      '不要使用 npm run dev（这只会启动前端服务器）'
    );
  }
};

// 包装 invoke 函数，添加环境检查
const safeInvoke = async (cmd, args) => {
  checkTauriEnvironment();
  try {
    return await invoke(cmd, args);
  } catch (error) {
    console.error(`Tauri invoke error [${cmd}]:`, error);
    throw error;
  }
};

export const authAPI = {
  login: (username, password, apiUrl) =>
    safeInvoke("cmd_login", { username, password, apiUrl }),
};

export const projectAPI = {
  getMyProject: () => safeInvoke("cmd_get_project", {}),
};

export const uploadAPI = {
  uploadFile: (filePath, projectId, reporterId) =>
    safeInvoke("cmd_upload_file", { filePath, projectId, reporterId }),
};

export const testAPI = {
  greet: (name) => safeInvoke("greet", { name }),
};
