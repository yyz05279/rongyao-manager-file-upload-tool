import { create } from "zustand";
import { authAPI, projectAPI } from "../services/api";

export const useAuthStore = create((set, get) => ({
  // 状态
  token: localStorage.getItem("token") || null,
  refreshToken: localStorage.getItem("refreshToken") || null,
  tokenExpiresAt: parseInt(localStorage.getItem("tokenExpiresAt") || "0", 10),
  userInfo: JSON.parse(localStorage.getItem("userInfo") || "null"),
  projectInfo: null,
  loading: false,
  error: null,
  screen: localStorage.getItem("token") ? "upload" : "login", // login or upload

  // 方法
  login: async (username, password, apiUrl) => {
    console.log("🔐 [authStore] 开始登录...");
    set({ loading: true, error: null });
    try {
      const response = await authAPI.login(username, password, apiUrl);
      console.log("✅ [authStore] 登录响应:", response);
      
      // ✅ 计算Token过期时间（24小时后）
      const tokenExpiresAt = Date.now() + 24 * 60 * 60 * 1000;
      
      // ✅ 保存到localStorage
      localStorage.setItem("token", response.token);
      localStorage.setItem("refreshToken", response.refresh_token);
      localStorage.setItem("tokenExpiresAt", tokenExpiresAt.toString());
      localStorage.setItem("userInfo", JSON.stringify(response.user_info));
      
      console.log("✅ [authStore] Token已保存到localStorage");
      console.log("  - Token过期时间:", new Date(tokenExpiresAt).toLocaleString());
      
      set({
        token: response.token,
        refreshToken: response.refresh_token,
        tokenExpiresAt: tokenExpiresAt,
        userInfo: response.user_info,
        screen: "upload",
        loading: false,
      });
      
      // ✅ 启动Token自动刷新定时器
      get().startTokenRefreshTimer();
      
      return response;
    } catch (err) {
      console.error("❌ [authStore] 登录失败:", err);
      set({ error: err.message || "登录失败", loading: false });
      throw err;
    }
  },

  logout: () => {
    console.log("👋 [authStore] 用户退出登录");
    
    // ✅ 清除定时器
    get().stopTokenRefreshTimer();
    
    // ✅ 清除localStorage
    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("tokenExpiresAt");
    localStorage.removeItem("userInfo");
    
    set({
      token: null,
      refreshToken: null,
      tokenExpiresAt: 0,
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

  // ✅ 刷新Token
  refreshToken: async () => {
    console.log("🔄 [authStore] 开始刷新Token");
    try {
      const newToken = await authAPI.refreshToken();
      console.log("✅ [authStore] Token刷新成功");
      
      // ✅ 更新Token和过期时间
      const tokenExpiresAt = Date.now() + 24 * 60 * 60 * 1000;
      
      localStorage.setItem("token", newToken);
      localStorage.setItem("tokenExpiresAt", tokenExpiresAt.toString());
      
      set({
        token: newToken,
        tokenExpiresAt: tokenExpiresAt,
      });
      
      console.log("✅ [authStore] Token过期时间已更新:", new Date(tokenExpiresAt).toLocaleString());
      
      return newToken;
    } catch (err) {
      console.error("❌ [authStore] Token刷新失败:", err);
      // Token刷新失败，清除登录状态
      get().logout();
      throw err;
    }
  },

  // ✅ 检查Token是否即将过期（提前30分钟刷新）
  shouldRefreshToken: () => {
    const { tokenExpiresAt } = get();
    if (!tokenExpiresAt) return false;
    
    const now = Date.now();
    const timeUntilExpiry = tokenExpiresAt - now;
    const thirtyMinutes = 30 * 60 * 1000;
    
    // 如果Token在30分钟内过期，则需要刷新
    return timeUntilExpiry < thirtyMinutes;
  },

  // ✅ 启动Token自动刷新定时器
  refreshTimerId: null,
  startTokenRefreshTimer: () => {
    console.log("⏰ [authStore] 启动Token自动刷新定时器");
    
    // 清除旧的定时器
    get().stopTokenRefreshTimer();
    
    // 每5分钟检查一次Token是否需要刷新
    const timerId = setInterval(() => {
      if (get().shouldRefreshToken()) {
        console.log("🔄 [authStore] Token即将过期，自动刷新");
        get().refreshToken().catch(err => {
          console.error("❌ [authStore] 自动刷新Token失败:", err);
        });
      }
    }, 5 * 60 * 1000); // 5分钟
    
    set({ refreshTimerId: timerId });
  },

  // ✅ 停止Token自动刷新定时器
  stopTokenRefreshTimer: () => {
    const { refreshTimerId } = get();
    if (refreshTimerId) {
      console.log("⏸️ [authStore] 停止Token自动刷新定时器");
      clearInterval(refreshTimerId);
      set({ refreshTimerId: null });
    }
  },

  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}));
