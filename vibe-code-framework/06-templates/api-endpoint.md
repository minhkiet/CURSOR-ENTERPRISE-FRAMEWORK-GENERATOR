# API Endpoint Template

> **Version:** 1.0.0 | **Format:** REST

---

## Express.js Template

```typescript
// controllers/userController.ts
import { Request, Response, NextFunction } from 'express';
import { ZodError } from 'zod';
import { CreateUserSchema, UpdateUserSchema } from '../schemas/userSchema';
import { CreateUserUseCase } from '../application/useCases/CreateUserUseCase';
import { GetUserUseCase } from '../application/useCases/GetUserUseCase';

export class UserController {
  constructor(
    private createUserUseCase: CreateUserUseCase,
    private getUserUseCase: GetUserUseCase
  ) {}

  async create(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const validated = CreateUserSchema.parse(req.body);
      const result = await this.createUserUseCase.execute(validated);

      if (!result.success) {
        res.status(400).json({
          error: {
            code: result.error,
            message: this.getErrorMessage(result.error)
          }
        });
        return;
      }

      res.status(201).json({
        data: {
          id: result.data.id,
          email: result.data.email,
          name: result.data.name,
          createdAt: result.data.createdAt.toISOString()
        }
      });
    } catch (error) {
      if (error instanceof ZodError) {
        res.status(400).json({
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Invalid input',
            details: error.errors.map(e => ({
              field: e.path.join('.'),
              message: e.message
            }))
          }
        });
        return;
      }
      next(error);
    }
  }

  async getById(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const { id } = req.params;
      const result = await this.getUserUseCase.execute(id);

      if (!result.success) {
        res.status(404).json({
          error: {
            code: 'NOT_FOUND',
            message: 'User not found'
          }
        });
        return;
      }

      res.json({
        data: {
          id: result.data.id,
          email: result.data.email,
          name: result.data.name,
          createdAt: result.data.createdAt.toISOString()
        }
      });
    } catch (error) {
      next(error);
    }
  }

  private getErrorMessage(code: string): string {
    const messages: Record<string, string> = {
      EMAIL_EXISTS: 'Email already exists',
      INVALID_PASSWORD: 'Invalid password format',
      WEAK_PASSWORD: 'Password must be at least 8 characters'
    };
    return messages[code] || 'An error occurred';
  }
}
```

## Validation Schema

```typescript
// schemas/userSchema.ts
import { z } from 'zod';

export const CreateUserSchema = z.object({
  email: z
    .string()
    .email('Invalid email format'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase')
    .regex(/[a-z]/, 'Password must contain lowercase')
    .regex(/[0-9]/, 'Password must contain number'),
  name: z
    .string()
    .min(1, 'Name is required')
    .max(100, 'Name must be less than 100 characters')
});

export const UpdateUserSchema = z.object({
  email: z.string().email().optional(),
  name: z.string().min(1).max(100).optional()
});

export const ListUsersSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(100).default(20),
  search: z.string().optional()
});

export type CreateUserDTO = z.infer<typeof CreateUserSchema>;
export type UpdateUserDTO = z.infer<typeof UpdateUserSchema>;
```

## Middleware

```typescript
// middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export function authenticate(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      res.status(401).json({ error: 'UNAUTHORIZED' });
      return;
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as {
      userId: string;
      role: string;
    };

    req.user = { id: decoded.userId, role: decoded.role };
    next();
  } catch (error) {
    res.status(401).json({ error: 'INVALID_TOKEN' });
  }
}

export function authorize(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!roles.includes(req.user!.role)) {
      res.status(403).json({ error: 'FORBIDDEN' });
      return;
    }
    next();
  };
}

// Extend Express Request
declare global {
  namespace Express {
    interface Request {
      user?: { id: string; role: string };
    }
  }
}
```

## Routes

```typescript
// routes/userRoutes.ts
import { Router } from 'express';
import { UserController } from '../controllers/userController';
import { authenticate, authorize } from '../middleware/auth';
import { validate } from '../middleware/validate';
import { CreateUserSchema, UpdateUserSchema, ListUsersSchema } from '../schemas/userSchema';

export function createUserRoutes(controller: UserController): Router {
  const router = Router();

  // Create user
  router.post(
    '/',
    validate(CreateUserSchema),
    controller.create.bind(controller)
  );

  // List users
  router.get(
    '/',
    authenticate,
    authorize('admin'),
    validate(ListUsersSchema),
    controller.list.bind(controller)
  );

  // Get user by ID
  router.get(
    '/:id',
    authenticate,
    controller.getById.bind(controller)
  );

  // Update user
  router.put(
    '/:id',
    authenticate,
    validate(UpdateUserSchema),
    controller.update.bind(controller)
  );

  // Delete user
  router.delete(
    '/:id',
    authenticate,
    authorize('admin'),
    controller.delete.bind(controller)
  );

  return router;
}
```

## Error Handler

```typescript
// middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express';
import { logger } from '../utils/logger';

export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  logger.error('Unhandled error', {
    error: error.message,
    stack: error.stack,
    path: req.path,
    method: req.method
  });

  if (error.name === 'ValidationError') {
    res.status(400).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: error.message
      }
    });
    return;
  }

  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'Internal server error'
    }
  });
}
```
