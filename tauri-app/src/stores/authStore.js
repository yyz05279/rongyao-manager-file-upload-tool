import { create } from "zustand";
import { authAPI, projectAPI } from "../services/api";

export const useAuthStore = create((set, get) => ({
  // 状态
  token: localStorage.getItem("token") || null,
  userInfo: JSON.parse(localStorage.getItem("userInfo") || "null"),
  projectInfo: null,
  loading: false,
  error: null,
  screen: localStorage.getItem("token") ? "upload" : "login", // login or upload

  // 方法
  login: async (username, password, apiUrl) => {
    set({ loading: true, error: null });
    try {
      const response = await authAPI.login(username, password, apiUrl);
      localStorage.setItem("token", response.token);
      localStorage.setItem("userInfo", JSON.stringify(response.user_info));
      
      set({
        token: response.token,
        userInfo: response.user_info,
        screen: "upload",
        loading: false,
      });
      
      return response;
    } catch (err) {
      set({ error: err.message || "登录失败", loading: false });
      throw err;
    }
  },

  logout: () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userInfo");
    set({
      token: null,
      userInfo: null,
      projectInfo: null,
      screen: "login",
    });
  },

  getProject: async () => {
    console.log("🔍 [authStore] 开始获取项目信息...");
    set({ loading: true, error: null });
    try {
      const projectInfo = await projectAPI.getMyProject();
      console.log("✅ [authStore] 项目信息获取成功:", projectInfo);
      set({ projectInfo, loading: false });
      return projectInfo;
    } catch (err) {
      console.error("❌ [authStore] 项目信息获取失败:", err);
      set({ error: err.message || "获取项目失败", loading: false });
      throw err;
    }
  },

  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}));
