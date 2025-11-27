# Deploying with Vercel

This guide covers deploying the **frontend** on Vercel and the **backend services** on Render.

## 🎯 Architecture

- **Frontend**: Vercel (React app)
- **Backend**: Render (FastAPI + Worker + Agent + Redis)

**Why this split?**
- Vercel: Best for frontend, global CDN, automatic deployments
- Render: Best for backend services that need long-running processes (Celery workers)

---

## 📋 Prerequisites

1. **GitHub Repository** with your code
2. **Vercel Account**: https://vercel.com
3. **Render Account**: https://render.com
4. **API Keys**: Gemini or OpenAI
5. **AWS S3**: For document storage

---

## 🚀 Part 1: Deploy Backend on Render

### Quick Deploy with Blueprint

1. Go to https://dashboard.render.com/blueprints
2. Click "New Blueprint Instance"
3. Connect to your GitHub repo
4. Render will detect `render.yaml` and create:
   - Backend service
   - Worker service
   - Agent service
   - Redis instance

5. Set environment variables in Render:
   ```
   GOOGLE_API_KEY=your_key
   AWS_ACCESS_KEY_ID=your_aws_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret
   AWS_BUCKET_NAME=your-bucket
   ```

6. **Copy the Backend URL** (e.g., `https://acd-backend.onrender.com`)

---

## 🚀 Part 2: Deploy Frontend on Vercel

### Method 1: Vercel Dashboard (Easiest)

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Configure Project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. **Environment Variables**:
   - Click "Environment Variables"
   - Add: `VITE_API_URL` = `https://acd-backend.onrender.com` (your backend URL from Render)

5. Click "Deploy"

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel

# Follow prompts:
# - Link to existing project or create new
# - Set build settings (auto-detected)
# - Add environment variable: VITE_API_URL

# Production deploy
vercel --prod
```

---

## 📝 Configure Environment Variables

### In Vercel Dashboard

1. Go to your project → Settings → Environment Variables
2. Add:
   ```
   Name: VITE_API_URL
   Value: https://acd-backend.onrender.com
   Environment: Production, Preview, Development
   ```

---

## 🔧 Update Frontend Code

The frontend needs to use the environment variable for API calls.

Already configured in `Home.jsx` and `Status.jsx`:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

---

## ✅ Post-Deployment Checklist

### Test the Deployment

1. Visit your Vercel URL (e.g., `https://your-app.vercel.app`)
2. Submit a test GitHub repository
3. Watch the status page update in real-time
4. Download the generated documentation

### Check Logs

- **Frontend**: Vercel Dashboard → Deployments → View Function Logs
- **Backend**: Render Dashboard → acd-backend → Logs
- **Worker**: Render Dashboard → acd-worker → Logs

---

## 🌐 Custom Domain (Optional)

### Add Domain to Vercel

1. Vercel Dashboard → Settings → Domains
2. Add your domain (e.g., `docs.yoursite.com`)
3. Update DNS records as shown by Vercel
4. SSL is automatic!

### Add Domain to Render Backend

1. Render Dashboard → acd-backend → Settings
2. Custom Domain → Add
3. Use subdomain like `api.yoursite.com`
4. Update frontend `VITE_API_URL` to use custom domain

---

## 💰 Pricing

### Vercel
- **Hobby (Free)**:
  - 100GB bandwidth/month
  - Unlimited deployments
  - Automatic SSL
  - Global CDN

- **Pro ($20/month)**:
  - 1TB bandwidth
  - More build minutes
  - Advanced analytics

### Render
- **Free Tier**:
  - 750 hours/month per service
  - Services sleep after 15min inactivity
  - 25MB Redis

- **Starter ($7/service/month)**:
  - No sleep
  - 512MB RAM
  - Better performance

**Total Free Tier**: $0/month  
**Total Production Ready**: ~$20-30/month (Vercel Hobby + Render Starter)

---

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push

Both Vercel and Render auto-deploy when you push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

- **Vercel**: Deploys frontend automatically
- **Render**: Deploys backend/worker/agent automatically

---

## 🐛 Troubleshooting

### CORS Errors

If you see CORS errors, check:
1. Backend has CORS middleware enabled ✓ (already added)
2. `VITE_API_URL` is set correctly in Vercel
3. Backend URL is accessible

### Backend Not Responding

- **Check**: Backend service is running on Render
- **Note**: Free tier sleeps after 15min - first request takes ~30s to wake up

### Worker Not Processing

- **Check**: Redis URL is correct in Render
- **Check**: Worker service is running
- **Check**: Worker logs for errors

### Agent Errors

- **Check**: API key is set in Render environment
- **Check**: Model name is correct (`gemini-2.5-flash`)

---

## 📊 Monitoring

### Vercel Analytics

1. Free analytics included
2. See: Page views, visitors, top pages
3. Upgrade to Pro for advanced analytics

### Render Metrics

1. Built-in metrics for each service
2. CPU, Memory, Network usage
3. Email alerts for failures

---

## 🚀 Alternative: All-Serverless Approach (Advanced)

### Deploy Backend as Vercel Serverless Functions

**Note**: This requires significant code refactoring:
- Convert FastAPI to serverless functions
- Use Vercel KV for Redis
- Use Vercel Cron for background tasks
- Agent would need to be serverless too

**Not recommended** for this project due to:
- Celery needs long-running processes
- LangGraph agent is stateful
- Complex async workflows

**Stick with Vercel (frontend) + Render (backend)** for best results!

---

## 📚 Resources

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Vite Environment Variables**: https://vitejs.dev/guide/env-and-mode.html

---

## ✨ Summary

**Deployment Stack:**
```
Frontend (Vercel)
     ↓ HTTPS
Backend (Render) ← Worker (Render) ← Agent (Render)
     ↓                    ↓
   Redis (Render)    S3 (AWS)
```

**Benefits:**
- ✅ Global CDN for frontend (Vercel)
- ✅ Automatic SSL everywhere
- ✅ Auto Git deployments
- ✅ Generous free tiers
- ✅ Production-ready in minutes
