# 全局 Token 管理说明

## 📋 功能概述

实现统一的 token 管理机制，所有 API 请求自动在 header 中添加 token，除了登录和退出接口。

## ✨ 实现方案

### 1. 基础服务类（BaseService）

创建了一个基础服务类，封装所有 HTTP 请求方法，自动处理 token 的添加。

**文件位置**：`services/base_service.py`

**核心功能**：

- 统一的 HTTP 请求封装（GET、POST、PUT、DELETE）
- 自动添加 token 到请求头
- 统一的响应解析和错误处理
- 安全的日志记录（隐藏敏感信息）

### 2. Token 添加机制

#### 请求头结构

```python
headers = {
    'Content-Type': 'application/json',
    'token': 'your_token_here'  # 自动添加
}
```

#### Token 添加逻辑

```python
def _get_headers(self, custom_headers: Dict = None, include_token: bool = True) -> Dict:
    """
    获取请求头，自动添加token

    :param custom_headers: 自定义请求头
    :param include_token: 是否包含token
    :return: 完整的请求头
    """
    headers = {
        'Content-Type': 'application/json'
    }

    # 添加token到请求头
    if include_token and self.token:
        headers['token'] = self.token

    # 合并自定义请求头
    if custom_headers:
        headers.update(custom_headers)

    return headers
```

## 🎯 使用方式

### 1. 需要 Token 的请求（默认）

```python
# 示例：获取项目信息
class ProjectService(BaseService):
    def get_my_project(self):
        # 自动添加token
        response = self.get('/api/v1/projects/my-project', include_token=True)
        return self.parse_response(response)
```

### 2. 不需要 Token 的请求

```python
# 示例：登录接口
response = self.post(
    '/api/v1/auth/login',
    json_data=login_data,
    include_token=False  # 登录时不需要token
)
```

## 📂 文件结构

```
services/
├── base_service.py       # 基础服务类（新增）✨
├── auth_service.py       # 认证服务（不继承BaseService）
├── project_service.py    # 项目服务（继承BaseService）✅
├── upload_service.py     # 上传服务（已废弃，功能移到UploadThread）
└── config_service.py     # 配置服务
```

## 🔧 各服务实现

### 1. BaseService（基础服务）

**职责**：

- 提供统一的 HTTP 请求方法
- 自动管理 token
- 统一错误处理
- 安全日志记录

**方法列表**：

| 方法               | 说明        | Token    |
| ------------------ | ----------- | -------- |
| `get()`            | GET 请求    | 默认添加 |
| `post()`           | POST 请求   | 默认添加 |
| `put()`            | PUT 请求    | 默认添加 |
| `delete()`         | DELETE 请求 | 默认添加 |
| `parse_response()` | 解析响应    | -        |

**示例代码**：

```python
from services.base_service import BaseService

# 创建服务实例
service = BaseService(api_base_url, token)

# GET 请求（自动添加token）
response = service.get('/api/v1/users/profile')
data = service.parse_response(response)

# POST 请求（自动添加token）
response = service.post('/api/v1/data', json_data={'key': 'value'})
data = service.parse_response(response)

# 不添加token的请求
response = service.post('/api/v1/auth/login',
                       json_data=login_data,
                       include_token=False)
```

### 2. ProjectService（项目服务）

**改动前**：

```python
class ProjectService:
    def get_my_project(self):
        url = f"{self.api_base_url}/api/v1/projects/my-project"
        headers = {
            "Content-Type": "application/json",
            "token": self.token  # 手动添加token
        }
        response = requests.get(url, headers=headers)
        # ... 处理响应
```

**改动后**：

```python
class ProjectService(BaseService):
    def get_my_project(self):
        # 使用基础服务的GET方法，自动添加token
        response = self.get('/api/v1/projects/my-project', include_token=True)
        return self.parse_response(response)
```

**优势**：

- ✅ 代码更简洁（从 30+ 行减少到 5 行）
- ✅ 自动处理 token
- ✅ 统一错误处理
- ✅ 更易维护

### 3. UploadThread（上传线程）

**改动前**：

```python
import_url = f"{self.api_base_url}/api/v1/daily-reports/batch-import"
headers = {
    'Authorization': f'Bearer {self.token}',
    'Content-Type': 'application/json'
}
response = requests.post(import_url, json=api_data, headers=headers)
```

**改动后**：

```python
# 创建基础服务实例
base_service = BaseService(self.api_base_url, self.token)

# 调用POST方法，自动添加token
response = base_service.post(
    '/api/v1/daily-reports/batch-import',
    json_data=api_data,
    include_token=True
)

# 解析响应
data = base_service.parse_response(response)
```

**优势**：

- ✅ 统一使用 `token` 字段（不再是 `Authorization`）
- ✅ 自动添加到请求头
- ✅ 统一的错误处理

### 4. AuthService（认证服务）

**特殊说明**：

- ❌ **不继承** BaseService
- ❌ 登录和刷新接口**不需要** token
- ✅ 保持独立实现

**原因**：

1. 登录时还没有 token
2. 刷新 token 使用 refreshToken，不是 token
3. 避免循环依赖

## 🔒 安全性

### 1. 日志安全

```python
def _safe_log_headers(self, headers: Dict) -> Dict:
    """隐藏敏感信息"""
    safe_headers = headers.copy()
    if 'token' in safe_headers and safe_headers['token']:
        safe_headers['token'] = f"{safe_headers['token'][:20]}..."
    return safe_headers
```

**效果**：

