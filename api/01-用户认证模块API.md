# 用户认证模块 API 接口文档

## 模块概述

用户认证模块负责处理用户登录、退出、密码修改、Token刷新等认证相关功能。

## 接口列表

### 1.1 用户登录
**接口地址：** `POST /api/v1/auth/login`

**功能描述：** 用户使用用户名和密码进行系统登录

**请求参数：**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**参数说明：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**响应示例：**
```json
{
  "code": 1,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 7200,
    "user": {
      "id": "1",
      "username": "admin",
      "name": "管理员",
      "email": "admin@example.com",
      "role": "ADMIN",
      "lastLoginTime": "2025-09-26T10:30:00Z"
    }
  }
}
```

**错误响应：**
```json
{
  "code": 401,
  "message": "用户名或密码错误",
  "data": null
}
```

---

### 1.2 刷新Token
**接口地址：** `POST /api/v1/auth/refresh`

**功能描述：** 使用刷新令牌获取新的访问令牌

**请求参数：**
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**参数说明：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| refreshToken | string | 是 | 刷新令牌 |

**响应示例：**
```json
{
  "code": 1,
  "message": "刷新成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 7200
  }
}
```

---

### 1.3 修改密码
**接口地址：** `PUT /api/v1/auth/password`

**功能描述：** 用户修改登录密码

**请求头：**
```
Content-Type: application/json
accept: application/json
token: {token}
```

**请求参数：**
```json
{
  "oldPassword": "oldPassword123",
  "newPassword": "newPassword123"
}
```

**参数说明：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| oldPassword | string | 是 | 原密码 |
| newPassword | string | 是 | 新密码 |

**响应示例：**
```json
{
  "code": 1,
  "message": "密码修改成功",
  "data": null
}
```

**错误响应：**
```json
{
  "code": 400,
  "message": "原密码错误",
  "data": null
}
```

---

### 1.4 用户登出
**接口地址：** `POST /api/v1/auth/logout`

**功能描述：** 用户退出登录，使Token失效

**请求头：**
```
Content-Type: application/json
accept: application/json
token: {token}
```

**响应示例：**
```json
{
  "code": 1,
  "message": "登出成功",
  "data": null
}
```

---

### 1.5 获取当前用户信息
**接口地址：** `GET /api/v1/auth/me`

**功能描述：** 获取当前登录用户的详细信息

**请求头：**
```
Content-Type: application/json
accept: application/json
token: {token}
```

**响应示例：**
```json
{
  "code": 1,
  "message": "查询成功",
  "data": {
    "id": "1",
    "username": "admin",
    "name": "管理员",
    "email": "admin@example.com",
    "role": "ADMIN",
    "permissions": ["project:read", "project:write", "record:read", "record:write"],
    "lastLoginTime": "2025-09-26T10:30:00Z",
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-09-26T10:30:00Z"
  }
}
```

## 数据模型

### User 用户模型
```json
{
  "id": "string",
  "username": "string",
  "name": "string", 
  "email": "string",
  "role": "ADMIN|USER|OPERATOR",
  "permissions": ["string"],
  "lastLoginTime": "string",
  "createdAt": "string",
  "updatedAt": "string"
}
```

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 401001 | 未提供认证令牌 |
| 401002 | 认证令牌无效 |
| 401003 | 认证令牌已过期 |
| 401004 | 用户名或密码错误 |
| 401005 | 原密码错误 |
| 401006 | 刷新令牌无效 |
| 401007 | 刷新令牌已过期 |

## 使用说明

1. **Token管理**：访问令牌有效期为2小时，刷新令牌有效期为7天
2. **权限控制**：不同角色用户具有不同的API访问权限
3. **安全建议**：建议在Token即将过期前主动刷新，避免用户操作中断
