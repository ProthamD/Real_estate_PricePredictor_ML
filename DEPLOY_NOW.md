# ⚡ DEPLOY FRONTEND NOW - 3 Commands

## Your Backend is Ready! 
✅ https://real-estate-pricepredictor-ml.onrender.com

---

## 🚀 Deploy Frontend (Copy & Paste)

```powershell
# Step 1: Go to frontend folder
cd "c:\Users\Protham Dey\ML Projects\Real_Estate\frontend"

# Step 2: Install gh-pages
npm install --save-dev gh-pages

# Step 3: Build and deploy
npm run build
npx gh-pages -d out
```

**After running above commands:**

1. Go to: https://github.com/ProthamD/Real_estate_PricePredictor_ML/settings/pages
2. Under "Source", select: **`gh-pages` branch**
3. Click **Save**
4. Wait 2 minutes

---

## 🎉 Your App Will Be Live At:

```
https://prothamd.github.io/Real_estate_PricePredictor_ML/
```

---

## 🧪 Test Backend First (Optional)

```powershell
# Test if backend is responding
Invoke-RestMethod -Uri "https://real-estate-pricepredictor-ml.onrender.com/"
```

Should show: `"Real Estate Prediction API - Use /predict endpoint"`

**If "Not Found"**: Backend might still be cold-starting (wait 30 seconds and try again)

---

## 📋 What Happens When You Deploy

1. `npm run build` creates static HTML/CSS/JS in `out/` folder
2. `npx gh-pages -d out` pushes the `out/` folder to `gh-pages` branch
3. GitHub Pages serves the static site from `gh-pages` branch
4. Your frontend calls your Render backend at: `https://real-estate-pricepredictor-ml.onrender.com`

---

## ✅ That's It!

Just run those 3 commands and enable GitHub Pages. You're done! 🎊
