# 🚀 Quick Deployment Commands

## Step 1: Push to GitHub

```powershell
cd "c:\Users\Protham Dey\ML Projects\Real_Estate"
git add .
git commit -m "Ready for deployment"
git push origin main
```

## Step 2: Deploy Backend to Render

1. Go to https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Connect GitHub repo: `real-estate-predictor`
4. Settings:
   - **Root Directory**: `Backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Click "Create Web Service"
6. Copy your backend URL (e.g., `https://real-estate-api-xxxx.onrender.com`)

## Step 3: Configure Frontend for GitHub Pages

Update `frontend/.env.production`:
```env
NEXT_PUBLIC_API_URL=https://YOUR-BACKEND-URL.onrender.com
```

Update `frontend/next.config.ts`:
```typescript
const nextConfig: NextConfig = {
  output: 'export',
  basePath: '/real-estate-predictor',  // Your repo name
  assetPrefix: '/real-estate-predictor/',
  images: { unoptimized: true },
};
```

## Step 4: Build and Deploy Frontend

```powershell
cd frontend
npm install
npm install --save-dev gh-pages

# Add to package.json scripts:
# "deploy": "npm run build && gh-pages -d out"

npm run deploy
```

## Step 5: Enable GitHub Pages

1. GitHub repo → Settings → Pages
2. Source: `gh-pages` branch
3. Save

## Done! 🎉

Your app is live at:
- Backend: `https://YOUR-BACKEND-URL.onrender.com`
- Frontend: `https://YOUR_USERNAME.github.io/real-estate-predictor/`
