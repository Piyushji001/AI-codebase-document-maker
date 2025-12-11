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

## 🔧 Manual Deployment (Using "New Web Service")

If you prefer to set up services manually instead of using the Blueprint:

### 1. Deploy Redis (Prerequisite)
1. Click **New +** -> **Redis**
2. Name: `acd-redis`
3. Plan: **Free**
4. Click **Create Redis**
5. **Copy the "Internal Redis URL"** (e.g., `redis://red-xxx:6379`) - You need this for the backend.

### 2. Deploy Backend + Worker (Web Service)
1. Click **New +** -> **Web Service**
2. Connect your repository
3. Settings:
   - **Name**: `acd-backend`
   - **Root Directory**: `.` (leave blank or set to `.`)
   - **Runtime**: **Python 3**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash start.sh`
   - **Plan**: **Free**
4. **Environment Variables** (Click "Add Environment Variable"):
   - `REDIS_URL`: (Paste Internal Redis URL from Step 1)
   - `GOOGLE_API_KEY`: Your Gemini API Key
   - `AGENT_URL`: (Leave blank for now, update after deploying Agent)
5. Click **Create Web Service**

### 3. Deploy AI Agent (Web Service)
1. Click **New +** -> **Web Service**
2. Connect your repository
3. Settings:
   - **Name**: `acd-agent`
   - **Root Directory**: `.` (leave blank or set to `.`)
   - **Runtime**: **Python 3**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn agent.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: **Free**
4. **Environment Variables**:
   - `GOOGLE_API_KEY`: Your Gemini API Key
5. Click **Create Web Service**
6. **Copy the Agent URL** (e.g., `https://acd-agent-xxx.onrender.com`)

### 4. Update Backend with Agent URL
1. Go back to **acd-backend** dashboard
2. Go to **Environment**
3. Add/Update `AGENT_URL` with the URL from Step 3
4. Save Changes (This will trigger a redeploy)

### 5. Deploy Frontend (Static Site)
1. Click **New +** -> **Static Site**
2. Connect your repository
3. Settings:
   - **Name**: `acd-frontend`
   - **Root Directory**: `.` (leave blank)
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Plan**: **Free**
4. **Environment Variables**:
   - `VITE_API_URL`: (Copy URL from `acd-backend`, e.g., `https://acd-backend-xxx.onrender.com`)
5. Click **Create Static Site**

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
