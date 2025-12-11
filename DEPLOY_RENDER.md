# Deploying to Render (100% Free Tier)

This guide deploys the entire backend stack on Render's free tier by combining the API and Worker into a single service.

## 🎯 Architecture

- **Backend + Worker**: Render Web Service (Python)
- **AI Agent**: Render Web Service (Python)
- **Redis**: Render Redis (Free Plan)
- **Frontend**: Render Static Site (or Vercel)

**Total Cost: $0/month**

---

## 🚀 Quick Deploy (Blueprint)

1. **Push to GitHub**
   Make sure `render.yaml` is in your repository.

2. **Go to Render Dashboard**
   - Click **"Blueprints"** -> **"New Blueprint Instance"**
   - Connect your repository
   - Render will auto-detect the configuration

3. **Set Environment Variables**
   Render will ask for these values:
   - `GOOGLE_API_KEY`: Your Gemini API Key
   - `OPENAI_API_KEY`: Your OpenAI API Key (optional)
   - `AWS_ACCESS_KEY_ID`: Your AWS Access Key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Key
   - `AWS_BUCKET_NAME`: Your S3 Bucket Name

4. **Deploy!**
   Click **"Apply"** and wait for services to go live.

---

## 🔧 Manual Deployment (If not using Blueprint)

### 1. Deploy Redis
- **Name**: `acd-redis`
- **Plan**: Free
- Copy **Internal Redis URL**

### 2. Deploy Backend + Worker (Web Service)
- **Name**: `acd-backend`
- **Root Directory**: `.` (Root)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `./start.sh`
- **Env Vars**:
  - `REDIS_URL`: (Internal Redis URL)
  - `GOOGLE_API_KEY`: ...
  - `AWS_...`: (AWS Credentials)
  - `AGENT_URL`: (Agent Service URL - set this after deploying agent)

### 3. Deploy Agent (Web Service)
- **Name**: `acd-agent`
- **Root Directory**: `.` (Root)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn agent.main:app --host 0.0.0.0 --port $PORT`
- **Env Vars**:
  - `GOOGLE_API_KEY`: ...

### 4. Deploy Frontend (Static Site)
- **Name**: `acd-frontend`
- **Root Directory**: `.` (Root)
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `dist`
- **Env Vars**:
  - `VITE_API_URL`: (Backend Service URL)

---

## 🐛 Troubleshooting

### Build Failed?
- Check if `requirements.txt` exists in the root directory.
- Check if `start.sh` is executable (run `chmod +x start.sh` locally and push).

### Worker Not Processing?
- Check logs of `acd-backend`. You should see both `Uvicorn running...` and `Celery worker...` logs.
- Ensure `REDIS_URL` is correct.

### Agent Error?
- Ensure `AGENT_URL` in backend env vars points to `https://acd-agent-xxx.onrender.com`.

---

## 💰 Free Tier Limits
- **Web Services**: Spin down after 15 mins of inactivity. First request will take ~30s to wake up.
- **Redis**: 25MB limit (plenty for job queue).
