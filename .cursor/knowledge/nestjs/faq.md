# NestJS FAQ - Câu Hỏi Thường Gặp

## Mục lục
1. [General](#1-general)
2. [Modules](#2-modules)
3. [Controllers](#3-controllers)
4. [Database](#4-database)
5. [Authentication](#5-authentication)

---

## 1. General

### Q1: Làm thế nào để configure NestJS application?

**A:**

```typescript
// main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // Global prefix
  app.setGlobalPrefix('api/v1');
  
  // Global validation pipe
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    transform: true,
    forbidNonWhitelisted: true,
  }));
  
  // Global exception filter
  app.useGlobalFilters(new HttpExceptionFilter());
  
  // CORS
  app.enableCors();
  
  // Validation
  const { PORT } = process.env;
  await app.listen(PORT || 3000);
}

bootstrap();
```

---

### Q2: Sự khác nhau giữa @Injectable() và @Inject()?

**A:**

| Decorator | Use Case |
|-----------|----------|
| `@Injectable()` | Marks class as injectable (automatic DI) |
| `@Inject()` | Manual injection for tokens |

```typescript
// Automatic (recommended)
@Injectable()
export class UsersService {
  constructor(private usersRepository: UsersRepository) {}
}

// Manual (for tokens)
@Injectable()
export class ConfigService {
  constructor(
    @Inject('CONFIG_TOKEN') private config: Config,
  ) {}
}
```

---

### Q3: Làm thế nào để handle errors?

**A:**

```typescript
// Built-in exceptions
throw new NotFoundException('User not found');
throw new BadRequestException('Invalid input');
throw new UnauthorizedException('Not authenticated');
throw new ForbiddenException('Access denied');
throw new ConflictException('Email already exists');

// Custom exception filter
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    
    const status = exception instanceof HttpException
      ? exception.getStatus()
      : 500;
      
    response.status(status).json({
      statusCode: status,
      message: exception.message,
      timestamp: new Date().toISOString(),
    });
  }
}

// Apply globally
app.useGlobalFilters(new AllExceptionsFilter());
```

---

## 2. Modules

### Q4: Làm thế nào để share services giữa modules?

**A:**

```typescript
// shared/shared.module.ts
@Module({
  providers: [LoggerService, ConfigService],
  exports: [LoggerService, ConfigService],
})
export class SharedModule {}

// users.module.ts
@Module({
  imports: [SharedModule],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

---

### Q5: Circular dependency thì xử lý thế nào?

**A:**

**Option 1: Forward Reference**
```typescript
// module-a.module.ts
@Module({
  imports: [forwardRef(() => ModuleB)],
})
export class ModuleA {}

// module-b.module.ts
@Module({
  imports: [forwardRef(() => ModuleA)],
})
export class ModuleB {}
```

**Option 2: Shared Module**
```typescript
// Extract shared to common module
@Module({
  exports: [SharedService],
})
export class SharedModule {}
```

---

## 3. Controllers

### Q6: Làm thế nào để validate query parameters?

**A:**

```typescript
// Optional with default
@Get()
async findAll(
  @Query('page', new DefaultValuePipe(1), ParseIntPipe) page: number,
  @Query('limit', new DefaultValuePipe(10), ParseIntPipe) limit: number,
) {
  return this.usersService.findAll({ page, limit });
}

// With DTO
class PaginationDto {
  @IsOptional()
  @IsInt()
  @Min(1)
  page?: number = 1;
  
  @IsOptional()
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number = 10;
}

@Get()
async findAll(@Query() pagination: PaginationDto) {
  return this.usersService.findAll(pagination);
}
```

---

### Q7: Làm thế nào để access current user trong controller?

**A:**

```typescript
// Custom decorator
export const CurrentUser = createParamDecorator(
  (data: string | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;
    
    return data ? user?.[data] : user;
  },
);

// Usage
@Get('profile')
async getProfile(@CurrentUser() user: User) {
  return user;
}

@Get('profile/id')
async getProfileId(@CurrentUser('id') userId: number) {
  return { userId };
}
```

---

## 4. Database

### Q8: Làm thế nào để use transactions?

**A:**

```typescript
// Option 1: QueryRunner
async createWithTransaction(data: CreateDto) {
  const queryRunner = this.dataSource.createQueryRunner();
  await queryRunner.connect();
  await queryRunner.startTransaction();
  
  try {
    const entity = await queryRunner.manager.save(Entity, data);
    await queryRunner.commitTransaction();
    return entity;
  } catch (error) {
    await queryRunner.rollbackTransaction();
    throw error;
  } finally {
    await queryRunner.release();
  }
}

// Option 2: DataSource.transaction
async createSafe(data: CreateDto) {
  return this.dataSource.transaction(async manager => {
    return manager.save(Entity, data);
  });
}
```

---

### Q9: Soft deletes với TypeORM?

**A:**

```typescript
// Entity with soft delete
@DeleteDateColumn()
deletedAt: Date;

// Query with soft delete
@Injectable()
export class UsersRepository {
  constructor(
    @InjectRepository(User)
    private repository: Repository<User>,
  ) {}
  
  // Find without deleted
  async findAll(): Promise<User[]> {
    return this.repository.find();
  }
  
  // Find with deleted
  async findAllWithDeleted(): Promise<User[]> {
    return this.repository.find({ withDeleted: true });
  }
  
  // Soft delete
  async softDelete(id: number): Promise<void> {
    await this.repository.softDelete(id);
  }
  
  // Restore
  async restore(id: number): Promise<void> {
    await this.repository.restore(id);
  }
}
```

---

## 5. Authentication

### Q10: Làm thế nào để implement JWT authentication?

**A:**

```typescript
// auth.module.ts
@Module({
  imports: [
    UsersModule,
    PassportModule,
    JwtModule.registerAsync({
      useFactory: (config: ConfigService) => ({
        secret: config.get('JWT_SECRET'),
        signOptions: { expiresIn: '1h' },
      }),
      inject: [ConfigService],
    }),
  ],
  providers: [AuthService, JwtStrategy, JwtAuthGuard],
  exports: [AuthService],
})
export class AuthModule {}

// JWT Strategy
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(config: ConfigService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: config.get('JWT_SECRET'),
    });
  }
  
  async validate(payload: any) {
    return { id: payload.sub, email: payload.email };
  }
}

// Usage in controller
@UseGuards(JwtAuthGuard)
@Get('profile')
async getProfile(@Request() req) {
  return req.user;
}
```

---

### Q11: Roles-based authorization?

**A:**

```typescript
// Roles decorator
export const ROLES_KEY = 'roles';
export const Roles = (...roles: string[]) => SetMetadata(ROLES_KEY, roles);

// Roles guard
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(
    private reflector: Reflector,
  ) {}
  
  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<string[]>(
      ROLES_KEY,
      [context.getHandler(), context.getClass()],
    );
    
    if (!requiredRoles) return true;
    
    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some(role => user.roles?.includes(role));
  }
}

// Usage
@Get('admin')
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('admin')
async adminOnly() {
  return 'Admin content';
}
```

---

### Q12: Pagination?

**A:**

```typescript
// Pagination DTO
class PaginationDto {
  @IsOptional()
  @IsInt()
  @Min(1)
  page?: number = 1;
  
  @IsOptional()
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number = 10;
}

// Paginated response
class PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    limit: number;
    totalPages: number;
  };
}

// Service
async findAll(pagination: PaginationDto): Promise<PaginatedResponse<User>> {
  const { page = 1, limit = 10 } = pagination;
  
  const [data, total] = await this.repository.findAndCount({
    skip: (page - 1) * limit,
    take: limit,
    order: { createdAt: 'DESC' },
  });
  
  return {
    data,
    meta: {
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit),
    },
  };
}
```

---

## Liên kết liên quan
- [NestJS Glossary](./glossary.md)
- [NestJS Architecture](./architecture.md)
- [NestJS Best Practices](./best-practice.md)
- [NestJS Anti-Patterns](./anti-pattern.md)
- [NestJS Checklist](./checklist.md)
- [NestJS Decision Tree](./decision-tree.md)
