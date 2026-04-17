# WashLogs Deployment & DevOps

## 🚢 Deployment

### Google Cloud Run

1. **Build Docker image**
   ```bash
   docker build -t washlogs-backend:latest .
   ```

2. **Push to Container Registry**
   ```bash
   docker tag washlogs-backend:latest gcr.io/YOUR_PROJECT_ID/washlogs-backend:latest
   docker push gcr.io/YOUR_PROJECT_ID/washlogs-backend:latest
   ```

3. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy washlogs-backend \
     --image gcr.io/YOUR_PROJECT_ID/washlogs-backend:latest \
     --platform managed \
     --region us-central1 \
     --set-env-vars DATABASE_URL=$DATABASE_URL,SUPABASE_URL=$SUPABASE_URL
   ```

### Vercel (Frontend)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   cd frontend
   vercel
   ```

3. **Configure Environment Variables in Vercel Dashboard**
   - `VITE_SUPABASE_URL`: Your Supabase URL
   - `VITE_SUPABASE_ANON_KEY`: Your Supabase Anon Key

### Environment Setup for Production

```env
DEBUG=false
ENVIRONMENT=production
SUPABASE_URL=prod_url
SUPABASE_KEY=prod_key
SUPABASE_SERVICE_KEY=prod_service_key
DATABASE_URL=postgresql://prod_user:prod_pass@prod_host:5432/washlogs
CORS_ORIGINS=https://yourdomain.com
```

## 📝 Logging

Logs are stored in the `logs/` directory with daily rotation:
- **washlogs.log**: Combined application logs

Check logs:
```bash
tail -f logs/washlogs.log
```
