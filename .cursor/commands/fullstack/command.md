---
description: Fullstack Web Development Command - Xây dựng, chỉnh sửa, debug web app end-to-end với ASP.NET Core Web API + React TypeScript
trigger: fullstack, /fullstack, fullstack web, dotnet react, aspnet react
category: Development
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Command: /fullstack

## Mục tiêu
Điều phối quy trình phát triển Fullstack Web hoàn chỉnh (End-to-End):
- **Backend:** ASP.NET Core Web API (Controllers, Services, DTOs, EF Core/Dapper)
- **Frontend:** React + TypeScript + TSX (Pages, Components, API Services, State)
- **Database:** Truy vấn, migrations, tối ưu hóa
- **Auth:** JWT token flow, Protected Routes, Role-based Access Control

## Cú pháp Lệnh (Invocation)

```text
/fullstack feature <feature_name>       # Phát triển tính năng mới từ Backend đến Frontend
/fullstack fix <issue_description>      # Debug và sửa lỗi theo quy trình Root Cause Analysis (RCA)
/fullstack api <endpoint_spec>          # Tạo Controller + DTOs + Frontend API Service
/fullstack audit                        # Kiểm tra tính toàn vẹn của kết nối fullstack & contracts
/fullstack verify                       # Chạy check-list 17 điểm trước khi bàn giao
```

## Luồng Thực thi (Execution Pipeline)

```text
1. [Analysis]       Khảo sát cấu trúc dự án (Backend, Frontend, DB, Auth, Dependencies)
2. [Database]       Cập nhật Entities, migrations (nếu cần)
3. [Backend API]    Tạo DTOs, Service, Controller với [Authorize] & validation
4. [Frontend API]   Đồng bộ TypeScript types & tạo Service trong src/services/
5. [Frontend UI]    Tạo/Cập nhật Components, Forms, Hooks, State
6. [Security]       Kiểm tra CORS, SQL injection, XSS, JWT header, secret leaks
7. [Verification]   Kiểm tra 17 tiêu chí: compile, status code, responsive, error states
```

## Ví dụ Sử dụng

### 1. Thêm tính năng quản lý sản phẩm
```text
/fullstack feature ProductManagement
- Yêu cầu: CRUD sản phẩm, phân trang, lọc theo danh mục
- Backend: ProductsController, ProductService, DTOs
- Frontend: ProductListPage, ProductModalForm, productService.ts
```

### 2. Sửa lỗi gọi API 401 / Token Refresh
```text
/fullstack fix "Token hết hạn gây lỗi 401 lặp vô tận trên frontend"
```
