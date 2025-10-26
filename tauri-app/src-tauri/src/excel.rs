use calamine::{open_workbook, Reader, Xlsx, DataType};
use serde_json::{json, Value};

pub fn parse_excel_file(file_path: &str) -> Result<Vec<Value>, String> {
    let mut workbook: Xlsx<_> = open_workbook(file_path)
        .map_err(|e| format!("无法打开 Excel 文件: {}", e))?;

    let mut all_data = Vec::new();

    // 获取所有工作表名称
    let sheet_names: Vec<String> = workbook.sheet_names().to_vec();

    for sheet_name in sheet_names.iter() {
        let sheet_data = parse_sheet(&mut workbook, sheet_name)?;
        if let Some(report) = sheet_data {
            all_data.push(report);
        }
    }

    Ok(all_data)
}

fn get_cell_value(row: &[DataType], col: usize) -> String {
    row.get(col)
        .map(|v| v.to_string())
        .unwrap_or_default()
        .trim()
        .to_string()
}

fn parse_sheet(
    workbook: &mut Xlsx<std::io::BufReader<std::fs::File>>,
    sheet_name: &str,
) -> Result<Option<Value>, String> {
    let range = workbook
        .worksheet_range(sheet_name)
        .ok_or_else(|| format!("工作表 '{}' 不存在", sheet_name))?
        .map_err(|e| format!("读取工作表失败: {}", e))?;

    let rows: Vec<_> = range.rows().collect();
    
    if rows.is_empty() {
        return Ok(None);
    }

    // 解析日报数据（与Python版本保持一致）
    let report_date = sheet_name.to_string();
    
    // 获取项目名称（第1行第1列，通常是"XXX项目工作日报"）
    let project_name = if let Some(first_row) = rows.get(0) {
        get_cell_value(first_row, 0)
            .replace("项目工作日报", "")
            .replace("日报", "")
            .trim()
            .to_string()
    } else {
        String::new()
    };

    // 解析整体进度描述（第3行第5列）
    let progress_description = if let Some(row) = rows.get(2) {
        get_cell_value(row, 4)
    } else {
        String::new()
    };

    // 根据描述判断进度状态
    let overall_progress = if progress_description.contains("正常") {
        "normal"
    } else if progress_description.contains("滞后") {
        "delayed"
    } else if progress_description.contains("超前") {
        "ahead"
    } else {
        "normal"
    };

    // 解析逐项进度汇报（第6-20行，序号2.x）
    let task_progress_list = parse_task_progress(&rows, 5, 19);
    
    // 解析明天工作计划（第6-20行，序号3.x）
    let tomorrow_plans = parse_tomorrow_plans(&rows, 5, 19);
    
    // 解析各工种工作汇报（从第20行开始，区域二）
    let worker_reports = parse_worker_reports(&rows, 19, 69);
    
    // 统计现场总人数
    let on_site_personnel_count = worker_reports.len();
    
    // 解析机械租赁情况（从第20行开始，区域三）
    let machinery_rentals = parse_machinery_rentals(&rows, 19, 69);
    
    // 解析问题反馈（从第20行开始，区域四，序号1.x或纯数字）
    let problem_feedbacks = parse_problem_feedbacks(&rows, 19, 79);
    
    // 解析需求描述（从第20行开始，区域四，子区域2）
    let requirements = parse_requirements(&rows, 19, 79);

    let report = json!({
        "reportDate": report_date,
        "reporterName": project_name,
        "overallProgress": overall_progress,
        "progressDescription": progress_description,
        "taskProgressList": task_progress_list,
        "tomorrowPlans": tomorrow_plans,
        "workerReports": worker_reports,
        "machineryRentals": machinery_rentals,
        "problemFeedbacks": problem_feedbacks,
        "requirements": requirements,
        "onSitePersonnelCount": on_site_personnel_count,
        "weather": null,
        "temperature": null,
        "remarks": null
    });

    Ok(Some(report))
}

