import React, { useState } from "react";
import { useAuthStore } from "../stores/authStore";
import "./LoginForm.css";

// 固定的 API 地址
const API_URL = "http://42.192.76.234:8081";

export function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [localError, setLocalError] = useState("");

  const { login, loading, getProject } = useAuthStore();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLocalError("");

    if (!username) {
      setLocalError("请输入用户名或手机号");
      return;
    }
    if (!password) {
      setLocalError("请输入密码");
      return;
    }

    try {
      // 登录成功
      console.log("🔐 [LoginForm] 开始登录...");
      await login(username, password, API_URL);
      console.log("✅ [LoginForm] 登录成功");
      
      // ✅ 立即获取项目信息（与Python版本保持一致）
      try {
        console.log("📋 [LoginForm] 开始获取项目信息...");
        const projectInfo = await getProject();
        console.log("✅ [LoginForm] 项目信息已获取:", projectInfo);
      } catch (err) {
        console.error("⚠️ [LoginForm] 获取项目信息失败:", err);
        // 不阻止登录流程，项目信息获取失败不影响登录
      }
      
      onLoginSuccess?.();
    } catch (err) {
      console.error("❌ [LoginForm] 登录失败:", err);
      setLocalError(err.message || "登录失败");
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h1>🔐 熔盐管理文件上传工具</h1>

        <div className="form-group">
          <label>用户名/手机号</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="输入用户名或手机号"
            className="form-input"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label>密码</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="输入密码"
            className="form-input"
            disabled={loading}
          />
        </div>

        {localError && <div className="error-message">❌ {localError}</div>}

        <button type="submit" disabled={loading} className="btn-login">
          {loading ? "登录中..." : "登录"}
        </button>
      </form>
    </div>
  );
}
