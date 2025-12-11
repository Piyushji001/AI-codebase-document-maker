# Deployment Summary

Quick reference for deploying the Autonomous Codebase Documenter.

## 🎯 Recommended Strategy: 100% Free Tier

We use a **hybrid service** approach to fit everything into free tiers.

| Service | Platform | Type | Cost |
|---------|----------|------|------|
| **Backend + Worker** | Render | Web Service | Free |
| **AI Agent** | Render | Web Service | Free |
| **Redis** | Render | Redis | Free |
| **Frontend** | Vercel | Static Site | Free |

**Total Cost: $0/month**

---

## 🚀 Quick Start

### 1. Backend & Agent (Render)
Use the `render.yaml` Blueprint:
1. Push code to GitHub
2. Go to Render -> Blueprints -> New Instance
3. Connect Repo -> Apply
4. Set Env Vars (API Keys, AWS Creds)

### 2. Frontend (Vercel)
1. Go to Vercel -> New Project
2. Import Repo
3. Set Root Directory: `frontend`
4. Set Env Var: `VITE_API_URL` = (Your Render Backend URL)
5. Deploy

---

## 🔑 Required Environment Variables

### Render (Backend Service)
```bash
REDIS_URL=redis://... (Internal)
GOOGLE_API_KEY=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_BUCKET_NAME=...
AGENT_URL=https://acd-agent-xxx.onrender.com
```

### Vercel (Frontend)
```bash
VITE_API_URL=https://acd-backend-xxx.onrender.com
```

---

## 📄 Documentation
- **Render Guide**: `DEPLOY_RENDER.md`
- **Vercel Guide**: `DEPLOY_VERCEL.md`
