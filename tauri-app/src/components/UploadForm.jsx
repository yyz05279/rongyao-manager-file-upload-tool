import React, { useState } from "react";
import { open } from "@tauri-apps/plugin-dialog";
import { useAuthStore } from "../stores/authStore";
import { uploadAPI } from "../services/api";
import "./UploadForm.css";

export function UploadForm() {
  const [filePath, setFilePath] = useState("");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const { token, userInfo, projectInfo, logout, getProject } = useAuthStore();

  const handleSelectFile = async () => {
    try {
      const file = await open({
        filters: [
          { name: "Excel", extensions: ["xlsx", "xls"] },
          { name: "All", extensions: ["*"] },
        ],
      });
      if (file) {
        setFilePath(file);
        setMessage("");
      }
    } catch (err) {
      setMessage(`❌ 选择文件失败: ${err}`);
    }
  };

  const handleUpload = async () => {
    if (!filePath) {
      setMessage("❌ 请先选择文件");
      return;
    }

    if (!projectInfo) {
      setMessage("⚠️ 获取项目信息中...");
      try {
        await getProject();
      } catch (err) {
        setMessage(`❌ 获取项目失败: ${err}`);
        return;
      }
    }

    setLoading(true);
    setUploadProgress(0);
    setMessage("📤 上传中...");

    try {
      const result = await uploadAPI.uploadFile(
        filePath,
        projectInfo.id,
        userInfo.id
      );
      setMessage(`✅ ${result}`);
      setUploadProgress(100);
      setFilePath("");
    } catch (err) {
      setMessage(`❌ 上传失败: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-header">
        <h1>📤 文件上传</h1>
        <div className="user-info">
          <span>👤 {userInfo?.username}</span>
          <button className="btn-logout" onClick={logout}>
            退出
          </button>
        </div>
      </div>

      {projectInfo && (
        <div className="project-info">
          <p>
            <strong>项目:</strong> {projectInfo.name}
          </p>
          <p>
            <strong>状态:</strong> {projectInfo.status_display_name}
          </p>
        </div>
      )}

      <div className="upload-content">
        <div className="file-selector">
          <input
            type="text"
            value={filePath}
            readOnly
            placeholder="选择 Excel 文件"
            className="form-input"
          />
          <button
            onClick={handleSelectFile}
            disabled={loading}
            className="btn-select"
          >
            选择文件
          </button>
        </div>

        <div className="progress-bar">
          <div className="progress" style={{ width: `${uploadProgress}%` }} />
        </div>

        <button
          onClick={handleUpload}
          disabled={loading || !filePath}
          className="btn-upload"
        >
          {loading ? "上传中..." : "开始上传"}
        </button>

        {message && (
          <div className={`message ${message.includes("❌") ? "error" : ""}`}>
            {message}
          </div>
        )}
      </div>
    </div>
  );
}
