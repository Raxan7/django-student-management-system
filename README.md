# Django Student Management System

A comprehensive Student Management System built with Django that allows efficient management of students, staff, courses, attendance, and other academic activities.

## Features

- **User Authentication**: Multi-user role-based login system (Admin, Staff, Students)
- **Admin Dashboard**: Complete administrative control panel
  - Manage Students and Staff (Add, Edit, View)
  - Manage Courses and Subjects
  - Handle Student/Staff Feedback
  - Manage Student/Staff Leave Applications
  - View Attendance Reports
- **Staff Dashboard**: 
  - Take and Update Attendance
  - Add/View Student Results
  - Apply for Leave
  - Provide Feedback to Admin
  - Send Student Notifications
- **Student Dashboard**:
  - View Attendance
  - View Results/Grades
  - Apply for Leave
  - Provide Feedback to Admin
  - View Notifications

## Technology Stack

- **Backend**: Django (Python Web Framework)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (default) / MySQL / PostgreSQL
- **Authentication**: Django Authentication System

## Installation and Setup

1. Clone the repository
   ```bash
   git clone https://github.com/Raxan7/django-student-management-system.git
   cd django-student-management-system
   ```

2. Create a virtual environment and activate it
   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On Linux/Mac
   source env/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (Admin)
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000`

## Usage

### Admin Access
- URL: `/admin/` 
- Login with the superuser credentials created during setup

### Staff Access
- URL: `/` (Homepage)
- Login with staff credentials (created by admin)

### Student Access
- URL: `/` (Homepage)
- Login with student credentials (created by admin)

## Project Structure

The project is organized into various apps with the main functionality in the `student_management_app` directory:

- `student_management_app`: Contains the core application logic
  - `models.py`: Defines data models like Students, Staff, Courses, etc.
  - `views.py`: Contains the view functions/classes for different user roles
  - `templates/`: HTML templates for rendering UI
  - `static/`: Static files (CSS, JS, images)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django framework documentation
- Bootstrap for responsive UI components
- All contributors who help improve this system