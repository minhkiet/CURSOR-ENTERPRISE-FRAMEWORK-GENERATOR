# NestJS Architecture - Kiến Trúc Chi Tiết

## Mục lục
1. [Tổng quan Kiến trúc](#1-tổng-quan-kiến-trúc)
2. [Request Lifecycle](#2-request-lifecycle)
3. [Module Structure](#3-module-structure)
4. [Database Integration](#4-database-integration)
5. [Authentication Architecture](#5-authentication-architecture)

---

## 1. Tổng quan Kiến trúc

### 1.1 NestJS Overview

NestJS là một framework để xây dựng efficient, scalable Node.js server-side applications. Nó sử dụng TypeScript, support strong architecture patterns, và kết hợp elements của OOP, FP, và FRP.

Core building blocks:
- **Modules**: Organizational units
- **Controllers**: Route handling
- **Providers/Services**: Business logic
- **Pipes**: Data transformation/validation
- **Guards**: Authorization
- **Interceptors**: Cross-cutting concerns
- **Filters**: Error handling

### 1.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                       NESTJS APPLICATION                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    REQUEST                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    MIDDLEWARE                                 │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │ Logger | CORS | BodyParser | Helmet | RateLimit      │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      GUARDS                                    │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │ AuthGuard | RolesGuard | ThrottlerGuard              │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      INTERCEPTORS                             │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │ Logging | Transform | Cache | Timing                 │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      PIPES                                     │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │ ValidationPipe | ParseIntPipe | DefaultValuePipe    │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    CONTROLLER                                 │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │ @Get @Post @Put @Delete @Patch                       │ │   │
│  │  │ Handler Methods                                       │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    PROVIDER / SERVICE                         │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │ Business Logic | Database Access | External APIs    │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Request Lifecycle

### 2.1 Detailed Lifecycle

```
┌─────────────────────────────────────────────────────────────────────┐
│                      REQUEST LIFECYCLE                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. Incoming Request                                               │
│     │                                                               │
│     ▼                                                               │
│  2. Middleware (Global)                                           │
│     │                                                               │
│     ├── LoggerMiddleware                                           │
│     ├── CorsMiddleware                                              │
│     ├── BodyParserMiddleware                                        │
│     └── RateLimitMiddleware                                         │
│     │                                                               │
│     ▼                                                               │
│  3. Module Middleware                                              │
│     │                                                               │
│     ▼                                                               │
│  4. Guards (Global + Route)                                      │
│     │                                                               │
│     ├── AuthGuard                                                 │
│     ├── RolesGuard                                                 │
│     └── Check if request should proceed                            │
│     │                                                               │
│     ▼                                                               │
│  5. Interceptors (Pre-Handler)                                    │
│     │                                                               │
│     ├── LoggingInterceptor                                          │
│     └── TransformInterceptor                                        │
│     │                                                               │
│     ▼                                                               │
│  6. Pipes (Pre-Handler)                                           │
│     │                                                               │
│     ├── ValidationPipe                                             │
│     └── ParseIntPipe                                               │
│     │                                                               │
│     ▼                                                               │
│  7. Controller Handler                                            │
│     │                                                               │
│     ├── Execute handler                                            │
│     └── Return response                                            │
│     │                                                               │
│     ▼                                                               │
│  8. Interceptors (Post-Handler)                                   │
│     │                                                               │
│     ├── Transform response                                         │
│     └── Cache response                                             │
│     │                                                               │
│     ▼                                                               │
│  9. Exception Filters (if error)                                  │
│     │                                                               │
│     ├── HttpExceptionFilter                                         │
│     └── AllExceptionFilter                                         │
│     │                                                               │
│     ▼                                                               │
│  10. Response                                                     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Module Structure

### 3.1 Feature Module Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                       MODULE ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     APP MODULE                                │   │
│  │  (Root Module)                                              │   │
│  │                                                             │   │
│  │  imports: [                                                 │   │
│  │    UsersModule,                                             │   │
│  │    AuthModule,                                              │   │
│  │    ProductsModule,                                          │   │
│  │    TypeOrmModule.forRoot(...)                              │   │
│  │  ]                                                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│          ┌───────────────────┼───────────────────┐                │
│          │                   │                   │                  │
│          ▼                   ▼                   ▼                   │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │   Users       │  │    Auth      │  │  Products    │          │
│  │   Module      │  │    Module     │  │   Module     │          │
│  │               │  │               │  │               │          │
│  │  Controllers: │  │  Controllers: │  │  Controllers: │          │
│  │  - UsersCtrl │  │  - AuthCtrl  │  │  - Products  │          │
│  │               │  │               │  │               │          │
│  │  Services:   │  │  Services:   │  │  Services:   │          │
│  │  - UsersSvc   │  │  - AuthSvc   │  │  - ProductsSvc│          │
│  │               │  │               │  │               │          │
│  │  Entities:   │  │  Guards:    │  │  Entities:   │          │
│  │  - User      │  │  - JwtGuard │  │  - Product   │          │
│  │               │  │               │  │               │          │
│  │  DTOs:       │  │  Strategies: │  │  DTOs:       │          │
│  │  - CreateDto │  │  - JwtStrat │  │  - CreateDto │          │
│  │  - UpdateDto │  │               │  │  - UpdateDto │          │
│  │               │  │  Decorators:│  │               │          │
│  │  Repositories │  │  - CurrentUser│  │  Repositories │          │
│  └───────────────┘  └───────────────┘  └───────────────┘          │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.2 Shared Module Pattern

```
┌─────────────────────────────────────────────────────────────────────┐
│                       SHARED MODULE                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    SHARED MODULE                              │   │
│  │                                                             │   │
│  │  providers: [                                               │   │
│  │    LoggerService,                                           │   │
│  │    ValidationService,                                       │   │
│  │    ConfigService,                                           │   │
│  │  ]                                                          │   │
│  │                                                             │   │
│  │  exports: [                                                 │   │
│  │    LoggerService,                                           │   │
│  │    ValidationService,                                       │   │
│  │    ConfigService,                                           │   │
│  │  ]                                                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │   Users       │  │    Auth      │  │  Products    │          │
│  │   Module      │  │    Module     │  │   Module     │          │
│  │               │  │               │  │               │          │
│  │  imports: [   │  │  imports: [   │  │  imports: [   │          │
│  │    SharedModule│  │   SharedModule│  │   SharedModule│          │
│  │  ]            │  │  ]            │  │  ]            │          │
│  └───────────────┘  └───────────────┘  └───────────────┘          │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 4. Database Integration

### 4.1 TypeORM Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     TYPEORM INTEGRATION                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    TYPEORM MODULE                            │   │
│  │                                                             │   │
│  │  TypeOrmModule.forRoot({                                  │   │
│  │    type: 'postgres',                                      │   │
│  │    host: 'localhost',                                     │   │
│  │    port: 5432,                                            │   │
│  │    username: 'user',                                      │   │
│  │    password: 'password',                                   │   │
│  │    database: 'mydb',                                      │   │
│  │    entities: [__dirname + '/**/*.entity{.ts,.js}'],     │   │
│  │    synchronize: false,                                     │   │
│  │    logging: true,                                         │   │
│  │  })                                                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    ENTITY EXAMPLE                             │   │
│  │                                                             │   │
│  │  @Entity('users')                                          │   │
│  │  export class User {                                       │   │
│  │    @PrimaryGeneratedColumn()                                │   │
│  │    id: number;                                              │   │
│  │                                                             │   │
│  │    @Column()                                                │   │
│  │    name: string;                                           │   │
│  │                                                             │   │
│  │    @Column({ unique: true })                               │   │
│  │    email: string;                                            │   │
│  │                                                             │   │
│  │    @Column({ default: true })                              │   │
│  │    isActive: boolean;                                       │   │
│  │                                                             │   │
│  │    @CreateDateColumn()                                      │   │
│  │    createdAt: Date;                                         │   │
│  │                                                             │   │
│  │    @OneToMany(() => Post, post => post.author)              │   │
│  │    posts: Post[];                                           │   │
│  │  }                                                          │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 4.2 Repository Pattern

```typescript
// users.repository.ts
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './user.entity';

@Injectable()
export class UsersRepository {
  constructor(
    @InjectRepository(User)
    private repository: Repository<User>,
  ) {}
  
  async findAll(): Promise<User[]> {
    return this.repository.find();
  }
  
  async findOne(id: number): Promise<User | null> {
    return this.repository.findOne({ where: { id } });
  }
  
  async findByEmail(email: string): Promise<User | null> {
    return this.repository.findOne({ where: { email } });
  }
  
  async create(userData: Partial<User>): Promise<User> {
    const user = this.repository.create(userData);
    return this.repository.save(user);
  }
  
  async update(id: number, userData: Partial<User>): Promise<void> {
    await this.repository.update(id, userData);
  }
  
  async delete(id: number): Promise<void> {
    await this.repository.delete(id);
  }
}
```

---

## 5. Authentication Architecture

### 5.1 JWT Auth Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    JWT AUTHENTICATION FLOW                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐       │
│  │ Client  │───►│  Auth  │───►│  JWT   │───►│ Response│       │
│  │         │    │ Controller│    │ Service│    │ (Token) │       │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘       │
│                       │              │                               │
│                       │              ▼                               │
│                       │    ┌─────────────────┐                      │
│                       │    │  JWT Signature  │                      │
│                       │    │  - User ID     │                      │
│                       │    │  - Email       │                      │
│                       │    │  - Roles       │                      │
│                       │    │  - Expiry     │                      │
│                       │    └─────────────────┘                      │
│                       │                                             │
│                       ▼                                             │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                  AUTHENTICATED REQUEST                        │  │
│  │                                                              │  │
│  │  Headers: {                                                  │  │
│  │    Authorization: Bearer <jwt_token>                          │  │
│  │  }                                                           │  │
│  │       │                                                      │  │
│  │       ▼                                                      │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │                    JWT GUARD                           │   │  │
│  │  │  1. Extract token from header                        │   │  │
│  │  │  2. Verify token signature                           │   │  │
│  │  │  3. Check expiry                                    │   │  │
│  │  │  4. Attach user to request                          │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  │                      │                                      │  │
│  │                      ▼                                      │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │              CONTROLLER HANDLER                       │   │  │
│  │  │  @Get('profile')                                     │   │  │
│  │  │  getProfile(@CurrentUser() user: User) {           │   │  │
│  │  │    return user;                                     │   │  │
│  │  │  }                                                   │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.2 Auth Module Implementation

```typescript
// auth.module.ts
@Module({
  imports: [
    UsersModule,
    JwtModule.registerAsync({
      useFactory: (configService: ConfigService) => ({
        secret: configService.get('JWT_SECRET'),
        signOptions: { expiresIn: '1h' },
      }),
      inject: [ConfigService],
    }),
  ],
  controllers: [AuthController],
  providers: [AuthService, JwtStrategy, JwtAuthGuard],
  exports: [AuthService, JwtAuthGuard],
})
export class AuthModule {}

// auth.service.ts
@Injectable()
export class AuthService {
  constructor(
    private usersService: UsersService,
    private jwtService: JwtService,
  ) {}
  
  async validateUser(email: string, pass: string): Promise<User | null> {
    const user = await this.usersService.findByEmail(email);
    if (user && await bcrypt.compare(pass, user.password)) {
      return user;
    }
    return null;
  }
  
  async login(user: User) {
    const payload = { sub: user.id, email: user.email, roles: user.roles };
    return {
      access_token: this.jwtService.sign(payload),
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
      },
    };
  }
}
```

---

## Liên kết liên quan
- [NestJS Glossary](./glossary.md)
- [NestJS Best Practices](./best-practice.md)
- [NestJS Anti-Patterns](./anti-pattern.md)
- [NestJS Checklist](./checklist.md)
- [NestJS FAQ](./faq.md)
- [NestJS Decision Tree](./decision-tree.md)
