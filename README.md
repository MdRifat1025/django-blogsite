# Blog Site - Django Blog Publishing Platform

A comprehensive blog publishing and reading platform built with Django featuring user authentication, blog management, favorites, ratings, and more.

## Features

### User Management
- **User Registration & Authentication**
  - Email verification for account activation
  - Login/Logout system
  - User profile management
  - Three user roles: Admin, Author, Reader

### Blog Management
- **For Authors:**
  - Create blogs with title, body, categories, and date
  - Edit and delete own blogs
  - Author profile with bio, profile picture, and social media links
  
### Reader Features
- **Search & Filtering:**
  - Filter by category, date, and author
  - Advanced search functionality
  
- **Favorites System:**
  - Save favorite blogs
  - Email notification when blog is favorited
  
- **Reviews & Ratings:**
  - Rate blogs (0-6 scale)
  - View average ratings
  - Sort blogs by rating

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup Instructions

1. **Clone or extract the project**

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   
   # Email Configuration
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
blog_site/
├── blog_project/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                 # User authentication app
│   ├── models.py         # Custom user model, Profile
│   ├── views.py          # Auth views
│   ├── forms.py          # Registration, Profile forms
│   └── templates/
├── blogs/                 # Blog management app
│   ├── models.py         # Blog, Category, Rating, Favorite models
│   ├── views.py          # Blog CRUD, filtering, ratings
│   ├── forms.py          # Blog creation forms
│   └── templates/
├── templates/             # Global templates
├── static/               # CSS, JS, images
└── media/                # User uploads
```

## User Roles

### Admin
- Full access to Django admin panel
- Manage all users, blogs, categories
- Moderate content

### Author
- Create, edit, delete own blogs
- Manage profile and bio
- View blog statistics

### Reader
- Browse and search blogs
- Rate blogs
- Save favorite blogs
- Leave reviews

## Email Configuration

For development, emails are printed to console. For production:

1. Use a real SMTP server (Gmail, SendGrid, etc.)
2. Update `.env` with proper credentials
3. For Gmail, enable 2FA and create an App Password
4. Change `EMAIL_BACKEND` to `django.core.mail.backends.smtp.EmailBackend`

## Usage

### Creating a Blog
1. Login as an Author
2. Navigate to "Create Blog"
3. Fill in title, content, category
4. Click "Publish"

### Rating a Blog
1. Login as any user
2. View a blog post
3. Select rating (0-6)
4. Submit rating

### Saving Favorites
1. Login as any user
2. Click "Add to Favorites" on any blog
3. Receive email notification
4. View favorites in your profile

### Filtering Blogs
- Use the search bar for keyword search
- Filter by category from dropdown
- Filter by author
- Sort by date or rating

## Development Notes

- Email verification links are valid for 24 hours
- Password reset tokens expire after 1 hour
- Blog images are stored in `media/blog_images/`
- Profile pictures are stored in `media/profile_pics/`

## Security Considerations

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use strong passwords for email accounts
- Configure ALLOWED_HOSTS properly
- Use HTTPS in production
- Keep dependencies updated

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for educational purposes.

## Support

For issues or questions, please refer to the Django documentation or create an issue in the repository.
