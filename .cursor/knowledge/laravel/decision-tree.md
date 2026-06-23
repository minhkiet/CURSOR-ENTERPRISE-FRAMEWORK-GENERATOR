# Laravel Decision Tree - Cây Quyết Định Laravel

## Quyết định về Auth

### Câu hỏi: Authentication solution nào?

- **Breeze**: Simple, modern (recommended)
- **Fortify**: Headless authentication
- **Sanctum**: API tokens, SPA auth

## Quyết định về Database

### Câu hỏi: ORM nào?

- **Eloquent**: Full-featured ORM (recommended)
- **Query Builder**: Simple queries

## Quyết định về Frontend

### Câu hỏi: Frontend stack nào?

- **Blade + Vue/React**: Traditional
- **Inertia.js**: SPA feel với Blade
- **API + Separate Frontend**: Headless

## Quyết định về Queue

### Câu hỏi: Queue driver nào?

- **Redis**: Fast (recommended)
- **Database**: Simple
- **Beanstalkd**: Alternative

## Summary

Laravel Breeze + Eloquent + Redis là recommended stack.
