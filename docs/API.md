# WashLogs API Documentation

## Base URL
`http://localhost:8000/api`

## Authentication
Authentication is enforced using Supabase JWT Bearer Tokens. All requests must include an `Authorization: Bearer <token>` header.

## Endpoints Summary

| Endpoint | Method | Description | Request Body / Params | Response | Auth Required |
|----------|--------|-------------|-----------------------|----------|---------------|
| `/api/orders` | POST | Create a new order with garments | `{"customer_name": "str", "phone_number": "str", "items": [...]}` | `201 Created` - Order details | Yes |
| `/api/orders/{order_id}` | GET | Retrieve a single order with items | Path: `order_id` (UUID) | `200 OK` - Order details | Yes |
| `/api/orders` | GET | List orders with filtering and pagination | Query: `status`, `customer_name`, `phone_number`, `limit`, `offset` | `200 OK` - List of orders | Yes |
| `/api/orders/{order_id}/status` | PATCH | Update order status | `{"status": "RECEIVED \| PROCESSING \| READY \| DELIVERED"}` | `200 OK` - Updated order | Yes |
| `/api/orders/{order_id}` | DELETE | Delete an order | Path: `order_id` (UUID) | `204 No Content` | Yes |
| `/api/dashboard` | GET | Get business analytics | None | `200 OK` - Dashboard stats | Yes |

## Detailed Models

### Response Format
All operations typically follow this standardized wrapper format on success or fail.

| Status | Details | Example Payload |
|--------|---------|-----------------|
| **Success (2xx)** | Returns a `data` object wrapping the payload with a timestamp. | `{"data": {...}, "timestamp": "2024-01-15T..."}` |
| **Error (4xx, 5xx)** | Returns an `error` array outlining the invalid fields and status code. | `{"error": "Validation error", "details": [...], "status_code": 422}` | 

## Validation Rules

| Field | Restrictions |
|-------|--------------|
| `customer_name` | Required, Max 100 characters, Cannot be whitespace. |
| `phone_number` | Required, Minimum 10 digits. |
| `garment_type` | Enum: Shirt, Pants, Saree, Dress, Skirt, Jacket, Coat, Sweater, Blouse, Other. | 
| `quantity` | Required, Positive Integer (> 0). |
| `price_per_item`| Required, Positive Float (> 0, rounded to 2 decimal places). |

## Status Codes

| Code | Type | Description |
|------|------|-------------|
| `200 OK` | Success | Request succeeded. |
| `201 Created` | Success | Resource created (e.g., Order Created). |
| `204 No Content` | Success | Deletion successful. |
| `400 Bad Request` | Client Error | Invalid request structure. |
| `401 Unauthorized` | Client Error | Missing or invalid Bearer JWT Token. |
| `404 Not Found` | Client Error | Target resource unavailable. |
| `422 Unprocessable` | Client Error | Schema validation error (e.g., missing required fields). |
| `500 Server Error` | Server Error | Unhandled server exception. |

## Testing

You can use the local `/docs` or `/redoc` interfaces for live API testing:
* **Swagger UI**: `http://localhost:8000/api/docs`
* **ReDoc**: `http://localhost:8000/api/redoc`