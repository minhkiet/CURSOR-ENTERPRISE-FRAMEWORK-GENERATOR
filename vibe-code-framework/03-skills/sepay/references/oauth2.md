# OAuth2: third-party apps acting for SePay users

## When

An app used by many SePay customers (plugin, accounting tool, marketplace) needs to read their bank accounts / transactions or manage their webhooks, with each user granting access. For your own company only, use an API key instead (`sepay-api.md`).

## Flow (authorization code)

1. Register the app in my.sepay.vn → `client_id`, `client_secret`, redirect URI, scopes.
2. Redirect the user to `https://my.sepay.vn/oauth/authorize?response_type=code&client_id=…&redirect_uri=…&scope=<space-separated>&state=<random>`.
3. Callback `?code=…&state=…`: verify `state` against the session (CSRF), then exchange the code at `https://my.sepay.vn/oauth/token` server side.
4. Call the API with `Authorization: Bearer <access_token>`.
5. Refresh with the refresh token before / when the access token expires (access ~1 h, refresh ~1 month; check `/vi/sepay-oauth2/access-token`).
6. Handle revocation: a 401 after refresh means the user revoked access; ask them to reconnect.

## Scopes (check the docs for the current list)

`bank-account:read`, `transaction:read`, `webhook:read`, `webhook:write`, `webhook:delete`, `profile`, `company`. Request the fewest that do the job.

## Best practice and traps

- `state` is required: random, stored server side, compared exactly on callback.
- Exchange codes and store tokens server side, encrypted at rest; never put `client_secret` in a browser or mobile app.
- Redirect URI must match the registered one exactly.
- Store tokens per SePay user / company; refresh atomically so two workers do not burn the same refresh token.
- Webhooks created through OAuth belong to the user's company: show the user what you create, delete them on disconnect.

## Docs map

- `/vi/sepay-oauth2/tong-quan#cac-pham-vi-scopes` "Các phạm vi (scopes)" · `#base-url-api` "Base URL API"
- `/vi/sepay-oauth2/dang-ky-ung-dung#cach-dang-ky-ung-dung` "Cách đăng ký ứng dụng"
- `/vi/sepay-oauth2/bat-dau-nhanh#urls-quan-trong` "URLs quan trọng" · `#tong-hop-luong-tich-hop` · `#ma-loi-thuong-gap`
- `/vi/sepay-oauth2/luong-xac-thuc#buoc-4-doi-ma-uy-quyen-lay-access-token` · `#buoc-6-lam-moi-access-token` · `#xu-ly-loi`
- `/vi/sepay-oauth2/access-token#luu-tru-access-token-an-toan` · `#quan-ly-token-het-han`
- APIs: `/vi/sepay-oauth2/tai-khoan-ngan-hang`, `/vi/sepay-oauth2/giao-dich`, `/vi/sepay-oauth2/api-webhook`, `/vi/sepay-oauth2/cong-ty`, `/vi/sepay-oauth2/nguoi-dung`