// 解析逐项进度汇报（序号2.x）
fn parse_task_progress(rows: &[&[DataType]], start_row: usize, end_row: usize) -> Vec<Value> {
    let mut tasks = Vec::new();
    
    for i in start_row..=end_row.min(rows.len().saturating_sub(1)) {
        if let Some(row) = rows.get(i) {
            let task_no = get_cell_value(row, 0);
            let task_name = get_cell_value(row, 1);
            
            // 只保存序号以"2."开头且有内容的任务
            if !task_name.is_empty() && task_no.starts_with("2.") {
                let planned_progress = get_cell_value(row, 2);
                let actual_progress = get_cell_value(row, 4);
                let deviation_reason = get_cell_value(row, 5);
                let impact_measures = get_cell_value(row, 6);
                
                tasks.push(json!({
                    "taskNo": task_no,
                    "taskName": task_name,
                    "plannedProgress": planned_progress,
                    "actualProgress": actual_progress,
                    "deviationReason": deviation_reason,
                    "impactMeasures": impact_measures
                }));
            }
        }
    }
    
    tasks
}

// 解析明天工作计划（序号3.x）
fn parse_tomorrow_plans(rows: &[&[DataType]], start_row: usize, end_row: usize) -> Vec<Value> {
    let mut plans = Vec::new();
    
    for i in start_row..=end_row.min(rows.len().saturating_sub(1)) {
        if let Some(row) = rows.get(i) {
            let plan_no = get_cell_value(row, 0);
            let task_name = get_cell_value(row, 1);
            
            // 只保存序号以"3."开头且有内容的计划
            if !task_name.is_empty() && plan_no.starts_with("3.") {
                let goal = get_cell_value(row, 2);
                let responsible_person = get_cell_value(row, 4);
                let required_resources = get_cell_value(row, 5);
                let remarks = get_cell_value(row, 6);
                
                plans.push(json!({
                    "planNo": plan_no,
                    "taskName": task_name,
                    "goal": goal,
                    "responsiblePerson": responsible_person,
                    "requiredResources": required_resources,
                    "remarks": remarks
                }));
            }
        }
    }
    
    plans
}

// 解析各工种工作汇报（区域二）
fn parse_worker_reports(rows: &[&[DataType]], start_row: usize, end_row: usize) -> Vec<Value> {
    let mut workers = Vec::new();
    let mut in_target_area = false;
    
    for i in start_row..=end_row.min(rows.len().saturating_sub(1)) {
        if let Some(row) = rows.get(i) {
            let seq_no = get_cell_value(row, 0);
            let name = get_cell_value(row, 1);
            
            // 检测区域标题
            if seq_no == "二" {
                in_target_area = true;
                continue;
            }
            
            // 遇到下一个区域标题，停止解析
            if (seq_no == "三" || seq_no == "四" || seq_no == "五") && in_target_area {
                break;
            }
            
            // 只在目标区域内解析数据
            if !in_target_area {
                continue;
            }
            
            // 跳过表头行
            if name == "姓名" || name == "序号" {
                continue;
            }
            
            // 只保存有姓名的记录
            if !name.is_empty() {
                let job_type = get_cell_value(row, 2);
                let worker_type = get_cell_value(row, 3);
                let work_content = get_cell_value(row, 4);
                let work_hours = get_cell_value(row, 6);
                
                workers.push(json!({
                    "seqNo": seq_no,
                    "name": name,
                    "jobType": job_type,
                    "workerType": worker_type,
                    "workContent": work_content,
                    "workHours": work_hours
                }));
            }
        }
    }
    
    workers
}

// 解析机械租赁情况（区域三）
fn parse_machinery_rentals(rows: &[&[DataType]], start_row: usize, end_row: usize) -> Vec<Value> {
    let mut machinery = Vec::new();
    let mut in_target_area = false;
    
    for i in start_row..=end_row.min(rows.len().saturating_sub(1)) {
        if let Some(row) = rows.get(i) {
            let seq_no = get_cell_value(row, 0);
            let machine_name = get_cell_value(row, 1);
            
            // 检测区域标题
            if seq_no == "三" {
                in_target_area = true;
                continue;
            }
            
            // 遇到下一个区域标题，停止解析
            if (seq_no == "四" || seq_no == "五" || seq_no == "六") && in_target_area {
                break;
            }
            
            // 只在目标区域内解析数据
            if !in_target_area {
                continue;
            }
            
            // 跳过表头行
            if machine_name == "机械名称" || machine_name == "序号" {
                continue;
            }
            
            // 只保存有机械名称的记录
            if !machine_name.is_empty() {
                let quantity = get_cell_value(row, 2);
                let tonnage = get_cell_value(row, 3);
                let usage = get_cell_value(row, 4);
                let shift = get_cell_value(row, 5);
                let remarks = get_cell_value(row, 6);
                
                machinery.push(json!({
                    "seqNo": seq_no,
                    "machineName": machine_name,
                    "quantity": quantity,
                    "tonnage": tonnage,
                    "usage": usage,
                    "shift": shift,
                    "remarks": remarks
                }));
            }
        }
    }
    
    machinery
}

