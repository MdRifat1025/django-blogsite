# Quick Start Guide - Blog Site

## Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

### Step 2: Setup Environment

```bash
# Copy environment file
cp .env.example .env

# The default settings work for development
# No changes needed for quick start!
```

### Step 3: Initialize Database

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Load sample data (recommended for testing)
python setup_sample_data.py
```

### Step 4: Run the Server

```bash
python manage.py runserver
```

### Step 5: Access the Application

Open your browser and visit:
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

### Default Login Credentials

After running `setup_sample_data.py`, you can login with:

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Author Account:**
- Username: `john_author`
- Password: `password123`

**Reader Account:**
- Username: `reader`
- Password: `password123`

## Testing the Features

### As an Author

1. **Login** with author credentials
2. **Create a blog**: Click "Create Blog" in navigation
3. **Fill in details**: Title, content, category, and optional image
4. **Publish**: Click "Create Blog" button
5. **Edit/Delete**: View your blog and use edit/delete buttons

### As a Reader

1. **Browse blogs**: View all blogs on home page
2. **Filter blogs**: Use search and filter options
3. **Read blog**: Click on any blog to read full content
4. **Rate blog**: Click "Rate this Blog" button
5. **Add to favorites**: Click "Add to Favorites" button
6. **View favorites**: Click "Favorites" in navigation

### As an Admin

1. **Login** to admin panel: http://127.0.0.1:8000/admin/
2. **Manage users**: Add, edit, or remove users
3. **Manage blogs**: Moderate blog content
4. **Manage categories**: Create new categories
5. **View ratings**: Monitor blog ratings and reviews

## Key Features Demonstration

### User Registration with Email Verification

1. Click "Register" in navigation
2. Fill registration form
3. Check console for verification email (in development mode)
4. Copy verification link from console
5. Paste in browser to activate account

### Blog Search and Filtering

1. Go to home page
2. Use search box to find blogs by keyword
3. Filter by category from dropdown
4. Filter by author username
5. Sort by date, rating, or views

### Rating System

1. Open any blog post
2. Click "Rate this Blog"
3. Select rating (0-6)
4. Optionally add review text
5. Submit rating
6. View average rating on blog page

### Favorites System

1. Open any blog post
2. Click "Add to Favorites"
3. Author receives email notification (check console)
4. View favorites from "Favorites" link
5. Remove from favorites anytime

## Email Configuration

### Development (Default)

Emails are printed to console. Look for email content in terminal where you run `python manage.py runserver`.

### Production (Gmail Example)

1. Enable 2-Factor Authentication on Gmail
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Update `.env` file:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

## Common Commands

```bash
# Create superuser manually
python manage.py createsuperuser

# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Access from other devices on network
python manage.py runserver 0.0.0.0:8000

# Collect static files (for production)
python manage.py collectstatic

# Open Django shell
python manage.py shell
```

## File Structure Overview

```
blog_site/
├── blog_project/          # Main project settings
│   ├── settings.py       # Configuration
│   └── urls.py           # Main URL routing
├── users/                # User management app
│   ├── models.py         # User and Profile models
│   ├── views.py          # Authentication views
│   └── templates/        # User templates
├── blogs/                # Blog management app
│   ├── models.py         # Blog, Category, Rating models
│   ├── views.py          # Blog CRUD views
│   └── templates/        # Blog templates
├── templates/            # Global templates
│   └── base.html         # Base template
├── static/               # CSS, JS, images
├── media/                # User uploads
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```

## Next Steps

1. **Customize Design**: Edit templates in `templates/` and `static/`
2. **Add More Categories**: Use admin panel or Django shell
3. **Configure Email**: Update `.env` for real email sending
4. **Deploy**: See DEPLOYMENT.md for production setup
5. **Extend Features**: Add comments, likes, or notifications

## Troubleshooting

### Database Errors

```bash
# Reset database (WARNING: Deletes all data)
rm db.sqlite3
python manage.py migrate
python setup_sample_data.py
```

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

### Module Import Errors

```bash
pip install -r requirements.txt --upgrade
```

### Port Already in Use

```bash
# Use different port
python manage.py runserver 8080
```

## Need Help?

- Read the full README.md
- Check DEPLOYMENT.md for production setup
- Review Django documentation: https://docs.djangoproject.com/
- Check the code comments in views.py and models.py

## Happy Blogging! 🎉
