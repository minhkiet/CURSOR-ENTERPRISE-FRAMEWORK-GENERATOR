# NestJS Anti-Patterns - Các Mẫu Cần Tránh

## Mục lục
1. [Module Anti-Patterns](#1-module-anti-patterns)
2. [Controller Anti-Patterns](#2-controller-anti-patterns)
3. [Service Anti-Patterns](#3-service-anti-patterns)

---

## 1. Module Anti-Patterns

### 1.1 God Module

**Tên Pattern**: God Module

**Mô tả**: Đặt tất cả code vào một module duy nhất thay vì chia thành features.

**Ví dụ (Anti-Pattern)**:
```typescript
// ❌ BAD: Everything in AppModule
@Module({
  imports: [
    TypeOrmModule.forRoot({ /* ... */ }),
    TypeOrmModule.forFeature([User, Product, Order, Category, Payment]),
  ],
  controllers: [
    UsersController,
    ProductsController,
    OrdersController,
    CategoriesController,
    PaymentsController,
  ],
  providers: [
    UsersService,
    ProductsService,
    OrdersService,
    CategoriesService,
    PaymentsService,
    // 50 more services...
  ],
})
export class AppModule {}
```

**Hậu quả**:
- Monolithic, hard to maintain
- Circular dependencies
- Slow application startup
- Difficult to test

**Giải pháp thay thế**:
```typescript
// ✅ GOOD: Feature modules
@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

---

### 1.2 Circular Dependencies

**Tên Pattern**: Circular Dependency

**Mô tả**: Module A phụ thuộc vào Module B, và Module B phụ thuộc vào Module A.

**Ví dụ (Anti-Pattern)**:
```typescript
// ❌ BAD: Circular dependency
// auth.module.ts
@Module({
  imports: [UsersModule], // Needs UsersModule
  providers: [AuthService],
})
export class AuthModule {}

// users.module.ts
@Module({
  imports: [AuthModule], // AuthModule needs this!
  providers: [UsersService],
})
export class UsersModule {}
```

**Hậu quả**:
- Application fails to start
- Hard to debug
- Unpredictable behavior

**Giải pháp thay thế**:
```typescript
// ✅ GOOD: Use shared module
// shared/shared.module.ts
@Module({
  providers: [SharedService],
  exports: [SharedService],
})
export class SharedModule {}

// auth.module.ts
@Module({
  imports: [SharedModule],
})
export class AuthModule {}

// users.module.ts
@Module({
  imports: [SharedModule],
})
export class UsersModule {}
```

---

## 2. Controller Anti-Patterns

### 2.1 Fat Controllers

**Tên Pattern**: Fat Controller

**Mô tả**: Đặt business logic trong controller thay vì services.

**Ví dụ (Anti-Pattern)**:
```typescript
// ❌ BAD: Logic in controller
@Controller('users')
export class UsersController {
  constructor(
    private usersRepository: UsersRepository,
    private mailService: MailService,
  ) {}
  
  @Post()
  async create(@Body() createUserDto: CreateUserDto) {
    // Business logic in controller!
    const existingUser = await this.usersRepository.findOne({
      where: { email: createUserDto.email },
    });
    
    if (existingUser) {
      throw new ConflictException('Email already exists');
    }
    
    const hashedPassword = await bcrypt.hash(createUserDto.password, 10);
    const user = await this.usersRepository.save({
      ...createUserDto,
      password: hashedPassword,
    });
    
    await this.mailService.sendWelcomeEmail(user);
    
    return user;
  }
}
```

**Hậu quả**:
- Hard to test business logic
- Code duplication
- Controller becomes bloated
- Hard to maintain

**Giải pháp thay thế**:
```typescript
// ✅ GOOD: Thin controller, service handles logic
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}
  
  @Post()
  async create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }
}
```

---

### 2.2 Not Using DTOs

**Tên Pattern**: No DTOs

**Mô tả**: Sử dụng any type hoặc Entity direct cho input.

**Ví dụ (Anti-Pattern)**:
```typescript
// ❌ BAD: No DTOs
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}
  
  @Post()
  async create(@Body() body: any) {
    // No type safety, no validation
    return this.usersService.create(body);
  }
}
```

**Hậu quả**:
- No type safety
- No automatic validation
- Potential security issues
- Hard to document

**Giải pháp thay thế**:
```typescript
// ✅ GOOD: DTO with validation
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}
  
  @Post()
  async create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }
}