```
# 原始token（不会记录）
token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ

# 日志中显示
token: eyJhbGciOiJIUzI1Ni...
```

### 2. 密码安全

```python
def _safe_log_data(self, data: Dict) -> str:
    """隐藏密码"""
    if isinstance(data, dict) and 'password' in data:
        safe_data = data.copy()
        safe_data['password'] = '******'
        return str(safe_data)
    return str(data)
```

## 📊 Token 使用场景

| 接口                                | 需要 Token | 说明               |
| ----------------------------------- | ---------- | ------------------ |
| 登录 (`/api/v1/auth/login`)         | ❌         | 登录时还没有 token |
| 刷新 Token (`/api/v1/auth/refresh`) | ❌         | 使用 refreshToken  |
| 退出登录                            | ❌         | 可选               |
| 获取项目信息                        | ✅         | 需要认证           |
| 上传日报                            | ✅         | 需要认证           |
| 获取用户信息                        | ✅         | 需要认证           |
| 所有业务接口                        | ✅         | 默认需要认证       |

## 🎨 统一的错误处理

### 错误码映射

```python
def _extract_error_message(self, response: requests.Response) -> str:
    """提取错误信息"""
    try:
        result = response.json()
        return result.get('msg', result.get('message', ''))
    except:
        if response.status_code == 401:
            return '未授权或登录已过期'
        elif response.status_code == 403:
            return '没有权限'
        elif response.status_code == 404:
            return '接口不存在'
        elif response.status_code == 500:
            return '服务器内部错误'
        return f'HTTP {response.status_code}'
```

### 统一响应解析

```python
def parse_response(self, response: requests.Response, expected_code: int = 1) -> Dict:
    """
    解析响应，统一处理错误

    :param response: 响应对象
    :param expected_code: 期望的业务状态码（默认1表示成功）
    :return: 响应数据
    """
    # 检查HTTP状态码
    if response.status_code != 200:
        error_msg = self._extract_error_message(response)
        raise Exception(f'HTTP {response.status_code}: {error_msg}')

    # 解析JSON
    try:
        result = response.json()
    except ValueError as e:
        raise ValueError(f'响应格式错误：{str(e)}')

    # 检查业务状态码
    if result.get('code') != expected_code:
        error_msg = result.get('msg', result.get('message', '请求失败'))
        raise Exception(error_msg)

    return result.get('data', {})
```

## 💡 使用示例

### 示例 1：创建新服务

```python
from services.base_service import BaseService

class UserService(BaseService):
    """用户服务"""

    def get_user_profile(self, user_id: int):
        """获取用户信息（自动添加token）"""
        response = self.get(f'/api/v1/users/{user_id}')
        return self.parse_response(response)

    def update_user_profile(self, user_id: int, data: dict):
        """更新用户信息（自动添加token）"""
        response = self.put(f'/api/v1/users/{user_id}', json_data=data)
        return self.parse_response(response)

    def delete_user(self, user_id: int):
        """删除用户（自动添加token）"""
        response = self.delete(f'/api/v1/users/{user_id}')
        return self.parse_response(response)
```

### 示例 2：在 UI 中使用

```python
# 初始化服务
user_service = UserService(api_base_url, token)

# 调用接口（自动添加token）
try:
    user_data = user_service.get_user_profile(123)
    print(f"用户名: {user_data['username']}")
except Exception as e:
    QMessageBox.warning(self, "错误", f"获取用户信息失败: {str(e)}")
```

## 🚀 优势总结

### 1. 代码复用

- ✅ 避免重复的 HTTP 请求代码
- ✅ 统一的错误处理逻辑
- ✅ 减少代码量 50%+

### 2. 易于维护

- ✅ Token 管理集中化
- ✅ 修改一处，全局生效
- ✅ 新增接口只需几行代码

### 3. 安全性

- ✅ 自动添加 token
- ✅ 不会忘记添加 token
- ✅ 安全的日志记录

### 4. 一致性

- ✅ 所有接口使用相同的 token 字段
- ✅ 统一的错误码处理
- ✅ 标准化的响应格式

## 📝 迁移指南

### 迁移现有服务

**步骤 1**：继承 BaseService

```python
# 修改前
class MyService:
    def __init__(self, api_base_url: str, token: str):
        self.api_base_url = api_base_url
        self.token = token

# 修改后
from services.base_service import BaseService

class MyService(BaseService):
    def __init__(self, api_base_url: str, token: str):
        super().__init__(api_base_url, token)
```

**步骤 2**：使用基础方法

```python
# 修改前
url = f"{self.api_base_url}/api/v1/endpoint"
headers = {"token": self.token}
response = requests.get(url, headers=headers)

# 修改后
response = self.get('/api/v1/endpoint')
data = self.parse_response(response)
```

**步骤 3**：删除冗余代码

- 删除手动添加 token 的代码
- 删除重复的错误处理代码
- 删除 import requests（如果不需要）

## 🧪 测试建议

### 功能测试

1. **Token 自动添加测试**

   - 调用需要 token 的接口
   - 验证请求头包含 token 字段
   - 验证接口调用成功

2. **无 Token 接口测试**

   - 调用登录接口
   - 验证不包含 token 字段
   - 验证登录成功

3. **Token 失效测试**
   - 使用过期的 token
   - 验证返回 401 错误
   - 验证错误提示正确

### 日志测试

1. **安全日志测试**
   - 查看控制台日志
   - 验证 token 被隐藏
   - 验证密码被隐藏

---

**实现日期**: 2025-10-23  
**版本**: v2.3  
**状态**: ✅ 已完成
