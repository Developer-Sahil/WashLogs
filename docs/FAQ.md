# WashLogs FAQ 

### Q: I am getting `✗ Failed to initialize database` when starting the server
**A**: This points towards a connection failure with SQLAlchemy. Please verify your `DATABASE_URL` environment variable is fully qualified connecting to the Postgres instance in your `.env` file.

### Q: I am getting `✗ Failed to initialize Supabase client` upon startup
**A**: Ensure your `SUPABASE_URL` and `SUPABASE_KEY` are correct, injected correctly, and correspond to the active environment inside `.env`.

### Q: Why do I encounter CORS blocking errors in the browser client?
**A**: `Access to XMLHttpRequest blocked by CORS policy` means your frontend domain is not explicitly whitelisted via `CORS_ORIGINS`. Add your frontend base URL into the `CORS_ORIGINS` section inside `.env` configurations.

### Q: How do I test my API?
**A**: Out of the box, you can access testing natively in the browser via:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc 

### Q: I hit `ValueError: Quantity must be a positive integer` when ordering?
**A**: Pydantic validates inputs strictly out of the box based on `src.models.schemas.GarmentType` and standard rules. Orders require `quantity > 0` and total integer limits across requests. Check your JSON format payload is correct.
