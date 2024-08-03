# Mobile Showroom

An online mobile showroom website exclusively for cars..

## Getting Started

### Prerequisites

- Python 3.x
- pip (Python package installer)
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/kzmfhm/mobile-showroom.git
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv env
   source env/Scripts/activate  # On Windows
   # source env/bin/activate  # On macOS/Linux
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Django project:

   ```bash
   django-admin startproject ecommerce
   cd ecommerce
   ```

5. Create the `store` app:

   ```bash
   python manage.py startapp store
   ```

6. Apply migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

### Creating a Superuser

To create a superuser for accessing the Django admin panel, run:

```bash
python manage.py createsuperuser
```
