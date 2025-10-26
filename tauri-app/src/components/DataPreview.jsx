import React from "react";
import "./DataPreview.css";

export function DataPreview({ 
  reports, 
  selectedReports = [], 
  onToggleReport, 
  onSelectAll, 
  onDeselectAll, 
  onRowDoubleClick,
  title = "数据预览", // ✅ 自定义标题
  readOnly = false, // ✅ 只读模式（已上传的日报）
  emptyMessage = "📋 添加文件后，将自动解析并显示数据预览" // ✅ 自定义空状态提示
}) {
  if (!reports || reports.length === 0) {
    return (
      <div className="preview-empty">
        <p>{emptyMessage}</p>
      </div>
    );
  }

  const progressMap = {
    normal: "正常",
    delayed: "滞后",
    ahead: "超前",
  };

  const isAllSelected = !readOnly && reports.every((_, idx) => selectedReports.includes(idx));

  return (
    <div className={`data-preview ${readOnly ? 'readonly' : ''}`}>
      <div className="preview-header">
        <span className="preview-title">{title} ({reports.length} 条日报)</span>
        {!readOnly && (
          <div className="preview-actions">
            <button 
              className="btn-select-action btn-select-all" 
              onClick={onSelectAll}
              disabled={isAllSelected}
            >
              ✓ 全选
            </button>
            <button 
              className="btn-select-action btn-deselect-all" 
              onClick={onDeselectAll}
              disabled={selectedReports.length === 0}
            >
              ✗ 反选
            </button>
          </div>
        )}
      </div>

      <div className="preview-table-container">
        <table className="preview-table">
          <thead>
            <tr>
              <th>{readOnly ? '👁' : '✓'}</th>
              <th>日期</th>
              <th>项目名称</th>
              <th>进度状态</th>
              <th>任务数</th>
              <th>人员数</th>
              <th>机械数</th>
              <th>问题数</th>
              <th>天气</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((report, idx) => (
              <tr 
                key={idx}
                onDoubleClick={() => onRowDoubleClick?.(idx)}
                style={{ cursor: onRowDoubleClick ? 'pointer' : 'default' }}
                className={readOnly ? 'uploaded-row' : ''}
              >
                <td onClick={(e) => e.stopPropagation()}>
                  {readOnly ? (
                    <span className="view-icon" title="双击查看详情">👁</span>
                  ) : (
                    <input
                      type="checkbox"
                      checked={selectedReports.includes(idx)}
                      onChange={() => onToggleReport(idx)}
                    />
                  )}
                </td>
                <td>{report.reportDate}</td>
                <td>{report.reporterName}</td>
                <td className={`progress-${report.overallProgress}`}>
                  {progressMap[report.overallProgress] || "正常"}
                </td>
                <td>{report.taskProgressList?.length || 0}</td>
                <td>{report.onSitePersonnelCount || 0}</td>
                <td>{report.machineryRentals?.length || 0}</td>
                <td className={(report.problemFeedbacks?.length || 0) > 0 ? "has-problems" : ""}>
                  {report.problemFeedbacks?.length || 0}
                </td>
                <td>{report.weather || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

