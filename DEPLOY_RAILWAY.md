# Hybrid Deployment: Render + Railway

Deploy your application using **Render** (Backend, Agent, Frontend) and **Railway** (Worker) - all on free tiers!

## 🎯 Architecture

- **Frontend**: Render (Static Site) - Free
- **Backend**: Render (Web Service) - Free
- **Agent**: Render (Web Service) - Free
- **Worker**: Railway (Background Worker) - Free
- **Redis**: Render - Free

**Total Cost: $0/month**

---

## 📋 Part 1: Deploy on Render (Backend, Agent, Frontend, Redis)

### Step 1: Deploy Redis
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Redis"**
3. Name: `acd-redis`
4. Plan: **Free**
5. Click **"Create Redis"**
6. **Copy Internal Redis URL** (needed later)

### Step 2: Deploy Backend
1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repo
3. Settings:
   - Name: `acd-backend`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Environment Variables:
   ```
   REDIS_URL = <your-redis-internal-url>
   GOOGLE_API_KEY = <your-gemini-key>
   ```
5. **Create** and **copy the backend URL**

### Step 3: Deploy Agent
1. Click **"New +"** → **"Web Service"**
2. Connect repo
3. Settings:
   - Name: `acd-agent`
   - Root Directory: `agent`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Environment Variables:
   ```
   GOOGLE_API_KEY = <your-gemini-key>
   ```
5. **Create** and **copy the agent URL**

### Step 4: Deploy Frontend
1. Click **"New +"** → **"Static Site"**
2. Connect repo
3. Settings:
   - Name: `acd-frontend`
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
4. Environment Variables:
   ```
   VITE_API_URL = <your-backend-url>
   ```
5. **Create**

---

## 📋 Part 2: Deploy Worker on Railway

### Step 1: Sign Up for Railway
1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Sign up with GitHub (free)

### Step 2: Deploy Worker
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository
4. Railway will detect it and start deploying

### Step 3: Configure Worker Service
1. Click on your deployment
2. Go to **Settings** tab
3. Set **Root Directory**: `worker`
4. **Start Command** is auto-detected from `railway.json`

### Step 4: Add Environment Variables
Click on **Variables** tab and add:

```bash
REDIS_URL=<paste-redis-url-from-render>
AGENT_URL=<paste-agent-url-from-render>
AWS_ACCESS_KEY_ID=<your-aws-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret>
AWS_BUCKET_NAME=<your-bucket-name>
AWS_REGION=us-east-1
S3_ENDPOINT_URL=
```

### Step 5: Deploy
1. Click **"Deploy"**
2. Wait for deployment to complete
3. Check logs to verify worker started successfully

---

## ✅ Verification Checklist

### Render Services (Should all show "Live"):
- ✅ `acd-redis` - Running
- ✅ `acd-backend` - Live
- ✅ `acd-agent` - Live
- ✅ `acd-frontend` - Live

### Railway Service:
- ✅ `worker` - Deployed and running

---

## 🧪 Test Your Deployment

1. Visit your frontend URL (e.g., `https://acd-frontend.onrender.com`)
2. Paste a GitHub repository URL
3. Click **"Generate Documentation"**
4. Watch real-time status updates
5. Download generated docs when complete

### Check Logs if Something Fails:
- **Render Backend**: Check backend service logs
- **Railway Worker**: Check deployment logs in Railway dashboard
- **Render Agent**: Check agent service logs

---

## 🔧 Railway Free Tier Limits

- **550 hours/month** of execution time
- **512 MB RAM**
- **1 GB storage**
- **$5 free credit/month**

**Perfect for your worker!** 🎉

---

## 🐛 Troubleshooting

### Worker Not Processing Jobs?

**Check Railway Logs:**
1. Go to Railway dashboard
2. Click on your worker service
3. Click **"View Logs"**
4. Look for connection errors

**Common Issues:**
- ❌ Wrong Redis URL → Copy **Internal** URL from Render, not external
- ❌ Wrong Agent URL → Should be `https://acd-agent-xxx.onrender.com`
- ❌ Missing AWS credentials → Double-check all env vars

### Backend Can't Reach Worker?

**Verify Redis Connection:**
- Both backend and worker must use **same Redis URL**
- Use the **Internal** Redis URL from Render

### Railway Deployment Failed?

**Check:**
- `railway.json` exists in `worker/` folder
- `requirements.txt` exists in `worker/` folder
- Root directory is set to `worker`

---

## 💰 Total Cost Breakdown

| Service | Platform | Cost |
|---------|----------|------|
| Frontend | Render | Free |
| Backend | Render | Free |
| Agent | Render | Free |
| Redis | Render | Free |
| Worker | Railway | Free |

**Total: $0/month** 🎉

---

## 🔄 Auto-Deploy on Git Push

**Render**: Auto-deploys when you push to GitHub  
**Railway**: Auto-deploys when you push to GitHub

Just `git push` and both platforms update automatically!

---

## 📊 Monitoring

### Render Dashboard
- View logs for backend, agent, frontend
- Monitor CPU/Memory usage
- Set up email alerts

### Railway Dashboard
- View worker logs in real-time
- Monitor resource usage
- Check deployment history

---

## 🚀 Next Steps

1. ✅ Deployed all services
2. ✅ Tested documentation generation
3. 📝 Add custom domain (optional)
4. 📝 Set up monitoring alerts
5. 📝 Deploy to production branch

---

## 📚 Resources

- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **Railway Discord**: https://discord.gg/railway

Happy deploying! 🎉
