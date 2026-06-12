# Deployment Information

## Public URL
[YOUR_PUBLIC_URL_HERE] (e.g. https://your-agent.railway.app)

## Platform
Railway / Render / Cloud Run (Please choose one)

## Test Commands

### Health Check
```bash
curl [YOUR_PUBLIC_URL_HERE]/health
# Expected: {"status": "ok"}
```

### API Test (with authentication)
```bash
curl -X POST [YOUR_PUBLIC_URL_HERE]/ask \
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
