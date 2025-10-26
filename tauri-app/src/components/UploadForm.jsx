import React, { useState, useEffect } from "react";
import { open } from "@tauri-apps/plugin-dialog";
import { useAuthStore } from "../stores/authStore";
import { uploadAPI, excelAPI } from "../services/api";
import { DataPreview } from "./DataPreview";
import { ReportDetailDialog } from "./ReportDetailDialog";
import "./UploadForm.css";

export function UploadForm() {
  const [filePath, setFilePath] = useState("");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [parsedReports, setParsedReports] = useState([]);
  const [selectedReports, setSelectedReports] = useState([]);
  const [parsing, setParsing] = useState(false);
  const [selectedReport, setSelectedReport] = useState(null); // ✅ 选中的日报（用于详情弹窗）

  const { token, userInfo, projectInfo, logout, getProject } = useAuthStore();

  // ✅ 组件加载时确保有项目信息
  useEffect(() => {
    console.log("🔍 [UploadForm] useEffect 检查项目信息, projectInfo:", projectInfo);
    if (!projectInfo) {
      console.log("📋 [UploadForm] 项目信息为空，开始获取...");
      getProject()
        .then((info) => {
          console.log("✅ [UploadForm] 项目信息获取成功:", info);
        })
        .catch((err) => {
          console.error("⚠️ [UploadForm] 获取项目信息失败:", err);
        });
    } else {
      console.log("✅ [UploadForm] 项目信息已存在:", projectInfo);
    }
  }, [projectInfo, getProject]);

  // 角色映射（参考 Python 代码）
  const roleMap = {
    'ADMIN': '管理员',
    'MANAGER': '项目经理',
    'OPERATOR': '运维人员'
  };

  const getRoleText = (role) => {
    return roleMap[role] || role;
  };

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
        // 自动解析 Excel 文件（参考 Python 代码流程）
        await parseExcelFile(file);
      }
    } catch (err) {
      setMessage(`❌ 选择文件失败: ${err}`);
    }
  };

  const parseExcelFile = async (path) => {
    setParsing(true);
    setMessage("⏳ 正在解析 Excel 文件...");
    setParsedReports([]);
    setSelectedReports([]);
    
    try {
      const result = await excelAPI.parseExcel(path);
      if (result && result.reports) {
        // 用实际的项目名称替换 Excel 中解析的项目名称（参考 Python 代码）
        const reportsWithProjectName = result.reports.map(report => ({
          ...report,
          reporterName: projectInfo?.name || report.reporterName
        }));
        
        setParsedReports(reportsWithProjectName);
        setMessage(`✅ 解析成功！找到 ${result.reports.length} 条日报`);
      } else {
        setMessage("⚠️ 未找到日报数据");
      }
    } catch (err) {
      setMessage(`❌ 解析失败: ${err.message || err}`);
      console.error("Excel 解析错误:", err);
    } finally {
      setParsing(false);
    }
  };

  const handleToggleReport = (index) => {
    setSelectedReports((prev) =>
      prev.includes(index)
        ? prev.filter((i) => i !== index)
        : [...prev, index]
    );
  };

  const handleSelectAll = () => {
    setSelectedReports(parsedReports.map((_, idx) => idx));
  };

  const handleDeselectAll = () => {
    setSelectedReports([]);
  };

  // ✅ 双击打开详情弹窗（与Python版本保持一致）
  const handleRowDoubleClick = (index) => {
    if (index >= 0 && index < parsedReports.length) {
      setSelectedReport(parsedReports[index]);
    }
  };

  // ✅ 关闭详情弹窗
  const handleCloseDialog = () => {
    setSelectedReport(null);
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
        userInfo.id,
        token  // ✅ 传入token
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

  // ✅ 添加日志：监控 projectInfo 变化
  useEffect(() => {
    console.log("📊 [UploadForm] projectInfo 状态更新:", {
      hasProjectInfo: !!projectInfo,
      projectInfo: projectInfo,
    });
  }, [projectInfo]);

  return (
    <div className="upload-container">
      <div className="upload-header">
        <h1>📤 文件上传</h1>
        <div className="user-info">
          <span>
            👤 {userInfo?.name || userInfo?.username}
            {userInfo?.role && ` (${getRoleText(userInfo.role)})`}
            {projectInfo ? (
              <span style={{ marginLeft: '20px' }}>
                | 当前项目: <strong style={{ color: '#FFD700' }}>{projectInfo.name}</strong>
              </span>
            ) : (
              <span style={{ marginLeft: '20px', color: '#FF9800' }}>
                | 项目信息加载中...
              </span>
            )}
          </span>
          <button className="btn-logout" onClick={logout}>
            退出
          </button>
        </div>
      </div>

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

        {/* 数据预览表格 */}
        <DataPreview
          reports={parsedReports}
          selectedReports={selectedReports}
          onToggleReport={handleToggleReport}
          onSelectAll={handleSelectAll}
          onDeselectAll={handleDeselectAll}
          onRowDoubleClick={handleRowDoubleClick}
        />

        {/* ✅ 日报详情弹窗 */}
        {selectedReport && (
          <ReportDetailDialog
            report={selectedReport}
            onClose={handleCloseDialog}
          />
        )}

        <div className="progress-bar">
          <div className="progress" style={{ width: `${uploadProgress}%` }} />
        </div>

        <button
          onClick={handleUpload}
          disabled={loading || !filePath || selectedReports.length === 0}
          className="btn-upload"
        >
          {loading
            ? "上传中..."
            : selectedReports.length > 0
            ? `开始上传 (${selectedReports.length}/${parsedReports.length})`
            : "开始上传"}
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
