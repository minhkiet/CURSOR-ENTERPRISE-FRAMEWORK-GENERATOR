# Naming Convention Template

## Quy ước đặt tên

### File Naming

#### Rules Files
```
[category]-[name].mdc
```
Ví dụ:
- core-architecture.mdc
- token-optimization.mdc
- nextjs-best-practices.mdc

#### Skills Files
```
[category]-[name].mdc
```
Ví dụ:
- debug.mdc
- code-review.mdc
- rag-builder.mdc

#### Knowledge Files
```
[category]/[topic].md
```
Ví dụ:
- knowledge/nextjs/glossary.md
- knowledge/postgres/best-practice.md

#### Prompt Files
```
[type]-[name].prompt.md
```
Ví dụ:
- bug-fix.prompt.md
- feature-build.prompt.md

#### Workflow Files
```
[action]-[object].md
```
Ví dụ:
- build-feature.md
- fix-bug.md

### Code Naming

#### TypeScript
```typescript
// Components: PascalCase
// UserProfile.tsx
// LoginForm.tsx

// Functions: camelCase
// function getUserData()
// function calculateTotal()

// Constants: UPPER_SNAKE_CASE
// const MAX_RETRY_COUNT = 3
// const API_BASE_URL = 'https://api.example.com'

// Interfaces: PascalCase with I prefix (optional)
// interface IUserData
// interface UserProfile

// Types: PascalCase
// type UserStatus = 'active' | 'inactive'
```

#### C#
```csharp
// Classes: PascalCase
// public class UserService
// public class OrderRepository

// Methods: PascalCase
// public User GetUserById(int id)
// public void CreateOrder(Order order)

// Properties: PascalCase
// public string UserName { get; set; }

// Constants: PascalCase
// public const int MaxRetryCount = 3

// Interfaces: PascalCase with I prefix
// public interface IUserService
```

#### PHP (Laravel)
```php
// Controllers: PascalCase
// UserController.php
// OrderController.php

// Models: PascalCase, singular
// User.php
// Order.php

// Migrations: snake_case with timestamp
// 2024_01_01_000000_create_users_table.php

// Methods: camelCase
// public function getUserData()

// Properties: camelCase
// protected $fillable
```

### Database Naming

#### Tables
```
snake_case, plural
```
Ví dụ:
- users
- orders
- order_items
- user_profiles

#### Columns
```
snake_case
```
Ví dụ:
- user_id
- created_at
- first_name
- is_active

#### Indexes
```
idx_[table]_[column(s)]
```
Ví dụ:
- idx_users_email
- idx_orders_user_id_created_at

#### Foreign Keys
```
fk_[table]_[referenced_table]
```
Ví dụ:
- fk_orders_users
- fk_order_items_orders

### API Naming

#### REST Endpoints
```
/api/v{version}/{resource}
/api/v1/users
/api/v1/orders
```

#### HTTP Methods
```
GET     - Retrieve
POST    - Create
PUT     - Update (full)
PATCH   - Update (partial)
DELETE  - Delete
```

### Variable Naming

#### Boolean Variables
```
is[Something]
has[Something]
can[Something]
should[Something]
```
Ví dụ:
- isActive
- hasPermission
- canEdit

#### Array Variables
```
[pluralNoun]
users
items
products
```

#### Function Variables
```
Prefix: get, set, create, update, delete, find, list
```
Ví dụ:
- getUserById()
- createOrder()
- findUsersByEmail()

### CSS Naming (BEM)

```
.block__element--modifier
```
Ví dụ:
- .button__icon--primary
- .card__title--large
- .form__input--error

### Git Naming

#### Branch Naming
```
{type}/{ticket-id}-{short-description}
feature/PROJ-123-add-user-auth
bugfix/PROJ-456-fix-login-error
hotfix/PROJ-789-critical-security
```

#### Commit Naming
```
{type}: {description}

feat: add user authentication
fix: resolve login timeout issue
docs: update API documentation
refactor: improve query performance
test: add unit tests for user service
```

## Liên kết
- [[rules/coding-standards]] - Coding Standards
```
