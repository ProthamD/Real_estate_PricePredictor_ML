# 🏗️ Project Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         YOUR PROJECT                             │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐            ┌──────────────────┐
│   GitHub Pages   │            │      Render      │
│   (Frontend)     │◄──────────►│    (Backend)     │
│                  │   HTTPS    │                  │
│  Next.js Static  │            │  Flask + Model   │
└──────────────────┘            └──────────────────┘
         │                               │
         │                               │
         ▼                               ▼
    User Browser                   ML Pipeline
    - React Form                   - Preprocessing
    - Chakra UI                    - RandomForest
    - Axios HTTP                   - Prediction
```

## Data Flow

```
1. User visits GitHub Pages
   https://YOUR_USERNAME.github.io/Real_Estate/

2. User fills form with 13 housing features
   (CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT)

3. Frontend sends POST to Render backend
   POST https://YOUR-BACKEND-URL.onrender.com/predict
   Content-Type: application/json
   Body: { "CRIM": 0.00632, "ZN": 18, ... }

4. Backend processes request
   a. Flask receives JSON
   b. Converts to pandas DataFrame
   c. Passes through pipeline:
      - SimpleImputer (median strategy)
      - StandardScaler (normalization)
      - RandomForestRegressor (prediction)

5. Backend returns prediction
   Response: { "prediction": 25.128, "status": "success" }

6. Frontend displays result
   "Predicted Price: $25.128k"
```

## File Structure

```
Real_Estate/
│
├── Backend/                    # Flask API
│   ├── app.py                 # Main Flask app ✓ READY
│   ├── requirements.txt       # Python dependencies ✓ READY
│   ├── test_pipeline.py       # Local test script
│   └── test_api.py            # API endpoint test
│
├── Model/                      # ML Artifacts
│   ├── pipeline_combined.joblib    # ⚠️ MUST be in Git (14MB)
│   ├── ESTATE_PRICE_CALCULATOR.joblib  (old, not used)
│   ├── save_combined_pipeline.py   # Pipeline builder
│   ├── REdata.csv             # Training data
│   └── *.ipynb                # Jupyter notebooks
│
├── frontend/                   # Next.js App
│   ├── pages/
│   │   └── index.js           # Main page with form ✓ UPDATED
│   ├── next.config.ts         # Static export config ✓ READY
│   ├── package.json           # Node dependencies
│   ├── .env.production        # 🔴 TODO: Add your Render URL
│   └── .env.local             # Local dev config
│
├── .github/
│   └── workflows/
│       └── deploy.yml         # Auto-deploy to GitHub Pages
│
├── DEPLOYMENT.md              # 📘 Full deployment guide
├── QUICKSTART.md              # ⚡ Quick commands
├── README_DEPLOYMENT.md       # 🎯 What to do next
└── .gitignore                 # Git ignore rules
```

## Technology Stack

### Backend (Render)
- **Runtime**: Python 3.11+
- **Web Framework**: Flask 2.2.5
- **WSGI Server**: Gunicorn 21.2.0
- **ML Framework**: scikit-learn 1.6.1
- **Data Processing**: pandas 2.2.3, numpy 1.26.4
- **Model Format**: joblib pipeline

### Frontend (GitHub Pages)
- **Framework**: Next.js 15.3.3
- **UI Library**: Chakra UI 2.8.2
- **Form Handling**: react-hook-form 7.57.0
- **HTTP Client**: axios 1.9.0
- **Language**: TypeScript/JavaScript (React 19)
- **Styling**: TailwindCSS 4

### Deployment
- **Backend Host**: Render (free tier)
- **Frontend Host**: GitHub Pages (free)
- **CI/CD**: GitHub Actions
- **Version Control**: Git + GitHub

## Environment Variables

### Frontend
```env
NEXT_PUBLIC_API_URL=https://YOUR-BACKEND-URL.onrender.com
```
- Used in `pages/index.js` for API calls
- Must start with `NEXT_PUBLIC_` to be accessible in browser
- Set in `.env.production` for GitHub Pages
- Set in `.env.local` for local development

### Backend
No environment variables required for basic deployment.
Optional: Add for production (secrets, logging, etc.)

## Security Considerations

### Current State (Development)
- ✅ CORS enabled for all origins
- ✅ No API keys required
- ✅ No sensitive data in requests
- ✅ Model file in public repo (OK - it's just weights)

### Production Recommendations
1. **Restrict CORS** in `Backend/app.py`:
   ```python
   CORS(app, origins=["https://YOUR_USERNAME.github.io"])
   ```

2. **Add Rate Limiting**:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["100 per hour"])
   ```

3. **Add Input Validation**:
   - Check value ranges
   - Reject malformed requests
   - Log suspicious activity

4. **Monitor Usage**:
   - Set up Render logging
   - Track prediction counts
   - Alert on errors

## Performance Notes

### Backend (Render Free Tier)
- **Cold Start**: 30-60 seconds (after 15 min inactivity)
- **Warm Response**: ~200-500ms
- **Memory**: ~150MB (model + Flask)
- **Concurrent Requests**: Limited on free tier

### Frontend (GitHub Pages)
- **Initial Load**: ~1-2s (static files)
- **CDN**: GitHub's global CDN
- **Caching**: Aggressive (great for static sites)

### Model
- **Size**: ~14MB (RandomForestRegressor)
- **Inference Time**: ~10-50ms per prediction
- **Features**: 13 input features
- **Output**: Single float (house price in $1000s)

## Monitoring & Debugging

### Backend Logs (Render)
```
Dashboard → Your Service → Logs

Look for:
- "Pipeline exists: True" (startup)
- "Combined pipeline loaded successfully"
- Request logs with status codes
```

### Frontend Debugging
```javascript
// Open browser console (F12)
// Check Network tab for API calls
// Look for:
// - Request URL (should be Render backend)
// - Status code (200 = success)
// - Response body (prediction value)
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| CORS error | Origin mismatch | Check CORS config in `app.py` |
| 500 error | Model loading failed | Check pipeline_combined.joblib in Git |
| Slow response | Cold start | Wait 30-60s, or upgrade Render |
| 404 on Pages | Wrong basePath | Match `next.config.ts` to repo name |
| Build fails | Missing deps | Check `requirements.txt` syntax |

## Cost Breakdown

| Service | Tier | Cost | Limits |
|---------|------|------|--------|
| Render | Free | $0 | 750 hrs/month, sleeps after 15min |
| GitHub Pages | Free | $0 | 1GB storage, 100GB bandwidth |
| **Total** | - | **$0/month** | Perfect for demo/portfolio |

### Upgrade Path (Optional)
- **Render Starter**: $7/month (no sleep, faster, custom domain)
- **Vercel Pro**: $20/month (better frontend performance)

## Next Steps After Deployment

1. **Test thoroughly** with various inputs
2. **Share your project** (add to portfolio)
3. **Monitor logs** for first week
4. **Add features**:
   - Input presets (common house types)
   - Prediction history
   - Feature importance visualization
   - Comparison with market data

5. **Optimize**:
   - Add caching for common predictions
   - Reduce model size (pruning)
   - Add frontend loading states

---

**You now have a production-ready ML deployment!** 🎉

See `README_DEPLOYMENT.md` for exact steps to deploy.
