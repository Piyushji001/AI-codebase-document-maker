# Deploying to Render

Complete guide to deploy the Autonomous Codebase Documenter on Render.

## 📋 Prerequisites

1. **GitHub Repository**: Push your code to GitHub
2. **Render Account**: Sign up at https://render.com
3. **AWS S3 Bucket**: For document storage (free tier available)
   - Create a bucket at https://console.aws.amazon.com/s3
   - Get Access Key ID and Secret Access Key
4. **API Keys**: Gemini or OpenAI API key

---

## 🚀 Quick Deploy (Using Blueprint)

### Option 1: One-Click Deploy

1. Push your code to GitHub (make sure `render.yaml` is included)
2. Go to https://dashboard.render.com/blueprints
3. Click "New Blueprint Instance"
4. Connect your GitHub repository
5. Render will detect `render.yaml` and create all services automatically
6. Set environment variables (see below)

---

## 🔧 Manual Deployment

If you prefer manual setup:

### 1. Deploy Redis

1. Go to Render Dashboard → New → Redis
2. Name: `acd-redis`
3. Plan: **Free** (or Starter if you need persistence)
4. Click "Create Redis"
5. Copy the **Internal Redis URL** (needed for next steps)

### 2. Deploy Backend (FastAPI)

1. New → Web Service
2. Connect your GitHub repo
3. Settings:
   - **Name**: `acd-backend`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Environment Variables:
   ```
   REDIS_URL = <your-redis-internal-url>
   GOOGLE_API_KEY = <your-gemini-key>
   OPENAI_API_KEY = <your-openai-key>
   ```
5. Click "Create Web Service"

### 3. Deploy Worker (Celery)

1. New → Background Worker
2. Connect repository
3. Settings:
   - **Name**: `acd-worker`
   - **Root Directory**: `worker`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `celery -A tasks worker --loglevel=info`
4. Environment Variables:
   ```
   REDIS_URL = <your-redis-internal-url>
   AWS_ACCESS_KEY_ID = <your-aws-key>
   AWS_SECRET_ACCESS_KEY = <your-aws-secret>
   AWS_BUCKET_NAME = <your-bucket-name>
   AWS_REGION = us-east-1
   S3_ENDPOINT_URL = (leave empty for real S3)
   ```
5. Create

### 4. Deploy Agent (LangGraph)

1. New → Web Service
2. Settings:
   - **Name**: `acd-agent`
   - **Root Directory**: `agent`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Environment Variables:
   ```
   GOOGLE_API_KEY = <your-gemini-key>
   OPENAI_API_KEY = <your-openai-key>
   ```
4. Create

### 5. Deploy Frontend (React)

1. New → Static Site
2. Settings:
   - **Name**: `acd-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
3. Environment Variables:
   ```
   VITE_API_URL = <your-backend-url>
   ```
   (Get backend URL from step 2)
4. Create

---

## 🔑 Required Environment Variables Summary

### Backend
- `REDIS_URL` - From Redis service
- `GOOGLE_API_KEY` or `OPENAI_API_KEY`

### Worker
- `REDIS_URL` - From Redis service
- `AWS_ACCESS_KEY_ID` - From AWS
- `AWS_SECRET_ACCESS_KEY` - From AWS
- `AWS_BUCKET_NAME` - Your S3 bucket name
- `AWS_REGION` - e.g., `us-east-1`
- `S3_ENDPOINT_URL` - Leave empty

### Agent
- `GOOGLE_API_KEY` or `OPENAI_API_KEY`

### Frontend
- `VITE_API_URL` - Backend service URL

---

## 💰 Render Free Tier

**What's Free:**
- Redis: 25MB storage
- 3 Web Services (750 hrs/month each)
- Background Workers: 750 hrs/month
- Static Sites: Unlimited

**Monthly Cost: $0** (within free tier limits)

**Important**: Free tier services spin down after 15 minutes of inactivity. First request after spin-down takes ~30 seconds.

---

## 🎯 Using Real AWS S3

### Create S3 Bucket

```bash
# Using AWS CLI
aws s3 mb s3://your-unique-bucket-name
aws s3api put-public-access-block \
    --bucket your-unique-bucket-name \
    --public-access-block-configuration \
    "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
```

### Get AWS Credentials

1. Go to AWS IAM Console
2. Create new user with S3 permissions
3. Generate Access Keys
4. Save Access Key ID and Secret Access Key

---

## 📝 Post-Deployment

### Update Frontend API URL

After backend is deployed, update frontend's `VITE_API_URL`:
1. Go to frontend service settings
2. Environment → Edit
3. Set `VITE_API_URL` to backend URL (e.g., `https://acd-backend.onrender.com`)
4. Save and trigger redeploy

### Test Your Deployment

1. Visit your frontend URL
2. Submit a test GitHub repo
3. Check logs if something fails:
   - Backend logs: Check API errors
   - Worker logs: Check Celery errors
   - Agent logs: Check LLM errors

---

## 🐛 Troubleshooting

### "Service Unavailable" on first request
- **Cause**: Free tier services sleep after inactivity
- **Fix**: Wait 30 seconds for service to wake up

### Worker not processing jobs
- **Check**: Redis URL is correct in worker env vars
- **Check**: Worker logs for connection errors

### Agent returning errors
- **Check**: API key is valid
- **Check**: Model name is correct (`gemini-2.5-flash` or `gpt-4o-mini`)

### Downloads not working
- **Check**: S3 bucket permissions allow public access
- **Check**: AWS credentials are correct

---

## 🔄 Updating Your Deployment

Render auto-deploys on every push to your GitHub repo:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render will automatically rebuild and redeploy! 🎉

---

## 📊 Monitoring

- **Logs**: Available in Render dashboard for each service
- **Metrics**: CPU, Memory usage visible per service
- **Alerts**: Set up email alerts for failures

---

## 🚀 Upgrade to Paid Plans

If you exceed free tier or need better performance:
- **Starter Plan**: $7/month per service (no sleep, more RAM)
- **Standard Plan**: $25/month (auto-scaling, more resources)

---

## 📚 Additional Resources

- Render Docs: https://render.com/docs
- Render Discord: https://discord.gg/render
- AWS S3 Pricing: https://aws.amazon.com/s3/pricing/
