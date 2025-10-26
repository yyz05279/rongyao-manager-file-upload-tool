import React, { useState, useEffect } from "react";
import { useAuthStore } from "../stores/authStore";
import "./ReportDetailDialog.css";

export function ReportDetailDialog({ report, onClose }) {
  const [activeTab, setActiveTab] = useState(0);
  const { projectInfo } = useAuthStore();

  // ✅ 添加日志：检查详情弹窗获取的数据
  useEffect(() => {
    console.log("📋 [ReportDetailDialog] 打开详情弹窗");
    console.log("  - report:", report);
    console.log("  - projectInfo:", projectInfo);
  }, [report, projectInfo]);

  if (!report) return null;

  // 进度状态映射
  const progressMap = {
    normal: "正常🟢",
    delayed: "滞后🔴",
    ahead: "超前🔵",
  };

  // 基本信息
  const reportDate = report.reportDate || "-";
  const reporterName = report.reporterName || "-";
  const projectName = projectInfo?.name || reporterName;
  const projectType = projectInfo?.typeDisplayName || "-";
  const projectStatus = projectInfo?.statusDisplayName || "-";
  const overallProgress = report.overallProgress || "normal";
  const progressText = progressMap[overallProgress] || "正常🟢";
  const progressDescription = report.progressDescription || "-";

  // 统计信息
  const taskCount = report.taskProgressList?.length || 0;
  const workerCount = report.onSitePersonnelCount || 0;
  const machineryCount = report.machineryRentals?.length || 0;
  const problemCount = report.problemFeedbacks?.length || 0;

  // 天气信息
  const weather = report.weather || "-";
  const temperature = report.temperature || "-";

  // 项目管理信息
  const manager = projectInfo?.manager || "-";
  const completionProgress = projectInfo?.completionProgress || 0;
  const estimatedSaltAmount = projectInfo?.estimatedSaltAmount || 0;
  const actualSaltAmount = projectInfo?.actualSaltAmount || 0;

  // 选项卡内容
  const tabs = [
    {
      title: "📋 逐项进度汇报",
      content: <TaskProgressTab data={report.taskProgressList || []} />,
    },
    {
      title: "📅 明日工作计划",
      content: <TomorrowPlansTab data={report.tomorrowPlans || []} />,
    },
    {
      title: "👷 各工种工作汇报",
      content: <WorkerReportsTab data={report.workerReports || []} />,
    },
    {
      title: "🚜 机械租赁情况",
      content: <MachineryTab data={report.machineryRentals || []} />,
    },
    {
      title: "⚠️ 问题反馈",
      content: (
        <ProblemsTab
          problems={report.problemFeedbacks || []}
          requirements={report.requirements || []}
        />
      ),
    },
  ];

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-content" onClick={(e) => e.stopPropagation()}>
        {/* 标题 */}
        <div className="dialog-header">
          <h2>📋 日报详细信息</h2>
          <button className="close-button" onClick={onClose}>
            ✕
          </button>
        </div>

        {/* 基本信息面板 */}
        <div className="basic-info-panel">
          <h3>基本信息</h3>

          <div className="info-grid">
            {/* 第一行 */}
            <InfoItem label="📅 日期:" value={reportDate} />
            <InfoItem label="📁 项目:" value={projectName} />

            {/* 项目详细信息 */}
            {projectInfo && (
              <>
                <InfoItem label="🏷️ 类型:" value={projectType} />
                <InfoItem label="📊 状态:" value={projectStatus} />
              </>
            )}

            {/* 进度状态 */}
            <InfoItem label="🎯 进度状态:" value={progressText} />

            {/* 统计信息 */}
            <InfoItem label="📋 任务数:" value={taskCount} />
            <InfoItem label="👷 人员数:" value={workerCount} />
            <InfoItem label="🚜 机械数:" value={machineryCount} />
            <InfoItem label="⚠️ 问题数:" value={problemCount} />

            {/* 天气信息 */}
            {weather && weather !== "-" && (
              <>
                <InfoItem label="☀️ 天气:" value={weather} />
                {temperature && temperature !== "-" && (
                  <InfoItem label="🌡️ 温度:" value={temperature} />
                )}
              </>
            )}

            {/* 项目管理信息 */}
            {projectInfo && (
              <>
                <InfoItem label="👨‍💼 项目经理:" value={manager} />
                <InfoItem
                  label="📈 项目完成度:"
                  value={`${completionProgress}%`}
                />
                {(estimatedSaltAmount > 0 || actualSaltAmount > 0) && (
                  <>
                    <InfoItem
                      label="🎯 计划熔盐量:"
                      value={`${estimatedSaltAmount} 吨`}
                    />
                    <InfoItem
                      label="✅ 实际熔盐量:"
                      value={`${actualSaltAmount} 吨`}
                    />
                  </>
                )}
              </>
            )}
          </div>

          {/* 进度描述 */}
          {progressDescription && progressDescription !== "-" && (
            <div className="progress-description">
              <strong>📝 进度描述:</strong> {progressDescription}
            </div>
          )}
        </div>

        {/* 选项卡 */}
        <div className="tabs-container">
          <div className="tabs-header">
            {tabs.map((tab, index) => (
              <button
                key={index}
                className={`tab-button ${activeTab === index ? "active" : ""}`}
                onClick={() => setActiveTab(index)}
              >
                {tab.title}
              </button>
            ))}
          </div>

          <div className="tabs-content">{tabs[activeTab].content}</div>
        </div>

        {/* 关闭按钮 */}
        <div className="dialog-footer">
          <button className="btn-close" onClick={onClose}>
            关闭
          </button>
        </div>
      </div>
    </div>
  );
}

