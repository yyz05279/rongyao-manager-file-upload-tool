import { invoke } from "@tauri-apps/api/tauri";

export const authAPI = {
  login: (username, password, apiUrl) =>
    invoke("cmd_login", { username, password, apiUrl }),
};

export const projectAPI = {
  getMyProject: () => invoke("cmd_get_project", {}),
};

export const uploadAPI = {
  uploadFile: (filePath, projectId, reporterId) =>
    invoke("cmd_upload_file", { filePath, projectId, reporterId }),
};

export const testAPI = {
  greet: (name) => invoke("greet", { name }),
};
