# Testing Patterns Reference

> Based on [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) references

---

## Test Pyramid

```
         ┌─────────────────────────┐
         │         E2E            │  5%
         │   (End-to-End Tests)    │  Critical user journeys
         └─────────────────────────┘
           ┌─────────────────────┐
           │      Integration      │  15%
           │   (API, Components)   │  Component interactions
           └─────────────────────┘
         ┌─────────────────────────┐
         │          Unit           │  80%
         │    (Pure Functions)     │  Fast, isolated
         └─────────────────────────┘
```

**Ratio:** 80/15/5 (Unit/Integration/E2E)

---

## Test Naming Convention

### Structure

```
[UnitOfWork]_[Scenario]_[ExpectedBehavior]
```

### Examples

```typescript
// Unit Tests
describe('calculateDiscount', () => {
  it('returns 0 when amount is zero', () => { ... });
  it('returns 10% off for amounts over $100', () => { ... });
  it('caps discount at $50 maximum', () => { ... });
});

describe('UserService', () => {
  describe('createUser', () => {
    it('throws ValidationError when email is invalid', () => { ... });
    it('hashes password before storing', () => { ... });
    it('sends welcome email on success', () => { ... });
  });
});

// Integration Tests
describe('POST /api/users', () => {
  it('creates user and returns 201', () => { ... });
  it('returns 400 for duplicate email', () => { ... });
  it('returns 401 without auth token', () => { ... });
});
```

---

## Test Structure (AAA Pattern)

```typescript
describe('FeatureName', () => {
  it('should do X when Y', () => {
    // Arrange
    const input = createTestInput();
    const mock = jest.fn();
    
    // Act
    const result = subject.method(input, mock);
    
    // Assert
    expect(result).toEqual(expectedOutput);
    expect(mock).toHaveBeenCalledWith(expectedArg);
  });
});
```

---

## Mocking Strategies

### What to Mock

| Type | Mock? | Why |
|------|-------|-----|
| External APIs | ✅ Yes | Isolation, speed |
| Database | ✅ Yes | Speed, reliability |
| Time/Date | ✅ Yes | Predictability |
| Random | ✅ Yes | Determinism |
| Internal modules | ❌ No | Test actual behavior |
| Simple pure functions | ❌ No | No benefit |

### Mocking Best Practices

```typescript
// ❌ BAD: Mocking everything
it('validates email', () => {
  const mockValidator = jest.fn().mockReturnValue(true);
  const result = validateEmail('test@test.com', mockValidator);
  expect(result).toBe(true);
});

// ✅ GOOD: Test real behavior, mock external deps
it('validates email format', () => {
  const email = 'test@test.com';
  expect(isValidEmail(email)).toBe(true);
});

// ✅ GOOD: Mock only external services
it('fetches user from API', async () => {
  jest.spyOn(fetch, 'userService').mockResolvedValue(mockUser);
  const user = await getUser(1);
  expect(user.name).toBe('John');
});
```

---

## React Testing

### Component Testing

```typescript
describe('LoginForm', () => {
  it('renders email and password inputs', () => {
    render(<LoginForm onSubmit={jest.fn()} />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  it('shows error for invalid email', async () => {
    const onSubmit = jest.fn();
    render(<LoginForm onSubmit={onSubmit} />);
    
    userEvent.type(screen.getByLabelText(/email/i), 'invalid');
    userEvent.type(screen.getByLabelText(/password/i), 'password123');
    userEvent.click(screen.getByRole('button', { name: /sign in/i }));
    
    expect(await screen.findByText(/valid email/i)).toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('calls onSubmit with credentials on valid submission', async () => {
    const onSubmit = jest.fn();
    render(<LoginForm onSubmit={onSubmit} />);
    
    userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    userEvent.type(screen.getByLabelText(/password/i), 'password123');
    userEvent.click(screen.getByRole('button', { name: /sign in/i }));
    
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
  });
});
```

### Hook Testing

```typescript
describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter());
    act(() => result.current.increment());
    expect(result.current.count).toBe(1);
  });

  it('accepts custom initial value', () => {
    const { result } = renderHook(() => useCounter({ initial: 10 }));
    expect(result.current.count).toBe(10);
  });
});
```

