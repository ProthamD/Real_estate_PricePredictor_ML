# 🎯 FRONTEND DEPLOYMENT GUIDE

## ✅ Backend is Live!

Your backend is deployed at: **https://real-estate-pricepredictor-ml.onrender.com**

---

## 🚀 Deploy Frontend - 2 Options

### ⚡ Option 1: Quick Deploy with gh-pages (Recommended - 5 minutes)

```powershell
# Navigate to frontend folder
cd "c:\Users\Protham Dey\ML Projects\Real_Estate\frontend"

# Install gh-pages
npm install --save-dev gh-pages

# Build the app (this will use your Render URL from .env.production)
npm run build

# Deploy to GitHub Pages
npx gh-pages -d out
```

**After deployment:**
1. Go to https://github.com/ProthamD/Real_estate_PricePredictor_ML/settings/pages
2. Source: Select `gh-pages` branch
3. Click **Save**
4. Wait 1-2 minutes

**Your app will be live at:**
```
https://prothamd.github.io/Real_estate_PricePredictor_ML/
```

---

### 🤖 Option 2: Automatic Deploy with GitHub Actions

The workflow is already configured! Just enable GitHub Pages:

1. Go to https://github.com/ProthamD/Real_estate_PricePredictor_ML/settings/pages
2. Source: Select **"GitHub Actions"**
3. The workflow will automatically build and deploy on every push to `main`

**To trigger it now:**
```powershell
cd "c:\Users\Protham Dey\ML Projects\Real_Estate"
git add .github/workflows/deploy.yml
git commit -m "Configure workflow with Render URL"
git push
```

---

## 🧪 Test Your Backend First

Before deploying frontend, let's verify your backend is working:

### Check if Backend is Running

Visit in browser: https://real-estate-pricepredictor-ml.onrender.com/

You should see: `"Real Estate Prediction API - Use /predict endpoint"`

### Test the Prediction Endpoint

```powershell
$body = @{
  CRIM = 0.00632; ZN = 18; INDUS = 2.31; CHAS = 0
  NOX = 0.538; RM = 6.575; AGE = 65.2; DIS = 4.09
  RAD = 1; TAX = 296; PTRATIO = 15.3; B = 396.9; LSTAT = 4.98
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://real-estate-pricepredictor-ml.onrender.com/predict" -Method Post -Body $body -ContentType "application/json"
```

**Expected response:**
```json
{
  "prediction": 25.128,
  "status": "success"
}
```

**If you get "Not Found":**
- Backend might still be deploying (check Render dashboard)
- First cold start can take 30-60 seconds
- Check Render logs for errors

---

## 📝 Environment Variables Setup

Your `.env.production` is already configured with:
```env
NEXT_PUBLIC_API_URL=https://real-estate-pricepredictor-ml.onrender.com
```

This will be used during the build process.

**Note:** `.env.production` is gitignored (correct for security), so the GitHub Actions workflow uses the hardcoded URL.

---

## 🔧 Troubleshooting

### Backend Returns "Not Found"

**Possible causes:**
1. **Still deploying** - Check Render dashboard for deployment status
2. **Root directory misconfigured** - Should be `Backend` (capital B)
3. **Build failed** - Check Render logs

**How to check Render logs:**
1. Go to https://dashboard.render.com/
2. Click your service: `real-estate-pricepredictor-ml`
3. Click "Logs" tab
4. Look for errors

**Common Render issues:**
- Missing `Model/pipeline_combined.joblib` - should be in your repo (it is!)
- Wrong start command - should be `gunicorn app:app --bind 0.0.0.0:$PORT`
- Python version mismatch - Render auto-detects from `requirements.txt`

### Frontend Build Fails

```powershell
# Clear cache and rebuild
cd frontend
rm -r -fo .next, out
npm run build
```

### GitHub Pages Shows 404

- Verify `basePath` in `frontend/next.config.ts` is `/Real_estate_PricePredictor_ML`
- Make sure you selected `gh-pages` branch in GitHub Pages settings
- Wait 2-3 minutes after enabling Pages

---

## ✅ Final Checklist

- [x] Backend deployed to Render
- [x] Backend URL: https://real-estate-pricepredictor-ml.onrender.com
- [x] `.env.production` configured
- [x] GitHub Actions workflow updated
- [ ] **Test backend /predict endpoint** ← DO THIS FIRST
- [ ] **Deploy frontend with gh-pages**
- [ ] **Enable GitHub Pages**
- [ ] **Test complete app**

---

## 🎉 Once Everything is Working

Your URLs:
- **Backend API**: https://real-estate-pricepredictor-ml.onrender.com
- **Frontend App**: https://prothamd.github.io/Real_estate_PricePredictor_ML/
- **GitHub Repo**: https://github.com/ProthamD/Real_estate_PricePredictor_ML

Test the full flow:
1. Visit your frontend URL
2. Fill in the form with test data
3. Click "Predict Price"
4. Should show predicted price!

---

## 📚 Next Steps

1. **Test backend now** (use PowerShell command above)
2. **Deploy frontend** (use Option 1 - gh-pages)
3. **Enable GitHub Pages**
4. **Verify full app works**

Good luck! 🚀
