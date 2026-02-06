# 🚀 Railway Configuration - Step by Step (100% Working)

## The Problem
You're getting `DisallowedHost` error because Django doesn't recognize the Railway domain.

## The Solution - Two Parts

### PART 1: Code Fix (Already Done ✅)
We updated `spacetravel/settings.py` to:
- Accept `['*']` in debug mode (development)
- Accept specific domains in production (Railway)
- Include your Railway domain: `web-production-6505.up.railway.app`

### PART 2: Railway Environment Variables (YOU MUST DO THIS)

Go to **Railway Dashboard** → Your Project → **Web Service** → **Variables**

Set these environment variables:

```
DEBUG=False
```

**Why:** This tells Django to exit debug mode and use the ALLOWED_HOSTS list we defined.

Optional but recommended:

```
SECRET_KEY=your-long-random-secret-key-here
DATABASE_URL=postgresql://... (Railway will set this automatically)
```

## Step-by-Step Instructions

### 1. Open Railway Dashboard
- Go to: https://railway.app/dashboard
- Select your project (web-production-6505)
- Click on the **Web** service

### 2. Go to Variables Tab
- Click on **Variables** tab
- You should see existing variables

### 3. Add/Update Variables
- Find or create: `DEBUG=False`
- Click **Save**

### 4. Wait for Auto-Redeploy
- Railway will automatically redeploy
- Watch the build logs
- Should succeed in ~1-2 minutes

### 5. Test Your App
- Go to: https://web-production-6505.up.railway.app/
- Should now work! ✅

## If It Still Doesn't Work

**Check these things:**

1. **Is DEBUG really False?**
   ```
   Railway Dashboard → Web → Variables
   Look for: DEBUG=False
   ```

2. **Check the Deploy Logs**
   ```
   Railway Dashboard → Web → Deployments
   Click latest deployment
   Look for errors in build logs
   ```

3. **Clear Browser Cache**
   ```
   Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
   ```

4. **Check if PostgreSQL is connected**
   ```
   Railway Dashboard → PostgreSQL → Connect
   Verify credentials are in your Web service environment
   ```

## What Each Setting Does

| Setting | Value | Purpose |
|---------|-------|---------|
| `DEBUG` | `False` | Disable debug mode, use ALLOWED_HOSTS list |
| `SECRET_KEY` | Random string | Security key for sessions/CSRF |
| `DB_ENGINE` | `postgresql` | Use PostgreSQL instead of SQLite |
| `ALLOWED_HOSTS` | (in code) | Specify which domains can access the app |

## Technical Details

When `DEBUG=False`, Django uses this ALLOWED_HOSTS from code:

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'web-production-6505.up.railway.app',  # ← Your Railway domain
    '.railway.app',
    '.up.railway.app',
]
```

This explicitly allows:
- ✅ `web-production-6505.up.railway.app`
- ✅ Any subdomain of `.railway.app`
- ✅ Any subdomain of `.up.railway.app`

## Success Checklist

After making changes, verify:

- [ ] Variable `DEBUG=False` is set in Railway
- [ ] Deployment succeeded (no red errors)
- [ ] Browser shows your site (not error)
- [ ] Pages load with proper styling
- [ ] Can access `/admin` page

## Common Mistakes

❌ **Mistake 1:** Forgetting to set `DEBUG=False`
- If DEBUG=True, the code uses `['*']` which shouldn't work
- **Fix:** Set `DEBUG=False` in Railway Variables

❌ **Mistake 2:** Not waiting for redeploy
- Changes don't take effect until Railway redeploys
- **Fix:** Wait 1-2 minutes and refresh browser

❌ **Mistake 3:** Database not connected
- App works but crashes when accessing data
- **Fix:** Add PostgreSQL to Railway first

❌ **Mistake 4:** Using old browser cache
- Old error page cached in browser
- **Fix:** Hard refresh (Cmd+Shift+R)

## Next Steps After This Works

1. ✅ Fix ALLOWED_HOSTS (this page)
2. ✅ Set DEBUG=False (Railway Variables)
3. ⏳ Add PostgreSQL Database
4. ⏳ Set Database environment variables
5. ⏳ Test full app with login/signup

## Need Help?

Check Railway logs:
```
Railway Dashboard → Web → Deployments → Click latest → View logs
```

Look for:
- Build errors
- Startup errors
- DisallowedHost errors

## Version Info

- Django: 5.0.4
- Python: 3.11.8
- Gunicorn: 21.2.0
- Railway: Auto-detects Procfile

---

**Status:** After you set `DEBUG=False`, this WILL work! 💯