// 信息项组件
function InfoItem({ label, value }) {
  return (
    <div className="info-item">
      <span className="info-label">{label}</span>
      <span className="info-value">{value}</span>
    </div>
  );
}

// 任务进度选项卡
function TaskProgressTab({ data }) {
  if (!data || data.length === 0) {
    return <div className="no-data">暂无任务进度数据</div>;
  }

  return (
    <div className="tab-table-container">
      <table className="detail-table">
        <thead>
          <tr>
            <th>序号</th>
            <th>任务名称</th>
            <th>计划进度</th>
            <th>实际进度</th>
            <th>偏差原因</th>
            <th>影响及措施</th>
          </tr>
        </thead>
        <tbody>
          {data.map((task, index) => (
            <tr key={index}>
              <td>{task.taskNo || "-"}</td>
              <td>{task.taskName || "-"}</td>
              <td>{task.plannedProgress || "-"}</td>
              <td>{task.actualProgress || "-"}</td>
              <td>{task.deviationReason || "-"}</td>
              <td>{task.impactMeasures || "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// 明日计划选项卡
function TomorrowPlansTab({ data }) {
  if (!data || data.length === 0) {
    return <div className="no-data">暂无明日计划数据</div>;
  }

  return (
    <div className="tab-table-container">
      <table className="detail-table">
        <thead>
          <tr>
            <th>序号</th>
            <th>任务名称</th>
            <th>目标</th>
            <th>负责人</th>
            <th>所需资源</th>
            <th>备注</th>
          </tr>
        </thead>
        <tbody>
          {data.map((plan, index) => (
            <tr key={index}>
              <td>{plan.planNo || "-"}</td>
              <td>{plan.taskName || "-"}</td>
              <td>{plan.goal || "-"}</td>
              <td>{plan.responsiblePerson || "-"}</td>
              <td>{plan.requiredResources || "-"}</td>
              <td>{plan.remarks || "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// 人员报告选项卡
function WorkerReportsTab({ data }) {
  if (!data || data.length === 0) {
    return <div className="no-data">暂无人员报告数据</div>;
  }

  return (
    <div className="tab-table-container">
      <table className="detail-table">
        <thead>
          <tr>
            <th>序号</th>
            <th>姓名</th>
            <th>工种</th>
            <th>类型</th>
            <th>工作内容</th>
            <th>工时</th>
          </tr>
        </thead>
        <tbody>
          {data.map((worker, index) => (
            <tr key={index}>
              <td>{worker.seqNo || "-"}</td>
              <td>{worker.name || "-"}</td>
              <td>{worker.jobType || "-"}</td>
              <td>{worker.workerType || "-"}</td>
              <td>{worker.workContent || "-"}</td>
              <td>{worker.workHours || "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// 机械租赁选项卡
function MachineryTab({ data }) {
  if (!data || data.length === 0) {
    return <div className="no-data">暂无机械租赁数据</div>;
  }

  return (
    <div className="tab-table-container">
      <table className="detail-table">
        <thead>
          <tr>
            <th>序号</th>
            <th>机械名称</th>
            <th>数量</th>
            <th>吨位</th>
            <th>用途</th>
            <th>班次</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.seqNo || "-"}</td>
              <td>{item.machineName || "-"}</td>
              <td>{item.quantity || "-"}</td>
              <td>{item.tonnage || "-"}</td>
              <td>{item.usage || "-"}</td>
              <td>{item.shift || "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// 问题反馈选项卡（包含问题和需求）
function ProblemsTab({ problems, requirements }) {
  return (
    <div className="problems-tab">
      {/* 问题反馈分组 */}
      <div className="problems-group">
        <h4 className="group-title problem-title">1. 问题反馈</h4>
        {!problems || problems.length === 0 ? (
          <div className="no-data success">✅ 暂无问题反馈</div>
        ) : (
          <div className="tab-table-container">
            <table className="detail-table">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>问题描述</th>
                  <th>原因</th>
                  <th>影响</th>
                  <th>处理进度</th>
                </tr>
              </thead>
              <tbody>
                {problems.map((problem, index) => (
                  <tr key={index}>
                    <td>{problem.problemNo || "-"}</td>
                    <td className="problem-description">
                      {problem.description || "-"}
                    </td>
                    <td>{problem.reason || "-"}</td>
                    <td>{problem.impact || "-"}</td>
                    <td>{problem.progress || "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* 需求描述分组 */}
      <div className="requirements-group">
        <h4 className="group-title requirement-title">2. 需求描述</h4>
        {!requirements || requirements.length === 0 ? (
          <div className="no-data">暂无需求描述</div>
        ) : (
          <div className="tab-table-container">
            <table className="detail-table">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>需求描述</th>
                  <th>紧急程度</th>
                  <th>期望时间</th>
                </tr>
              </thead>
              <tbody>
                {requirements.map((req, index) => (
                  <tr key={index}>
                    <td>{req.requirementNo || "-"}</td>
                    <td>{req.description || "-"}</td>
                    <td>{req.urgencyLevel || "-"}</td>
                    <td>{req.expectedTime || "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

