# Django Chat App - Render Deployment

## Files Created for Deployment:

1. **Dockerfile** - Docker container configuration
2. **Procfile** - Process file for Render
3. **build.sh** - Build script for Render
4. **.dockerignore** - Files to exclude from Docker build

## Deploy to Render.com:

### Option 1: Using Dockerfile (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Create New Web Service on Render:**
   - Go to https://render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** `django-chat-app`
     - **Environment:** `Docker`
     - **Region:** Choose nearest
     - **Branch:** `main`
     - **Dockerfile Path:** `./Dockerfile`
     - **Instance Type:** Free or Starter

3. **Environment Variables:**
   Add these in Render dashboard:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app.onrender.com
   STATIC_CURRENT_USER_EMAIL=default@gmail.com
   ```

### Option 2: Using Build Script

If you prefer native Python environment:

1. In Render dashboard:
   - **Environment:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn chatserver.wsgi:application`

## Important Notes:

- **Database:** SQLite won't persist on Render (ephemeral storage). For production, upgrade to PostgreSQL.
- **Media Files:** Uploaded images won't persist. Use cloud storage (AWS S3, Cloudinary) for production.
- **ALLOWED_HOSTS:** Update `settings.py` with your Render domain.

## Local Docker Testing:

```bash
# Build the image
docker build -t django-chat .

# Run the container
docker run -p 8000:8000 django-chat
```

Visit http://localhost:8000/home/
