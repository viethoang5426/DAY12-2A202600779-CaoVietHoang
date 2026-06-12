# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. API Key bị hardcode trực tiếp trong mã nguồn.
2. Port bị fix cứng ở một giá trị cố định.
3. Chạy ứng dụng với chế độ Debug (`debug=True`).
4. Không có endpoint kiểm tra sức khoẻ (health check).
5. Không có logic tắt ứng dụng an toàn (graceful shutdown).

### Exercise 1.3: Comparison table
| Feature | Develop (Basic) | Production (Advanced) | Why Important? |
|---------|-----------------|-----------------------|----------------|
| Config | Hardcode | Env vars (Biến môi trường) | Bảo mật thông tin nhạy cảm (secrets) và linh hoạt khi đổi môi trường mà không cần sửa code. |
| Health check | Không có | `/health`, `/ready` | Giúp hệ thống quản lý (K8s, Docker) biết ứng dụng còn sống không để điều phối traffic hoặc tự động restart. |
| Logging | `print()` | Structured JSON Logging | Phân tích log dễ dàng hơn, tương thích với các công cụ thu thập log tập trung (Datadog, ELK). |
| Shutdown | Đột ngột | Graceful | Đảm bảo các request đang xử lý dở được hoàn tất trước khi container tắt hẳn, tránh mất mát dữ liệu. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: `python:3.11-slim`
2. Working directory: `/app`
3. Tại sao COPY requirements.txt trước? Để tận dụng Docker layer caching. Thư viện ít khi thay đổi hơn mã nguồn, việc cache lại sẽ giúp build nhanh hơn nhiều ở các lần sau.
4. CMD vs ENTRYPOINT khác nhau thế nào? `CMD` là tham số mặc định dễ dàng ghi đè khi chạy container, còn `ENTRYPOINT` định nghĩa lệnh chính bắt buộc để container hoạt động như một executable (khó ghi đè hơn).

### Exercise 2.3: Image size comparison
- Develop: Khoảng ~300 MB
- Production (Multi-stage build): Khoảng ~150 MB
- Difference: Giảm khoảng ~50%

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: `[Đợi điền sau khi có Public URL]`
- Screenshot: `[Đợi điền sau khi có Public URL]`

## Part 4: API Security

### Exercise 4.1-4.3: Test results
- API trả về `401 Unauthorized` nếu request thiếu header `X-API-Key`.
- API trả về `429 Too Many Requests` khi một user gửi quá số lượng limit (10 req/min).
- Với key và rate hợp lệ, API trả về `200 OK`.

### Exercise 4.4: Cost guard implementation
- Lưu trữ lượng tiền tiêu thụ của từng user trong Redis với key dạng `budget:{user_id}:{YYYY-MM}`.
- Mỗi lần gọi API sẽ cộng dồn chi phí dự kiến (`INCRBYFLOAT`).
- Nếu số lượng > $10 thì từ chối (trả về lỗi 403 hoặc 402).
- Key sẽ tự động xoá sau khoảng 32 ngày (`EXPIRE`).

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- Triển khai Stateless hoàn toàn bằng cách dời biến `conversation_history` từ RAM của process Python sang Redis (lưu bằng list hoặc json).
- Các API endpoints `/health` và `/ready` được đảm bảo lúc nào cũng sẵn sàng ping đến Redis để phản ánh trạng thái của container.
- Với việc Stateless và Health Check tốt, mô hình Docker Compose với Nginx có thể scale ứng dụng lên thành 3 instances (`--scale agent=3`) để nhận request đồng thời mà không bị conflict session.