// 解析问题反馈（区域四 -> 问题数据）
fn parse_problem_feedbacks(rows: &[&[DataType]], start_row: usize, end_row: usize) -> Vec<Value> {
    let mut problems = Vec::new();
    let mut in_target_area = false;
    
    for i in start_row..=end_row.min(rows.len().saturating_sub(1)) {
        if let Some(row) = rows.get(i) {
            let problem_no = get_cell_value(row, 0);
            let description = get_cell_value(row, 1);
            
            // 检测区域标题
            if problem_no == "四" {
                in_target_area = true;
                continue;
            }
            
            // 遇到下一个区域标题，停止解析
            if (problem_no == "五" || problem_no == "六") && in_target_area {
                break;
            }
            
            // 只在目标区域内解析数据
            if !in_target_area {
                continue;
            }
            
            // 跳过表头行和子标题行
            if description == "问题描述" || description == "问题反馈" || description == "序号" || description == "需求描述" {
                continue;
            }
            
            // 跳过子标题行（序号为"1"）
            if problem_no == "1" {
                continue;
            }
            
            // 支持两种格式：
            // 1. 纯数字格式（2、3、4...）- 10-19日之后的格式
            // 2. "1.x"格式（1.1、1.2...）- 10-19日的格式
            let is_numeric = problem_no.chars().all(|c| c.is_numeric()) && problem_no != "1";
            let is_sub_problem = problem_no.starts_with("1.") && problem_no.len() > 2;
            
            if !description.is_empty() && (is_numeric || is_sub_problem) {
                let reason = get_cell_value(row, 3);
                let impact = get_cell_value(row, 4);
                let progress = get_cell_value(row, 5);
                
                problems.push(json!({
                    "problemNo": problem_no,
                    "description": description,
                    "reason": reason,
                    "impact": impact,
                    "progress": progress
                }));
            }
        }
    }
    
    problems
}

// 解析需求描述（区域四 -> 子区域2）
fn parse_requirements(rows: &[&[DataType]], start_row: usize, end_row: usize) -> Vec<Value> {
    let mut requirements = Vec::new();
    let mut in_target_area = false;
    let mut in_requirements_section = false;
    
    for i in start_row..=end_row.min(rows.len().saturating_sub(1)) {
        if let Some(row) = rows.get(i) {
            let req_no = get_cell_value(row, 0);
            let description = get_cell_value(row, 1);
            
            // 检测区域标题
            if req_no == "四" {
                in_target_area = true;
                continue;
            }
            
            // 遇到下一个区域标题，停止解析
            if (req_no == "五" || req_no == "六") && in_target_area {
                break;
            }
            
            // 只在目标区域内解析数据
            if !in_target_area {
                continue;
            }
            
            // 检测需求描述子标题（序号为"2"且内容为"需求描述"或"需求"）
            if req_no == "2" && (description == "需求描述" || description == "需求") {
                in_requirements_section = true;
                continue;
            }
            
            // 只在需求描述子区域内解析数据
            if !in_requirements_section {
                continue;
            }
            
            // 跳过表头行
            if description == "需求描述" || description == "问题反馈" || description == "序号" {
                continue;
            }
            
            // 保存有需求描述的记录
            if !description.is_empty() {
                let urgency_level = get_cell_value(row, 3);
                let expected_time = get_cell_value(row, 5);
                
                requirements.push(json!({
                    "requirementNo": req_no,
                    "description": description,
                    "urgencyLevel": urgency_level,
                    "expectedTime": expected_time
                }));
            }
        }
    }
    
    requirements
}
