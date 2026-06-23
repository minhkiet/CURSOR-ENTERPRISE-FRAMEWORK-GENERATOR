# Laravel FAQ - Câu Hỏi Thường Gặp Laravel

## Giới thiệu

Tài liệu này tổng hợp các câu hỏi thường gặp về Laravel.

## Câu Hỏi Cơ Bản

### 1. Laravel là gì?

Laravel là PHP framework cho web application development. Cung cấp elegant syntax, MVC architecture, ORM, routing, authentication, và nhiều features khác.

### 2. Eloquent ORM là gì?

Eloquent là ORM của Laravel cung cấp beautiful ActiveRecord implementation. Mỗi table có một Model tương ứng với methods cho relationships, scopes, etc.

### 3. Laravel Blade là gì?

Blade là templating engine với features cho template inheritance, components, slots. Syntax đơn giản và clean.

### 4. Migrations là gì?

Migrations là version control cho database schema. Tạo và quản lý tables qua code thay vì raw SQL.

## Câu Hỏi Kỹ Thuật

### 5. Làm thế nào để tạo API?

API routes trong routes/api.php. Sử dụng API Resources để transform models. Sanctum hoặc Passport cho authentication.

### 6. Queue hoạt động như thế nào?

Queues defer time-consuming tasks. Create jobs với php artisan make:job. Process với php artisan queue:work.

### 7. Làm thế nào để implement authentication?

Sử dụng Laravel Breeze, Fortify, hoặc Sanctum. Built-in controllers và views cho registration, login, password reset.
