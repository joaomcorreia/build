# Build Platform - Multi-Tenant Website Builder

A sophisticated Django-based multi-tenant SaaS platform for building and managing websites with AI-powered tools, advanced media management, and subscription-based access control.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Django](https://img.shields.io/badge/Django-4.2.7-darkgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🚀 Features

### Multi-Tenancy
- **Schema-based isolation** - Each tenant gets their own database schema
- **Subdomain routing** - Automatic tenant identification via subdomains
- **Flexible subscription plans** - Starter, Professional, and Enterprise tiers
- **Per-tenant customization** - Colors, logos, and feature toggles

### Website Management
- **Visual page builder** - Drag-and-drop interface for creating pages
- **Reusable components** - Header, footer, hero sections, and custom components
- **Responsive design** - Mobile-first approach with Bootstrap integration
- **SEO optimization** - Meta tags, structured data, and analytics integration

### AI-Powered Tools
- **Content generation** - Create blog posts, product descriptions, and marketing copy
- **Image generation** - AI-powered image creation and editing
- **SEO optimization** - Automated meta descriptions and keyword suggestions
- **Text improvement** - Grammar checking and style enhancement

### Media Library
- **Advanced file management** - Organized folders with tagging and search
- **Image optimization** - Automatic WebP conversion and multiple size variants
- **Cloud storage** - AWS S3 integration for scalable media hosting
- **Usage tracking** - Monitor where files are used across your websites

### Developer Features
- **REST API** - Complete API for all platform functionality
- **Webhook system** - Real-time notifications for events
- **Custom domains** - Bring your own domain with SSL support
- **Analytics integration** - Google Analytics and Facebook Pixel support

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Public Schema │    │  Tenant Schema  │    │  Tenant Schema  │
│                 │    │                 │    │                 │
│ • Users         │    │ • Websites      │    │ • Websites      │
│ • Subscriptions │    │ • Pages         │    │ • Pages         │
│ • Tenants       │    │ • Media Files   │    │ • Media Files   │
│ • Billing       │    │ • AI Requests   │    │ • AI Requests   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Django App    │
                    │                 │
                    │ • Multi-tenant  │
                    │ • REST API      │
                    │ • Admin Panel   │
                    │ • Celery Tasks  │
                    └─────────────────┘
```

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7, Django REST Framework
- **Database**: PostgreSQL with django-tenants
- **Caching**: Redis
- **Background Tasks**: Celery
- **File Storage**: AWS S3 + Local (development)
- **AI Integration**: OpenAI GPT-4, DALL-E
- **Frontend**: Bootstrap 5, Alpine.js (future)
- **Deployment**: Docker, Nginx, Gunicorn

## 📦 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/joaomcorreia/build.git
cd build
```

### 2. Environment Setup

```bash
# Copy environment file
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Docker Deployment (Recommended)

```bash
# For development
./deploy.sh dev
# or on Windows
deploy.bat dev

# For production
./deploy.sh production
# or on Windows
deploy.bat production
```

### 4. Manual Setup (Alternative)

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate_schemas --shared
python manage.py create_public_tenant
python manage.py createsuperuser

# Start development server
python manage.py runserver

# In another terminal, start Celery
celery -A build_project worker --loglevel=info
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Core Settings
DEBUG=True
SECRET_KEY=your-super-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,.build.justcodeworks.eu

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/build_db

# Redis
REDIS_URL=redis://localhost:6379/0

# AWS S3 (Production)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Database Setup

1. Create PostgreSQL database:
```sql
CREATE DATABASE build_db;
CREATE USER build_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE build_db TO build_user;
```

2. Run migrations:
```bash
python manage.py migrate_schemas --shared
```

3. Create the public tenant:
```bash
python manage.py create_public_tenant --domain=build.justcodeworks.eu
```

## 🚀 Usage

### Creating a New Tenant

```bash
python manage.py create_tenant \
    "Acme Corp" \
    "acme" \
    "Acme Corporation" \
    "admin@acme.com" \
    --plan=professional \
    --days=30
```

This creates a tenant accessible at `acme.build.justcodeworks.eu`

### API Usage

The platform provides a comprehensive REST API:

```python
# Example: Create a new page via API
import requests

# Authenticate
response = requests.post('https://acme.build.justcodeworks.eu/api/v1/auth/login/', {
    'email': 'user@acme.com',
    'password': 'password'
})
token = response.json()['token']

# Create a page
headers = {'Authorization': f'Token {token}'}
page_data = {
    'title': 'About Us',
    'content': '<h1>About Our Company</h1><p>We are awesome!</p>',
    'is_published': True
}
response = requests.post(
    'https://acme.build.justcodeworks.eu/api/v1/websites/pages/',
    json=page_data,
    headers=headers
)
```

### AI Tools Integration

```python
# Generate content using AI
ai_request = {
    'tool_type': 'content_generator',
    'prompt': 'Write a compelling product description for organic coffee beans',
    'parameters': {
        'max_tokens': 200,
        'temperature': 0.7
    }
}
response = requests.post(
    'https://acme.build.justcodeworks.eu/api/v1/ai-tools/generate-content/',
    json=ai_request,
    headers=headers
)
```

## 🎨 Customization

### Theme Customization

Each tenant can customize their website appearance:

```python
# Update tenant branding
tenant_data = {
    'primary_color': '#ff6b35',
    'secondary_color': '#004e89',
    'logo_url': 'https://example.com/logo.png'
}
```

### Custom Components

Create reusable components for your websites:

```python
component = {
    'name': 'Hero Section',
    'component_type': 'hero',
    'html_content': '''
        <section class="hero bg-primary text-white py-5">
            <div class="container">
                <h1>{{title}}</h1>
                <p>{{subtitle}}</p>
                <a href="{{cta_link}}" class="btn btn-light">{{cta_text}}</a>
            </div>
        </section>
    ''',
    'css_styles': '''
        .hero {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        }
    '''
}
```

## 📊 Monitoring & Analytics

### Usage Statistics

Monitor platform usage through the admin panel:

- Tenant activity and resource usage
- API request volumes and performance
- AI tool usage and costs
- Storage consumption

### Performance Monitoring

- Database query optimization
- Redis cache hit rates
- Celery task processing times
- Error tracking and logging

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test websites

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🚢 Deployment

### Production Deployment

1. **Server Setup**:
   - Ubuntu 20.04+ or similar
   - Docker and Docker Compose
   - SSL certificates
   - Domain configuration

2. **Environment Configuration**:
   ```bash
   # Clone repository
   git clone https://github.com/joaomcorreia/build.git
   cd build
   
   # Configure production environment
   cp .env.example .env
   # Edit .env with production values
   
   # Deploy
   ./deploy.sh production
   ```

3. **SSL Setup**:
   ```bash
   # Using Certbot for Let's Encrypt
   certbot --nginx -d build.justcodeworks.eu -d *.build.justcodeworks.eu
   ```

### Scaling Considerations

- **Database**: Use read replicas for high traffic
- **Cache**: Redis clustering for large datasets
- **Storage**: CDN integration for media files
- **Workers**: Scale Celery workers based on queue length

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `python manage.py test`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Submit a pull request

### Code Style

- Follow PEP 8
- Use Black for code formatting
- Write comprehensive tests
- Document new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Wiki](https://github.com/joaomcorreia/build/wiki)
- **Issues**: [GitHub Issues](https://github.com/joaomcorreia/build/issues)
- **Discord**: [Community Server](https://discord.gg/build-platform)
- **Email**: support@justcodeworks.eu

## 🗺️ Roadmap

### Q1 2024
- [ ] Visual page builder interface
- [ ] Enhanced AI tools (GPT-4, Claude)
- [ ] Mobile app for content management
- [ ] Advanced analytics dashboard

### Q2 2024
- [ ] E-commerce integration
- [ ] Multi-language support
- [ ] Advanced SEO tools
- [ ] White-label solutions

### Q3 2024
- [ ] Marketplace for themes and plugins
- [ ] Advanced automation workflows
- [ ] Integration with popular tools (Zapier, etc.)
- [ ] Performance optimizations

---

**Built with ❤️ by the JustCodeWorks team**

For more information, visit [justcodeworks.eu](https://justcodeworks.eu)