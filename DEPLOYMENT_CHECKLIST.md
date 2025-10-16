# ✅ Deployment Checklist

Use this checklist to track your deployment progress!

## Pre-Deployment (Local)

- [ ] All code changes committed to Git
- [ ] `Model/pipeline_combined.joblib` exists (~14MB file)
- [ ] Tested `Backend/test_pipeline.py` - prediction works locally
- [ ] Created GitHub repository
- [ ] Pushed all files to GitHub

## Backend Deployment (Render)

- [ ] Signed up for Render account
- [ ] Created new Web Service
- [ ] Connected GitHub repository
- [ ] Configured service settings:
  - [ ] Root Directory: `Backend`
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
  - [ ] Instance Type: Free
- [ ] Deployment succeeded (check logs)
- [ ] Copied backend URL (e.g., `https://real-estate-api-xxxx.onrender.com`)
- [ ] Tested `/predict` endpoint with curl/PowerShell

Test command:
```powershell
$body = @{CRIM=0.00632;ZN=18;INDUS=2.31;CHAS=0;NOX=0.538;RM=6.575;AGE=65.2;DIS=4.09;RAD=1;TAX=296;PTRATIO=15.3;B=396.9;LSTAT=4.98} | ConvertTo-Json
Invoke-RestMethod -Uri "https://YOUR-URL.onrender.com/predict" -Method Post -Body $body -ContentType "application/json"
```

Expected: `{"prediction": 25.128, "status": "success"}`

## Frontend Configuration

- [ ] Updated `frontend/.env.production` with Render backend URL
- [ ] Verified `frontend/next.config.ts` basePath matches repo name
- [ ] Committed and pushed changes

## Frontend Deployment (GitHub Pages)

Choose ONE method:

### Method A: gh-pages package

- [ ] Installed gh-pages: `npm install --save-dev gh-pages`
- [ ] Added deploy script to `package.json`:
  ```json
  "scripts": {
    "deploy": "npm run build && gh-pages -d out"
  }
  ```
- [ ] Ran: `npm run deploy`
- [ ] Enabled GitHub Pages in repo settings (source: gh-pages branch)

### Method B: GitHub Actions (automated)

- [ ] Workflow file exists: `.github/workflows/deploy.yml`
- [ ] Updated API URL in workflow or added as GitHub secret
- [ ] Pushed to main branch (triggers auto-deploy)
- [ ] Enabled GitHub Pages in repo settings (source: GitHub Actions)

## Verification

- [ ] Backend URL is accessible (visit in browser - should show API message)
- [ ] Frontend URL is accessible: `https://YOUR_USERNAME.github.io/Real_Estate/`
- [ ] Form loads correctly
- [ ] Submitted test data (use values above)
- [ ] Received prediction result
- [ ] Checked browser console for errors (F12 → Console)
- [ ] Verified Network tab shows successful API call

## Post-Deployment (Optional)

- [ ] Added custom domain (if desired)
- [ ] Restricted CORS to GitHub Pages origin only
- [ ] Set up monitoring/logging
- [ ] Added rate limiting
- [ ] Created README.md with live demo links
- [ ] Shared project (portfolio, LinkedIn, etc.)

## Troubleshooting Done

If you encountered issues, check off what you fixed:

- [ ] Backend: Model file missing → Re-pushed pipeline_combined.joblib
- [ ] Frontend: 404 error → Fixed basePath in next.config.ts
- [ ] API: CORS error → Updated CORS settings in app.py
- [ ] API: Slow first request → Expected (free tier cold start)
- [ ] Build: Dependencies failed → Fixed requirements.txt/package.json
- [ ] GitHub Pages: Not updating → Cleared cache, checked deployment logs

## Final Status

**Backend Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Deployed ✓

**Frontend Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Deployed ✓

**Testing Status**: ⬜ Not Tested | ⬜ Tested ✓

---

## Your Live URLs

**Backend API**: `https://___________________.onrender.com`

**Frontend App**: `https://_____________________.github.io/Real_Estate/`

---

## Important Files to Keep Track Of

| File | Purpose | Status |
|------|---------|--------|
| `Backend/requirements.txt` | Python deps | ✅ Ready |
| `Backend/app.py` | Flask API | ✅ Ready |
| `Model/pipeline_combined.joblib` | ML model | ⚠️ Check Git |
| `frontend/.env.production` | API URL | 🔴 Update needed |
| `frontend/next.config.ts` | Export config | ✅ Ready |

---

## Quick Links

- 📘 Full Guide: `DEPLOYMENT.md`
- ⚡ Quick Commands: `QUICKSTART.md`
- 🏗️ Architecture: `ARCHITECTURE.md`
- 🎯 Next Steps: `README_DEPLOYMENT.md`

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **GitHub Pages**: https://docs.github.com/en/pages
- **Next.js Export**: https://nextjs.org/docs/app/building-your-application/deploying/static-exports

---

**Good luck with your deployment! 🚀**

Check off items as you complete them. Once all ✓ marks are done, your app is live!
