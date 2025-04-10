INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'tinymce',
    'crispy_forms',
    'crispy_bootstrap4',
    
    # Local apps
    'core',
    'users',
    'documents',
]

# TinyMCE settings
TINYMCE_DEFAULT_CONFIG = {
    # ... existing code ...
}

# Crispy Forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

# ... existing code ... 