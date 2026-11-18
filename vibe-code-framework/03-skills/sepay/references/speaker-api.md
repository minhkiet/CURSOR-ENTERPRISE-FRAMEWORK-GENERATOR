# Speaker API (SoundBox): payment announcer devices

## When

For partners that buy SePay speakers wholesale (white-label, under their own brand) and run them for their own merchants: POS / sales software, payment platforms, fintechs. A single shop that only wants a speaker at its own counter is not the audience: tell it to contact SePay, do not start an API integration. The partner app pairs the speakers with its merchants and makes them announce each successful payment. The speaker only announces; money goes straight to the merchant's bank account. The partner decides when a payment succeeded (e.g. from a SePay webhook, `webhook.md`) and then calls the speaker.

## Flow

1. Get `client_id` / `client_secret` from SePay (partner credentials; contact SePay first).
2. `POST /token/create` with Basic auth `client_id:client_secret` → Bearer token, valid about 100 minutes; cache and renew before expiry.
3. Pairing, once per device:
   1. `POST /speaker/pair/check` with the serial number: the device exists and is free.
   2. `POST /speaker/pair/request`: the speaker reads a 4-digit OTP aloud.
   3. `POST /speaker/pair/verify` with the OTP the merchant heard: paired.
4. Per payment: `POST /speaker/transactions/notify` → the speaker announces the amount.
5. Optional: `POST /speaker/transactions/check_notify` to confirm it played.

Base URL (production): `https://speaker-api.sepay.vn/devices/v1`; check `/vi/speaker-api/tong-quan#moi-truong` for current hosts.

## Best practice and traps

- Notify only after you confirmed the payment yourself (webhook with dedupe by transaction `id`); never announce from the client side or from an unverified redirect.
- Make notify idempotent: one transaction → one announcement, even if your webhook handler runs twice. Notify only from the request whose state transition changed the row (`integration-design.md` § 3).
- Keep the partner secret server side; one cached token for the service, not one per request.
- OTP pairing needs the merchant present at the device; handle wrong / expired OTP by requesting a new one.
- Handle device-offline errors without blocking order confirmation: the announcement is a side effect.

## Docs map

- `/vi/speaker-api/tong-quan#luong-hoat-dong` "Luồng hoạt động" · `#moi-truong` "Môi trường"
- `/vi/speaker-api/bat-dau-nhanh` (long page, read one step): `#buoc-1-lay-access-token` · `#buoc-3-lien-ket-thiet-bi` · `#buoc-4-gui-thong-bao-bien-dong-so-du` · `#tong-hop-luong-tich-hop` · `#ma-loi-thuong-gap`
- Endpoints: `/vi/speaker-api/api-kiem-tra-thiet-bi`, `/vi/speaker-api/yeu-cau-lien-ket-thiet-bi`, `/vi/speaker-api/kiem-tra-otp`, `/vi/speaker-api/api-thong-bao-bien-dong-so-du`, `/vi/speaker-api/api-chi-tiet-trang-thai-bien-dong-so-du`, `/vi/speaker-api/tao-access-token`
