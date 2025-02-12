# MyBlog

**MyBlog** is a personal blogging platform developed using Python and Django. It allows users to create, edit, and manage blog posts with ease.

## Features

- **Create Posts:** Write new blog entries with rich content.
- **Edit Posts:** Update existing posts as needed.
- **Delete Posts:** Remove posts that are no longer relevant.
- **List Posts:** View a list of all blog entries.
- **Detail View:** Read full content of individual posts.

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS
- **Database:** SQLite (default)

## Getting Started

### Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/lucosmo/myblog.git
   cd myblog
2. **Create a Virtual Environment:**
  
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  ```
3. **Install Dependencies:**

  ```bash
  pip install -r requirements.txt
  ```

4. **Apply Migrations:**

  ```bash
  python manage.py migrate
  ```
5. **Create a Superuser:**

  ```bash
  python manage.py createsuperuser
  ```
6. **Run the Development Server:**
  
  ```bash
  python manage.py runserver
  ```
  The application will be accessible at ```http://127.0.0.1:8000/```.

### Usage
- Access the Admin Panel: Navigate to http://127.0.0.1:8000/admin/ and log in with your superuser credentials to manage posts.
- View Blog Posts: Visit http://127.0.0.1:8000/ to see the list of published posts.
- Create, Edit, Delete Posts: Use the admin panel to manage your blog content.

### Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments

- Developed by lucosmo
- Built with Django, a high-level Python web framework.
