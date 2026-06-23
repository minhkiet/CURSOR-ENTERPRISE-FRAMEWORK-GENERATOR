# Supabase Decision Tree - Cây Quyết Định

## Quyết định về Hosting

### Câu hỏi: Host ở đâu?

- **Supabase Cloud**: Managed, easy
- **Self-host**: Full control

## Quyết định về Auth

### Câu hỏi: Auth provider nào?

- **Email/Password**: Simple
- **OAuth**: Google, GitHub, etc.

## Quyết định về Security

### Câu hỏi: Access control?

- **RLS**: Enable always
- **API Keys**: Proper usage

## Summary

Supabase Cloud + RLS + OAuth là common approach.
