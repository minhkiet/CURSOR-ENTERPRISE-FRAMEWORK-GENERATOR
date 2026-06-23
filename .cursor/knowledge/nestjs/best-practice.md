# NestJS Best Practices - Các Thực Hành Tốt Nhất

## Mục lục
1. [Module Organization](#1-module-organization)
2. [Controller Best Practices](#2-controller-best-practices)
3. [Service Best Practices](#3-service-best-practices)
4. [Database Best Practices](#4-database-best-practices)
5. [Security Best Practices](#5-security-best-practices)
6. [Testing Best Practices](#6-testing-best-practices)

---

## 1. Module Organization

### 1.1 Feature-Based Modules

**Mô tả**: Tổ chức modules theo features/domain thay vì technical layers.

**Ví dụ**:
```
src/
├── modules/
│   ├── auth/
│   │   ├── auth.module.ts
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── guards/
│   │   │   └── jwt-auth.guard.ts
│   │   ├── strategies/
│   │   │   └── jwt.strategy.ts
│   │   └── decorators/
│   │       └── current-user.decorator.ts
│   │
│   ├── users/
│   │   ├── users.module.ts
│   │   ├── users.controller.ts
│   │   ├── users.service.ts
│   │   ├── entities/
│   │   │   └── user.entity.ts
│   │   └── dto/
│   │       ├── create-user.dto.ts
│   │       └── update-user.dto.ts
│   │
│   ├── products/
│   │   └── ...
│   │
│   └── orders/
│       └── ...
│
├── shared/
│   ├── decorators/
│   ├── filters/
│   ├── guards/
│   ├── interceptors/
│   ├── pipes/
│   └── utils/
│
├── app.module.ts
└── main.ts
```

**Khi nào áp dụng**: Mọi NestJS applications.

### 1.2 Create Shared Module

**Mô tả**: Extract common functionality vào shared module.

**Ví dụ**:
```typescript
// shared/shared.module.ts
@Module({
  providers: [
    Logger,
    ConfigService,
    {
      provide: 'MAILER',
      useFactory: () => nodemailer.createTransport({/* ... */}),
    },
  ],
  exports: [Logger, ConfigService, 'MAILER'],
})
export class SharedModule {}

// Usage in feature module
@Module({
  imports: [SharedModule],
})
export class UsersModule {}
```

**Khi nào áp dụng**: Common services được reuse across modules.

---

## 2. Controller Best Practices

### 2.1 Keep Controllers Thin

**Mô tả**: Controllers chỉ nên handle HTTP concerns và delegate logic đến services.

**Ví dụ**:
```typescript
// ❌ BAD: Fat controller
@Controller('users')
export class UsersController {
  constructor(private readonly usersRepository: UsersRepository) {}
  
  @Get()
  async findAll() {
    // Too much logic in controller
    const users = await this.usersRepository.find({
      where: { isActive: true },
      select: ['id', 'name', 'email'],
      order: { createdAt: 'DESC' },
    });
    
    const transformed = users.map(u => ({
      ...u,
      createdAt: u.createdAt.toISOString(),
    }));
    
    return { data: transformed, count: transformed.length };
  }
}

// ✅ GOOD: Thin controller
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}
  
  @Get()
  async findAll() {
    return this.usersService.findAllUsers();
  }
}
```

**Khi nào áp dụng**: Mọi controllers.

### 2.2 Use DTOs for Input Validation

**Mô tả**: Define DTOs với class-validator decorators để automatic validation.

**Ví dụ**:
```typescript
// create-user.dto.ts
import { IsEmail, IsString, MinLength, IsOptional, IsEnum } from 'class-validator';
import { UserRole } from '../entities/user.entity';

export class CreateUserDto {
  @IsString()
  @MinLength(2)
  name: string;
  
  @IsEmail()
  email: string;
  
  @IsString()
  @MinLength(8)
  password: string;
  
  @IsOptional()
  @IsEnum(UserRole)
  role?: UserRole;
}

// update-user.dto.ts
import { PartialType, PickType } from '@nestjs/mapped-types';

export class UpdateUserDto extends PartialType(CreateUserDto) {}

// Using in controller
@Post()
async create(@Body() createUserDto: CreateUserDto) {
  return this.usersService.create(createUserDto);
}
```

**Khi nào áp dụng**: Mọi POST/PUT/PATCH endpoints.

---

## 3. Service Best Practices

### 3.1 Use Repository Pattern

**Mô tả**: Tách data access logic vào repositories riêng biệt.

**Ví dụ**:
```typescript
// users.repository.ts
@Injectable()
export class UsersRepository {
  constructor(
    @InjectRepository(User)
    private repository: Repository<User>,
  ) {}
  
  async findAll(options?: FindManyOptions<User>): Promise<User[]> {
    return this.repository.find(options);
  }
  
  async findOne(id: number): Promise<User | null> {
    return this.repository.findOne({ where: { id } });
  }
  
  async findByEmail(email: string): Promise<User | null> {
    return this.repository.findOne({ where: { email } });
  }
  
  async create(data: CreateUserDto): Promise<User> {
    const user = this.repository.create(data);
    return this.repository.save(user);
  }
}

// users.service.ts
@Injectable()
export class UsersService {
  constructor(private readonly usersRepository: UsersRepository) {}
  
  async findAllUsers() {
    return this.usersRepository.findAll({
      where: { isActive: true },
      order: { createdAt: 'DESC' },
    });
  }
}
```

**Khi nào áp dụng**: Applications với complex data access logic.

### 3.2 Handle Errors Gracefully

**Mô tả**: Throw appropriate exceptions và handle errors properly.

**Ví dụ**:
```typescript
@Injectable()
export class UsersService {
  async findOneOrThrow(id: number): Promise<User> {
    const user = await this.usersRepository.findOne(id);
    
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    
    return user;
  }
  
  async create(createUserDto: CreateUserDto): Promise<User> {
    const existingUser = await this.usersRepository.findByEmail(createUserDto.email);
    
    if (existingUser) {
      throw new ConflictException('User with this email already exists');
    }
    
    try {
      return await this.usersRepository.create(createUserDto);
    } catch (error) {
      throw new InternalServerErrorException('Failed to create user');
    }
  }
}
```

**Khi nào áp dụng**: Mọi service methods.

---

## 4. Database Best Practices

### 4.1 Use Transactions

**Mô tả**: Wrap multiple operations trong transaction để đảm bảo data consistency.

**Ví dụ**:
```typescript
@Injectable()
export class OrdersService {
  constructor(
    private dataSource: DataSource,
    private ordersRepository: OrdersRepository,
    private inventoryService: InventoryService,
  ) {}
  
  async createOrder(createOrderDto: CreateOrderDto): Promise<Order> {
    const queryRunner = this.dataSource.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();
    
    try {
      // Create order
      const order = await queryRunner.manager.save(Order, {
        userId: createOrderDto.userId,
        items: createOrderDto.items,
        total: 0,
      });
      
      // Update inventory
      for (const item of createOrderDto.items) {
        await this.inventoryService.decrementStock(
          queryRunner.manager,
          item.productId,
          item.quantity,
        );
      }
      
      // Calculate total
      order.total = await this.calculateTotal(createOrderDto.items);
      
      await queryRunner.commitTransaction();
      return order;
    } catch (error) {
      await queryRunner.rollbackTransaction();
      throw error;
    } finally {
      await queryRunner.release();
    }
  }
}
```

**Khi nào áp dụng**: Multiple related database operations.

### 4.2 Use Query Builder for Complex Queries

**Mô tả**: Sử dụng Query Builder cho complex queries thay vì raw SQL.

**Ví dụ**:
```typescript
async searchUsers(query: UserSearchQuery): Promise<User[]> {
  return this.dataSource
    .getRepository(User)
    .createQueryBuilder('user')
    .leftJoinAndSelect('user.posts', 'post')
    .leftJoinAndSelect('user.profile', 'profile')
    .where('user.isActive = :isActive', { isActive: true })
    .andWhere(query.search ? 'user.name ILIKE :search' : '1=1', {
      search: `%${query.search}%`,
    })
    .andWhere(query.role ? 'user.role = :role' : '1=1', {
      role: query.role,
    })
    .orderBy('user.createdAt', 'DESC')
    .skip((query.page - 1) * query.limit)
    .take(query.limit)
    .getMany();
}
```

**Khi nào áp dụng**: Complex queries với multiple conditions.

---

## 5. Security Best Practices

### 5.1 Use Guards for Authorization

**Mô tả**: Implement guards để protect routes với proper authorization.

**Ví dụ**:
```typescript
// roles.guard.ts
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}
  
  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>(
      'roles',
      context.getHandler(),
    );
    
    if (!requiredRoles) {
      return true;
    }
    
    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some(role => user.roles?.includes(role));
  }
}

// Usage
@Get('admin')
@UseGuards(JwtAuthGuard, RolesGuard)
@SetMetadata('roles', ['admin'])
async adminOnly() {
  return 'Admin content';
}

// Custom decorator
export const Roles = (...roles: string[]) => SetMetadata('roles', roles);

@Get('admin')
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('admin')
async adminOnly() {}
```

**Khi nào áp dụng**: Protected routes.

### 5.2 Validate Input with ValidationPipe

**Mô tả**: Configure global ValidationPipe để automatic DTO validation.

**Ví dụ**:
```typescript
// main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    transform: true,
    forbidNonWhitelisted: true,
    transformOptions: {
      enableImplicitConversion: true,
    },
    validatorOptions: {
      whitelist: true,
      forbidNonWhitelisted: true,
    },
  }));
  
  await app.listen(3000);
}
```

**Khi nào áp dụng**: Mọi input validation.

---

## 6. Testing Best Practices

### 6.1 Unit Test Services

**Mô tả**: Test services với mocks cho dependencies.

**Ví dụ**:
```typescript
describe('UsersService', () => {
  let service: UsersService;
  let repository: jest.Mocked<UsersRepository>;
  
  beforeEach(async () => {
    const mockRepository = {
      findOne: jest.fn(),
      find: jest.fn(),
      create: jest.fn(),
      save: jest.fn(),
    };
    
    const module = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: UsersRepository,
          useValue: mockRepository,
        },
      ],
    }).compile();
    
    service = module.get<UsersService>(UsersService);
    repository = module.get(UsersRepository);
  });
  
  it('should find a user by id', async () => {
    const user = { id: 1, name: 'John', email: 'john@example.com' };
    repository.findOne.mockResolvedValue(user);
    
    const result = await service.findOne(1);
    
    expect(result).toEqual(user);
    expect(repository.findOne).toHaveBeenCalledWith(1);
  });
  
  it('should throw NotFoundException when user not found', async () => {
    repository.findOne.mockResolvedValue(null);
    
    await expect(service.findOne(999)).rejects.toThrow(NotFoundException);
  });
});
```

**Khi nào áp dụng**: Mọi services.

### 6.2 Integration Test with TestingModule

**Mô tả**: Test controllers với full NestJS module.

**Ví dụ**:
```typescript
describe('UsersController (Integration)', () => {
  let controller: UsersController;
  let service: jest.Mocked<UsersService>;
  
  beforeEach(async () => {
    const mockService = {
      findAll: jest.fn(),
      findOne: jest.fn(),
      create: jest.fn(),
    };
    
    const module = await Test.createTestingModule({
      controllers: [UsersController],
      providers: [
        {
          provide: UsersService,
          useValue: mockService,
        },
      ],
    }).compile();
    
    controller = module.get<UsersController>(UsersController);
    service = module.get(UsersService);
  });
  
  describe('GET /users', () => {
    it('should return an array of users', async () => {
      const users = [{ id: 1, name: 'John' }];
      service.findAll.mockResolvedValue(users);
      
      const result = await controller.findAll();
      
      expect(result).toEqual(users);
      expect(service.findAll).toHaveBeenCalled();
    });
  });
});
```

**Khi nào áp dụng**: Controller testing.

---

## Liên kết liên quan
- [NestJS Glossary](./glossary.md)
- [NestJS Architecture](./architecture.md)
- [NestJS Anti-Patterns](./anti-pattern.md)
- [NestJS Checklist](./checklist.md)
- [NestJS FAQ](./faq.md)
- [NestJS Decision Tree](./decision-tree.md)