---

## API Testing

### REST API

```typescript
describe('Users API', () => {
  const baseUrl = '/api/users';
  
  describe(`GET ${baseUrl}`, () => {
    it('returns list of users', async () => {
      const response = await request(app).get(baseUrl);
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('data');
      expect(Array.isArray(response.body.data)).toBe(true);
    });

    it('supports pagination', async () => {
      const response = await request(app)
        .get(baseUrl)
        .query({ page: 1, limit: 10 });
      
      expect(response.body).toHaveProperty('pagination');
      expect(response.body.pagination.page).toBe(1);
    });
  });

  describe(`POST ${baseUrl}`, () => {
    it('creates new user', async () => {
      const newUser = {
        email: 'new@example.com',
        name: 'New User',
        password: 'SecurePass123!'
      };
      
      const response = await request(app)
        .post(baseUrl)
        .send(newUser);
      
      expect(response.status).toBe(201);
      expect(response.body.email).toBe(newUser.email);
      expect(response.body).not.toHaveProperty('password');
    });

    it('returns 400 for invalid email', async () => {
      const response = await request(app)
        .post(baseUrl)
        .send({ email: 'invalid', name: 'Test', password: 'pass' });
      
      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error');
    });
  });
});
```

---

## E2E Testing

### Critical User Journeys

```typescript
describe('Checkout Flow', () => {
  beforeEach(() => {
    // Reset database, login
  });

  it('completes full checkout process', () => {
    // 1. Browse products
    landingPage.visit();
    landingPage.searchFor('laptop');
    
    // 2. Add to cart
    productPage.addToCart();
    expect(cartPage.itemCount()).toBe(1);
    
    // 3. Checkout
    cartPage.checkout();
    
    // 4. Enter shipping
    checkoutPage.enterShipping(testAddress);
    
    // 5. Enter payment
    checkoutPage.enterPayment(testPayment);
    
    // 6. Place order
    checkoutPage.placeOrder();
    
    // 7. Verify confirmation
    expect(confirmationPage.orderNumber()).toBeVisible();
    expect(email inbox).toReceiveOrderConfirmation();
  });

  it('handles payment failure gracefully', () => {
    checkoutPage.enterInvalidPayment();
    checkoutPage.placeOrder();
    
    expect(checkoutPage.errorMessage()).toContain('payment declined');
    expect(orderConfirmationPage).not.toBeVisible();
  });
});
```

---

## Anti-Patterns to Avoid

### Test Design

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Asserting on implementation details | Brittle tests | Test behavior, not structure |
| No assertions | Useless tests | Always assert something |
| Overspecific mocks | Overmocked tests | Use real objects when safe |
| Testing multiple things | Complex tests | One assertion per test |
| No setup/teardown | Shared state | Clean state per test |
| Sleep/hard waits | Flaky tests | Use proper waits |

### Examples

```typescript
// ❌ BAD: Testing implementation
it('calls the validate method', () => {
  const spy = jest.spyOn(validator, 'validate');
  processInput(data);
  expect(spy).toHaveBeenCalled(); // Brittle!
});

// ✅ GOOD: Testing behavior
it('rejects invalid input', () => {
  const result = processInput(invalidData);
  expect(result.valid).toBe(false);
  expect(result.errors).toContainEqual({ field: 'email' });
});

// ❌ BAD: No assertion
it('processes data', () => {
  processData(data);
  // No expect!
});

// ✅ GOOD: Clear assertion
it('processes data correctly', () => {
  const result = processData(data);
  expect(result).toEqual(expectedOutput);
});
```

---

## Beyonce Rule

> "If you liked it, you should have put a test on it."

For every function you write:
- ✅ Unit test the happy path
- ✅ Unit test error cases
- ✅ Integration test the flow
- ✅ E2E test critical journeys

---

## Links

- [agent-skills](https://github.com/addyosmani/agent-skills) - Source reference
- [[skill-registry]] - Testing skill triggers
- [[testing]] - Testing rules in framework
