# Django Chat App - PythonAnywhere Deployment Guide

## Step 1: Upload Your Code

### Option A: Using Git (Recommended)
1. Push your code to GitHub
2. On PythonAnywhere, open a Bash console
3. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

### Option B: Upload Files Directly
1. Go to Files tab
2. Upload your project files
3. Or use the "Upload a file" button

## Step 2: Create Virtual Environment

In the Bash console:
```bash
cd ~/your-project-folder
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 3: Configure Web App

1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration** (not Django wizard)
4. Select **Python 3.10**

## Step 4: Configure WSGI File

Click on the WSGI configuration file link and replace content with:

```python
import os
import sys

# Add your project directory to the sys.path
project_home = '/home/yourusername/your-project-folder'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'chatserver.settings'

# Activate virtual environment
activate_this = '/home/yourusername/your-project-folder/venv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace:** `yourusername` and `your-project-folder` with your actual paths

## Step 5: Configure Virtualenv Path

In the Web tab:
- **Virtualenv:** `/home/yourusername/your-project-folder/venv`

## Step 6: Configure Static Files

In the Web tab, add static files mapping:

| URL          | Directory                                              |
|--------------|--------------------------------------------------------|
| /static/     | /home/yourusername/your-project-folder/static         |
| /media/      | /home/yourusername/your-project-folder/media          |

## Step 7: Update Django Settings

Edit `chatserver/settings.py`:

```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Step 8: Collect Static Files & Migrate

In Bash console:
```bash
cd ~/your-project-folder
source venv/bin/activate
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser  # Optional: create admin user
```

## Step 9: Reload Web App

1. Go to Web tab
2. Click **Reload yourusername.pythonanywhere.com** button

## Step 10: Test Your App

Visit: `https://yourusername.pythonanywhere.com/home/`

## Troubleshooting

### Check Error Logs
- Go to Web tab
- Click on error log and server log links
- Look for Python errors

### Common Issues:

1. **ImportError: No module named 'chatapp'**
   - Check WSGI file paths
   - Ensure virtual environment is activated
   - Verify `sys.path` includes project directory

2. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check static files mapping in Web tab
   - Verify STATIC_ROOT is set

3. **Database errors**
   - Run migrations: `python manage.py migrate`
   - Check database file permissions

4. **Media uploads not working**
   - Check media directory exists: `mkdir -p media/chat_images`
   - Set permissions: `chmod 755 media`

## Update Deployed Code

When you make changes:

```bash
# In Bash console
cd ~/your-project-folder
git pull  # If using Git
source venv/bin/activate
python manage.py collectstatic --noinput
python manage.py migrate
```

Then reload the web app from the Web tab.

## Important Notes:

- **Free tier limitations:** 
  - CPU seconds limited
  - One web app only
  - Custom domains require paid plan
  
- **Database:** SQLite works fine on PythonAnywhere (persistent storage)

- **Media files:** Uploads persist (unlike Render free tier)

- **Scheduled tasks:** Use the Schedule tab for periodic tasks

- **HTTPS:** Automatically enabled for pythonanywhere.com domains

## Environment Variables (Optional)

For sensitive data, use PythonAnywhere's environment variables:

1. Go to Web tab
2. Scroll to "Environment variables" section
3. Add:
   ```
   SECRET_KEY=your-secret-key-here
   STATIC_CURRENT_USER_EMAIL=default@gmail.com
   ```

4. Access in settings.py:
   ```python
   SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
   STATIC_CURRENT_USER_EMAIL = os.environ.get('STATIC_CURRENT_USER_EMAIL', 'wow@gmail.com')
   ```

## Complete Bash Commands Summary:

```bash
# Clone or navigate to project
cd ~/your-project-folder

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create media directory
mkdir -p media/chat_images

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

Your app will be live at: `https://yourusername.pythonanywhere.com/home/`
