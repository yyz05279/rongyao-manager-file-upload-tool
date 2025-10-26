import { invoke } from "@tauri-apps/api/core";

// API 调用包装函数，提供更好的错误处理
const safeInvoke = async (cmd, args) => {
  try {
    return await invoke(cmd, args);
  } catch (error) {
    console.error(`Tauri invoke error [${cmd}]:`, error);
    // 提供用户友好的错误信息
    if (error.message) {
      throw new Error(error.message);
    }
    throw error;
  }
};

export const authAPI = {
  login: (username, password, apiUrl) =>
    safeInvoke("cmd_login", { username, password, apiUrl }),
  
  refreshToken: () =>
    safeInvoke("cmd_refresh_token", {}),
};

export const projectAPI = {
  getMyProject: () => safeInvoke("cmd_get_project", {}),
};

export const uploadAPI = {
  uploadFile: (filePath, projectId, reporterId) =>
    safeInvoke("cmd_upload_file", { filePath, projectId, reporterId }),
};

export const excelAPI = {
  parseExcel: (filePath) => safeInvoke("cmd_parse_excel", { filePath }),
};

export const testAPI = {
  greet: (name) => safeInvoke("greet", { name }),
};
