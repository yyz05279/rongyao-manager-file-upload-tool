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
        all_data.extend(sheet_data);
    }

    Ok(all_data)
}

fn parse_sheet(
    workbook: &mut Xlsx<std::io::BufReader<std::fs::File>>,
    sheet_name: &str,
) -> Result<Vec<Value>, String> {
    let range = workbook
        .worksheet_range(sheet_name)
        .ok_or_else(|| format!("工作表 '{}' 不存在", sheet_name))?
        .map_err(|e| format!("读取工作表失败: {}", e))?;

    let mut data = Vec::new();

    for (row_idx, row) in range.rows().enumerate() {
        // 跳过标题行
        if row_idx == 0 {
            continue;
        }

        // 提取行数据
        let record = json!({
            "rowIndex": row_idx,
            "date": row.get(0).map(|v| v.to_string()),
            "content": row.get(1).map(|v| v.to_string()),
            "status": row.get(2).map(|v| v.to_string()),
            "remark": row.get(3).map(|v| v.to_string()),
        });

        data.push(record);
    }

    Ok(data)
}
