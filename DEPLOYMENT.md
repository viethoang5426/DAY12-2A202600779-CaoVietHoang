# Deployment Information

## Public URL
https://day12-2a202600779-caoviethoang-production.up.railway.app

## Platform
Railway / Render / Cloud Run (Please choose one)

## Test Commands

### Health Check
```bash
curl https://day12-2a202600779-caoviethoang-production.up.railway.app/health
# Expected: {"status": "ok"}
```

### API Test (with authentication)
```bash
curl -X POST https://day12-2a202600779-caoviethoang-production.up.railway.app/ask \
  -H "X-API-Key: my-super-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
```

## Environment Variables Set
- `PORT` (Mặc định Railway/Render sẽ tự cung cấp)
- `REDIS_URL` (Cần tạo một Redis service trên Railway/Render và truyền URL vào biến này)
- `AGENT_API_KEY` = `my-super-secret-key-123`
- `LOG_LEVEL` = `INFO`

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
