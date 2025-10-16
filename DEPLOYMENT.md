# 🚀 Deployment Guide: Real Estate Price Predictor

This guide walks you through deploying the Real Estate Price Predictor with:
- **Backend (Flask API)**: Hosted on Render
- **Frontend (Next.js)**: Hosted on GitHub Pages

---

## 📋 Prerequisites

1. **GitHub account** (for version control and GitHub Pages)
2. **Render account** (free tier available at [render.com](https://render.com))
3. Git installed on your machine

---

## 🔧 Part 1: Prepare Your Repository

### 1.1 Initialize Git (if not already done)

```bash
cd "c:\Users\Protham Dey\ML Projects\Real_Estate"
git init
git add .
git commit -m "Initial commit: Real Estate Price Predictor"
```

### 1.2 Push to GitHub

1. Create a new repository on GitHub (e.g., `real-estate-predictor`)
2. Push your code:

```bash
git remote add origin https://github.com/YOUR_USERNAME/real-estate-predictor.git
git branch -M main
git push -u origin main
```

---

## 🐍 Part 2: Deploy Backend to Render

### 2.1 What's Already Prepared

✅ `Backend/requirements.txt` - All Python dependencies with pinned versions
✅ `Backend/app.py` - Flask API with CORS enabled
✅ `Model/pipeline_combined.joblib` - Combined preprocessing + model pipeline

### 2.2 Deploy on Render

1. **Go to [Render Dashboard](https://dashboard.render.com/)**

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your `real-estate-predictor` repo

3. **Configure the Service**

   | Setting | Value |
   |---------|-------|
   | **Name** | `real-estate-api` (or any name) |
   | **Region** | Choose closest to you |
   | **Branch** | `main` |
   | **Root Directory** | `Backend` |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT` |
   | **Instance Type** | `Free` |

4. **Environment Variables** (optional)
   - Add any secrets if needed (none required for basic setup)

5. **Click "Create Web Service"**

   Render will:
   - Install dependencies from `requirements.txt`
   - Start your Flask app with Gunicorn
   - Provide a URL like: `https://real-estate-api-xxxx.onrender.com`

### 2.3 Test Your Backend

Once deployed, test the `/predict` endpoint:

```powershell
# PowerShell test
$body = @{
  CRIM = 0.00632
  ZN = 18
  INDUS = 2.31
  CHAS = 0
  NOX = 0.538
  RM = 6.575
  AGE = 65.2
  DIS = 4.09
  RAD = 1
  TAX = 296
  PTRATIO = 15.3
  B = 396.9
  LSTAT = 4.98
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://YOUR-BACKEND-URL.onrender.com/predict" -Method Post -Body $body -ContentType "application/json"
```

Expected response:
```json
{
  "prediction": 25.128,
  "status": "success"
}
```

---

## 🌐 Part 3: Deploy Frontend to GitHub Pages

### 3.1 Configure Next.js for Static Export

GitHub Pages requires static HTML files. Update your Next.js config:

**Edit `frontend/next.config.ts`:**

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',  // Enable static HTML export
  basePath: '/real-estate-predictor',  // Replace with your repo name
  assetPrefix: '/real-estate-predictor/',
  images: {
    unoptimized: true,  // GitHub Pages doesn't support Next.js Image Optimization
  },
};

export default nextConfig;
```

### 3.2 Create Environment File

Create `frontend/.env.production`:

```env
NEXT_PUBLIC_API_URL=https://YOUR-BACKEND-URL.onrender.com
```

**⚠️ Important:** Replace `YOUR-BACKEND-URL` with your actual Render backend URL!

### 3.3 Build the Frontend

```powershell
cd frontend
npm install
npm run build
```

This creates an `out/` folder with static files.

### 3.4 Deploy to GitHub Pages

**Option A: Manual Deployment**

1. Install `gh-pages`:
   ```powershell
   npm install --save-dev gh-pages
   ```

2. Add deploy script to `frontend/package.json`:
   ```json
   "scripts": {
     "dev": "next dev --turbopack",
     "build": "next build",
     "start": "next start",
     "lint": "next lint",
     "deploy": "npm run build && gh-pages -d out"
   }
   ```

3. Deploy:
   ```powershell
   npm run deploy
   ```

**Option B: GitHub Actions (Automated)**

Create `.github/workflows/deploy.yml` in your repo root:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        working-directory: ./frontend
        run: npm install
        
      - name: Build Next.js app
        working-directory: ./frontend
        env:
          NEXT_PUBLIC_API_URL: https://YOUR-BACKEND-URL.onrender.com
        run: npm run build
        
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/out
```

### 3.5 Enable GitHub Pages

1. Go to your GitHub repo → **Settings** → **Pages**
2. Under "Source", select `gh-pages` branch
3. Click **Save**

Your site will be available at:
```
https://YOUR_USERNAME.github.io/real-estate-predictor/
```

---

## ✅ Part 4: Verify Deployment

### Test the Complete Flow

1. **Visit your GitHub Pages URL**
2. **Fill in the form** with sample data:
   - CRIM: 0.00632
   - ZN: 18
   - INDUS: 2.31
   - CHAS: 0
   - NOX: 0.538
   - RM: 6.575
   - AGE: 65.2
   - DIS: 4.09
   - RAD: 1
   - TAX: 296
   - PTRATIO: 15.3
   - B: 396.9
   - LSTAT: 4.98

3. **Click "Predict Price"**
4. You should see: **"Predicted Price: $25.128k"** (or similar)

---

## 🔧 Troubleshooting

### Backend Issues

**Problem**: "Application error" on Render
- Check Render logs: Dashboard → Your Service → Logs
- Common issues:
  - Missing `Model/pipeline_combined.joblib` - ensure it's committed to Git
  - Wrong start command - should be `gunicorn app:app --bind 0.0.0.0:$PORT`

**Problem**: CORS errors
- Backend has CORS enabled for all origins (`CORS(app)`)
- For production, restrict origins in `app.py`:
  ```python
  CORS(app, origins=["https://YOUR_USERNAME.github.io"])
  ```

### Frontend Issues

**Problem**: 404 on GitHub Pages
- Ensure `basePath` in `next.config.ts` matches your repo name
- Check GitHub Pages is enabled with `gh-pages` branch

**Problem**: API calls fail
- Check `NEXT_PUBLIC_API_URL` is set correctly
- Open browser DevTools → Network tab to see actual request URL
- Verify Render backend is running (visit backend URL directly)

**Problem**: "Failed to fetch prediction"
- Backend might be sleeping (Render free tier sleeps after inactivity)
- First request may take 30-60 seconds to wake up

---

## 🎯 Next Steps

### Production Improvements

1. **Security**
   - Restrict CORS to specific origin (your GitHub Pages URL)
   - Add rate limiting to prevent abuse
   - Use environment variables for sensitive config

2. **Performance**
   - Upgrade Render to paid tier (no sleep, faster cold starts)
   - Add caching for common predictions
   - Consider CDN for frontend assets

3. **Monitoring**
   - Add logging to track predictions
   - Set up Render health checks
   - Monitor error rates

4. **Features**
   - Add prediction history
   - Show feature importance visualization
   - Add input validation with helpful hints

---

## 📝 Summary

✅ Backend deployed on Render with Gunicorn + Flask  
✅ Model pipeline loaded from `pipeline_combined.joblib`  
✅ Frontend deployed on GitHub Pages as static site  
✅ Frontend calls backend API via environment variable  
✅ CORS enabled for cross-origin requests  

**Your app is now live!** 🎉

Backend API: `https://YOUR-BACKEND-URL.onrender.com`  
Frontend: `https://YOUR_USERNAME.github.io/real-estate-predictor/`

---

## 🆘 Need Help?

- **Render Docs**: https://render.com/docs
- **Next.js Static Export**: https://nextjs.org/docs/app/building-your-application/deploying/static-exports
- **GitHub Pages**: https://docs.github.com/en/pages
