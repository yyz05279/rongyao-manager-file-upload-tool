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

    // 解析日报数据（简化版）
    // 从工作表名称获取日期，或从第一行获取
    let report_date = sheet_name.to_string();
    
    // 获取项目名称（通常在第一行）
    let project_name = if let Some(first_row) = rows.get(0) {
        get_cell_value(first_row, 0)
            .replace("项目工作日报", "")
            .replace("日报", "")
            .trim()
            .to_string()
    } else {
        "未知项目".to_string()
    };

    // 简单统计（实际应该根据 Excel 结构解析）
    let total_rows = rows.len().saturating_sub(1); // 减去标题行

    let report = json!({
        "reportDate": report_date,
        "reporterName": if project_name.is_empty() { "未知项目" } else { &project_name },
        "overallProgress": "normal",
        "taskCount": total_rows,
        "onSitePersonnelCount": 0,
        "machineryCount": 0,
        "problemCount": 0,
        "weather": "-",
        "temperature": "-"
    });

    Ok(Some(report))
}
