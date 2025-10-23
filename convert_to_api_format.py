#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Excel解析结果转换为API批量导入格式
"""

import json
import sys


def convert_to_api_format(parsed_data, project_id, reporter_id):
    """
    将解析后的JSON转换为API批量导入格式
    
    :param parsed_data: 解析后的日报数据列表
    :param project_id: 项目ID
    :param reporter_id: 填报人ID
    :return: API格式的数据
    """
    reports = []
    
    for report in parsed_data:
        # 转换单个日报数据
        api_report = {
            "reportDate": report.get("reportDate", ""),
            "projectName": report.get("projectName", ""),
            "overallProgress": report.get("overallProgress", "normal"),
            "progressDescription": report.get("progressDescription", ""),
            "taskProgressList": json.dumps(report.get("taskProgressList", []), ensure_ascii=False),
            "tomorrowPlans": json.dumps(report.get("tomorrowPlans", []), ensure_ascii=False),
            "workerReports": json.dumps(report.get("workerReports", []), ensure_ascii=False),
            "machineryRentals": json.dumps(report.get("machineryRentals", []), ensure_ascii=False),
            "problemFeedbacks": json.dumps(report.get("problemFeedbacks", []), ensure_ascii=False),
            "requirements": json.dumps(report.get("requirements", []), ensure_ascii=False),
            "weather": report.get("weather"),
            "temperature": report.get("temperature"),
            "onSitePersonnelCount": report.get("onSitePersonnelCount", 0),
            "remarks": report.get("remarks")
        }
        reports.append(api_report)
    
    # 构建API格式
    api_data = {
        "projectId": project_id,
        "reporterId": reporter_id,
        "reports": reports
    }
    
    return api_data


def main():
    """主函数"""
    if len(sys.argv) < 4:
        print("使用方法: python convert_to_api_format.py <输入JSON文件> <项目ID> <填报人ID> [输出文件]")
        print("示例: python convert_to_api_format.py parsed.json 1 1 api_import.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    project_id = int(sys.argv[2])
    reporter_id = int(sys.argv[3])
    output_file = sys.argv[4] if len(sys.argv) > 4 else None
    
    print(f"读取解析结果: {input_file}")
    print(f"项目ID: {project_id}")
    print(f"填报人ID: {reporter_id}")
    print()
    
    try:
        # 读取解析后的JSON
        with open(input_file, 'r', encoding='utf-8') as f:
            parsed_data = json.load(f)
        
        print(f"读取到 {len(parsed_data)} 条日报数据")
        
        # 转换为API格式
        api_data = convert_to_api_format(parsed_data, project_id, reporter_id)
        
        print(f"转换完成，共 {len(api_data['reports'])} 条记录")
        print()
        
        # 输出或保存
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(api_data, f, ensure_ascii=False, indent=2)
            print(f"✓ API格式数据已保存到: {output_file}")
        else:
            # 输出到控制台
            print("="*80)
            print("API格式数据：")
            print("="*80)
            print(json.dumps(api_data, ensure_ascii=False, indent=2))
        
        # 显示统计信息
        print()
        print("="*80)
        print("数据统计：")
        print("="*80)
        print(f"项目ID: {api_data['projectId']}")
        print(f"填报人ID: {api_data['reporterId']}")
        print(f"日报数量: {len(api_data['reports'])}")
        
        # 显示日期范围
        if api_data['reports']:
            dates = [r['reportDate'] for r in api_data['reports']]
            print(f"日期范围: {min(dates)} 至 {max(dates)}")
        
        print()
        print("="*80)
        print("API调用示例：")
        print("="*80)
        if output_file:
            print(f"""
curl -X POST "http://42.192.76.234:8081
/api/v1/daily-reports/batch-import" \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d @{output_file}
""")
        else:
            print(f"""
# 先保存到文件
python {sys.argv[0]} {input_file} {project_id} {reporter_id} api_import.json

# 再调用API
curl -X POST "http://42.192.76.234:8081
/api/v1/daily-reports/batch-import" \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d @api_import.json
""")
        
    except FileNotFoundError:
        print(f"错误: 文件不存在: {input_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

