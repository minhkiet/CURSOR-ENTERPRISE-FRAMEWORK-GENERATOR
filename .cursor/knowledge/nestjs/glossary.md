# NestJS Glossary - Thuật Ngữ Chuyên Ngành

## Mục lục
1. [Module](#1-module)
2. [Controller](#2-controller)
3. [Provider/Service](#3-provider-service)
4. [Dependency Injection](#4-dependency-injection)
5. [Guards](#5-guards)
6. [Pipes](#6-pipes)
7. [Decorators](#7-decorators)

---

## Module

**Định nghĩa**: Modules là organizational units nhóm related components lại với nhau. Mỗi NestJS application có ít nhất một root module (AppModule).

**Ví dụ**:
```typescript
// users.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { User } from './user.entity';
import { AuthModule } from '../auth/auth.module';

@Module({
  imports: [
    TypeOrmModule.forFeature([User]),
    AuthModule,
  ],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

---

## Controller

**Định nghĩa**: Controllers xử lý incoming requests và trả về responses. Chúng định nghĩa routes và delegate logic đến services.

**Ví dụ**:
```typescript
// users.controller.ts
import { 
  Controller, 
  Get, 
  Post, 
  Body, 
  Param, 
  ParseIntPipe,
  HttpCode,
  HttpStatus 
} from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { UsersService } from './users.service';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}
  
  @Get()
  async findAll() {
    return this.usersService.findAll();
  }
  
  @Get(':id')
  async findOne(@Param('id', ParseIntPipe) id: number) {
    return this.usersService.findOne(id);
  }
  
  @Post()
  @HttpCode(HttpStatus.CREATED)
  async create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }
  
  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  async remove(@Param('id', ParseIntPipe) id: number) {
    return this.usersService.remove(id);
  }
}
```

---

## Provider/Service

**Định nghĩa**: Providers là classes có thể inject như dependencies. Services là providers phổ biến nhất, chứa business logic.

**Ví dụ**:
```typescript
// users.service.ts
import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './user.entity';
import { CreateUserDto } from './dto/create-user.dto';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>,
  ) {}
  
  async findAll(): Promise<User[]> {
    return this.usersRepository.find();
  }
  
  async findOne(id: number): Promise<User> {
    const user = await this.usersRepository.findOne({ where: { id } });
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    return user;
  }
  
  async create(createUserDto: CreateUserDto): Promise<User> {
    const user = this.usersRepository.create(createUserDto);
    return this.usersRepository.save(user);
  }
  
  async remove(id: number): Promise<void> {
    const result = await this.usersRepository.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
  }
}
```

---

## Dependency Injection

**Định nghĩa**: NestJS sử dụng dependency injection để quản lý dependencies. Container tự động resolve và inject dependencies vào constructors.

**Ví dụ**:
```typescript
// Constructor injection (recommended)
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}
}

// Property injection (less common)
export class UsersService {
  @Inject(UsersRepository)
  private readonly usersRepository: UsersRepository;
}

// Optional injection
constructor(
  @Optional() @Inject(CONFIG_TOKEN) private config: Config,
) {}
```

---

## Guards

**Định nghĩa**: Guards xác định whether a given request sẽ được handle bởi route handler hay không. Chúng implement CanActivate interface.

**Ví dụ**:
```typescript
// auth.guard.ts
import { 
  Injectable, 
  CanActivate, 
  ExecutionContext,
  UnauthorizedException 
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private jwtService: JwtService) {}
  
  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const token = this.extractTokenFromHeader(request);
    
    if (!token) {
      throw new UnauthorizedException('No token provided');
    }
    
    try {
      const payload = await this.jwtService.verifyAsync(token);
      request['user'] = payload;
    } catch {
      throw new UnauthorizedException('Invalid token');
    }
    
    return true;
  }
  
  private extractTokenFromHeader(request: any): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}

// Usage
@Get('profile')
@UseGuards(AuthGuard)
async getProfile(@Request() req) {
  return req.user;
}
```

---

## Pipes

**Định nghĩa**: Pipes thực hiện transformation hoặc validation của data trước khi nó đến route handlers.

**Ví dụ**:
```typescript
// Built-in pipes
@Get(':id')
async findOne(
  @Param('id', ParseIntPipe) id: number,
  @Query('limit', new DefaultValuePipe(10), ParseIntPipe) limit: number,
) {}

// Validation pipe
import { ValidationPipe } from '@nestjs/common';

app.useGlobalPipes(new ValidationPipe({
  whitelist: true,
  transform: true,
  forbidNonWhitelisted: true,
}));

// Custom pipe
@Injectable()
export class ParseIntPipe implements PipeTransform<string, number> {
  transform(value: string): number {
    const val = parseInt(value, 10);
    if (isNaN(val)) {
      throw new BadRequestException('Invalid number');
    }
    return val;
  }
}
```

---

## Decorators

**Định nghĩa**: Decorators là functions được prefix với @ được sử dụng để attach metadata và behavior vào classes và methods.

**Ví dụ**:
```typescript
// Request decorators
@Get()
async findAll(
  @Query('page') page: number,
  @Query('limit') limit: number,
  @Body() body: any,
  @Headers('authorization') auth: string,
  @Ip() ip: string,
  @Param('id') id: string,
  @Request() req: any,
) {}

// Custom decorators
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const CurrentUser = createParamDecorator(
  (data: string | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;
    
    return data ? user?.[data] : user;
  },
);

// Usage
@Get('profile')
async getProfile(@CurrentUser('id') userId: number) {}
```

---

## Middleware

**Định nghĩa**: Middleware là functions có quyền truy cập vào request và response objects, và next middleware function trong application cycle.

**Ví dụ**:
```typescript
// logger.middleware.ts
@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
  }
}

// Functional middleware
export const LoggerMiddleware = (req: Request, res: Response, next: NextFunction) => {
  console.log(`Request...`);
  next();
};

// Apply in module
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(LoggerMiddleware).forRoutes('*');
  }
}
```

---

## Exception Filters

**Định nghĩa**: Exception Filters xử lý exceptions thrown trong application và tạo custom error responses.

**Ví dụ**:
```typescript
// http-exception.filter.ts
@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();
    
    const status = exception instanceof HttpException
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;
      
    const message = exception instanceof HttpException
      ? exception.getResponse()
      : 'Internal server error';
      
    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message,
    });
  }
}

// Usage
app.useGlobalFilters(new HttpExceptionFilter());
```

---

## Interceptors

**Định nghĩa**: Interceptors có khả năng wrap methods và thêm logic before/after method execution.

**Ví dụ**:
```typescript
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, T> {
  intercept(context: ExecutionContext, next: CallHandler): Observable<T> {
    return next.handle().pipe(
      map(data => ({
        data,
        timestamp: new Date().toISOString(),
      })),
    );
  }
}

// Logging interceptor
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const { method, url } = request;
    const now = Date.now();
    
    return next.handle().pipe(
      tap(() => {
        const response = context.switchToHttp().getResponse();
        console.log(`${method} ${url} ${response.statusCode} - ${Date.now() - now}ms`);
      }),
    );
  }
}
```

---

## Liên kết liên quan
- [NestJS Architecture](./architecture.md)
- [NestJS Best Practices](./best-practice.md)
- [NestJS Anti-Patterns](./anti-pattern.md)
- [NestJS Checklist](./checklist.md)
- [NestJS FAQ](./faq.md)
- [NestJS Decision Tree](./decision-tree.md)
