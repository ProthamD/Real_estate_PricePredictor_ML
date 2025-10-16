# 🔍 Backend Troubleshooting - Render Not Found

## ❌ Issue: Backend returns "Not Found"

Your backend at `https://real-estate-pricepredictor-ml.onrender.com` is returning 404.

The header `x-render-routing: no-server` indicates Render can't find your service.

---

## 🛠️ Fix: Check Render Configuration

### Step 1: Go to Render Dashboard

https://dashboard.render.com/

Find your service: `real-estate-pricepredictor-ml`

---

### Step 2: Check Service Status

Look at the top of the service page:

- **🟢 Live** = Service is running ✓
- **🟡 Building** = Still deploying (wait 2-5 minutes)
- **🔴 Build Failed** = Error in deployment (check logs)
- **⚫ Deploy Failed** = Error starting service (check logs)

---

### Step 3: Verify Configuration

Click **"Settings"** tab and verify:

#### Repository Settings
```
Repository: ProthamD/Real_estate_PricePredictor_ML ✓
Branch: main ✓
```

#### Build & Deploy Settings
```
Root Directory: Backend     ← MUST BE EXACTLY THIS (capital B)
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
```

**⚠️ Common Mistake:**
- ❌ Root Directory: `backend` (lowercase)
- ❌ Root Directory: `/Backend` (with leading slash)
- ❌ Root Directory: `Backend/` (with trailing slash)
- ✅ Root Directory: `Backend` (capital B, no slashes)

---

### Step 4: Check Logs

Click **"Logs"** tab and look for:

#### Good Signs ✅
```
==> Installing dependencies from requirements.txt
Successfully installed Flask...
==> Starting service...
Pipeline exists: True
Combined pipeline loaded successfully
[INFO] Starting gunicorn...
```

#### Bad Signs ❌

**Build Errors:**
```
ERROR: Could not find requirements.txt
ERROR: No such file or directory: 'requirements.txt'
```
**Fix:** Root Directory is wrong. Set to `Backend`

**Model Loading Errors:**
```
FileNotFoundError: [Errno 2] No such file or directory: '../Model/pipeline_combined.joblib'
```
**Fix:** Check that `Model/pipeline_combined.joblib` is in your GitHub repo

**Port Binding Errors:**
```
gunicorn: command not found
```
**Fix:** Check `requirements.txt` includes `gunicorn==21.2.0`

---

### Step 5: Check Files on GitHub

Verify these files exist in your repo:

https://github.com/ProthamD/Real_estate_PricePredictor_ML

Required files:
- ✅ `Backend/app.py`
- ✅ `Backend/requirements.txt`
- ✅ `Model/pipeline_combined.joblib` (~14MB)

---

## 🔄 Fix Steps

### If Root Directory is Wrong:

1. Go to Render → Your Service → **Settings**
2. Find **Root Directory**
3. Change to: `Backend` (capital B, no slashes)
4. Click **Save Changes**
5. Render will automatically redeploy (wait 3-5 minutes)

### If Build Failed:

1. Check Render **Logs** for specific error
2. Common fixes:
   - Ensure `Backend/requirements.txt` exists in GitHub
   - Ensure `Model/pipeline_combined.joblib` is committed to Git
   - Check Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
3. Click **Manual Deploy** → **Deploy latest commit**

### If Still Having Issues:

**Redeploy from scratch:**

1. Delete the current Render service
2. Create new Web Service
3. Connect GitHub repo: `ProthamD/Real_estate_PricePredictor_ML`
4. Configure:
   ```
   Name: real-estate-pricepredictor-ml
   Root Directory: Backend
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
   ```
5. Click **Create Web Service**

---

## ✅ How to Test When Fixed

Once Render shows **🟢 Live**, test:

```powershell
# Test root endpoint
Invoke-RestMethod -Uri "https://real-estate-pricepredictor-ml.onrender.com/"
```

Should return: `"Real Estate Prediction API - Use /predict endpoint"`

```powershell
# Test prediction
$body = @{
  CRIM = 0.00632; ZN = 18; INDUS = 2.31; CHAS = 0
  NOX = 0.538; RM = 6.575; AGE = 65.2; DIS = 4.09
  RAD = 1; TAX = 296; PTRATIO = 15.3; B = 396.9; LSTAT = 4.98
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://real-estate-pricepredictor-ml.onrender.com/predict" -Method Post -Body $body -ContentType "application/json"
```

Should return:
```json
{
  "prediction": 25.128,
  "status": "success"
}
```

---

## 📋 Quick Checklist

Go through these on Render dashboard:

- [ ] Service status is **🟢 Live** (not building/failed)
- [ ] Root Directory is exactly: `Backend`
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
- [ ] Logs show "Pipeline exists: True"
- [ ] Logs show "Combined pipeline loaded successfully"
- [ ] No errors in logs

---

## 🆘 What to Check in Logs

**Search for these in Render logs:**

1. `"Pipeline exists:"` - Should be `True`
2. `"Combined pipeline loaded"` - Should be `successfully`
3. `"Starting gunicorn"` - Server should start
4. `"Listening at"` - Should show port binding

**If you see:**
- `"Pipeline exists: False"` → Model file not found
- `"Error loading pipeline"` → Check model file in GitHub
- `"command not found"` → Check requirements.txt
- `"No such file or directory"` → Check Root Directory setting

---

## 💡 Most Likely Issues

1. **Root Directory wrong** (85% of cases)
   - Fix: Set to `Backend` exactly
   
2. **Model file missing** (10% of cases)
   - Fix: Ensure `Model/pipeline_combined.joblib` is in Git
   
3. **Still deploying** (5% of cases)
   - Fix: Wait 2-5 minutes, check status

---

Once you've checked these settings and redeployed, test again. Let me know what you see in the Render logs!