// create-user.dto.ts
export class CreateUserDto {
  @IsEmail()
  email: string;
  
  @IsString()
  @MinLength(8)
  password: string;
}
```

---

## 3. Service Anti-Patterns

### 3.1 Not Handling Errors

**Tên Pattern**: Silent Errors

**Mô tả**: Catch errors nhưng không throw appropriate exceptions.

**Ví dụ (Anti-Pattern)**:
```typescript
// ❌ BAD: Swallowing errors
@Injectable()
export class UsersService {
  constructor(private usersRepository: UsersRepository) {}
  
  async findOne(id: number) {
    try {
      return await this.usersRepository.findOne(id);
    } catch (error) {
      // Error swallowed!
      return null;
    }
  }
}
```

**Hậu quả**:
- Hard to debug
- Silent failures
- Potential security issues
- User gets no feedback

**Giải pháp thay thế**:
```typescript
// ✅ GOOD: Proper error handling
@Injectable()
export class UsersService {
  async findOne(id: number) {
    const user = await this.usersRepository.findOne(id);
    
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    
    return user;
  }
}
```

---

### 3.2 Synchronous Operations

**Tên Pattern**: Async Ignorance

**Mô tả**: Sử dụng synchronous operations trong async methods.

**Ví dụ (Anti-Pattern)**:
```typescript
// ❌ BAD: Blocking operations
@Injectable()
export class UsersService {
  async create(createUserDto: CreateUserDto) {
    // Synchronous bcrypt - blocks event loop!
    const hashedPassword = bcrypt.hashSync(createUserDto.password, 10);
    
    // Synchronous file read!
    const config = fs.readFileSync('config.json');
    
    return this.usersRepository.save({
      ...createUserDto,
      password: hashedPassword,
    });
  }
}
```

**Hậu quả**:
- Event loop blocked
- Poor performance under load
- Application becomes unresponsive

**Giải pháp thay thế**:
```typescript
// ✅ GOOD: Async operations
@Injectable()
export class UsersService {
  async create(createUserDto: CreateUserDto) {
    // Async bcrypt - doesn't block
    const hashedPassword = await bcrypt.hash(createUserDto.password, 10);
    
    // Async file read
    const config = await fs.promises.readFile('config.json');
    
    return this.usersRepository.save({
      ...createUserDto,
      password: hashedPassword,
    });
  }
}
```

---

### 3.3 Over-Injecting Dependencies

**Tên Pattern**: Too Many Dependencies

**Mô tả**: Injecting quá nhiều dependencies vào một service.

**Ví dụ (Anti-Pattern)**:
```typescript
// ❌ BAD: Too many dependencies
@Injectable()
export class OrderService {
  constructor(
    private usersService: UsersService,
    private productsService: ProductsService,
    private inventoryService: InventoryService,
    private paymentService: PaymentService,
    private emailService: EmailService,
    private smsService: SmsService,
    private loggerService: LoggerService,
    private configService: ConfigService,
    private cacheService: CacheService,
    private storageService: StorageService,
    private notificationService: NotificationService,
    // Too many!
  ) {}
}
```

**Hậu quả**:
- Constructor too long
- Hard to test
- Violates Single Responsibility
- Hard to understand

**Giải pháp thay thế**:
```typescript
// ✅ GOOD: Facade pattern or refactor
@Injectable()
export class OrderService {
  constructor(
    private readonly ordersFacade: OrdersFacade,
    private readonly notificationService: NotificationService,
    private readonly logger: Logger,
  ) {}
}

// Or split into smaller services
@Injectable()
export class PaymentFacade {
  constructor(
    private paymentService: PaymentService,
    private invoiceService: InvoiceService,
    private receiptService: ReceiptService,
  ) {}
}
```

---

## Liên kết liên quan
- [NestJS Glossary](./glossary.md)
- [NestJS Architecture](./architecture.md)
- [NestJS Best Practices](./best-practice.md)
- [NestJS Checklist](./checklist.md)
- [NestJS FAQ](./faq.md)
- [NestJS Decision Tree](./decision-tree.md)
