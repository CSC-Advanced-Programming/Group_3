# Innovation Hub Management System

A Django-based management system for innovation hubs, built following Clean Architecture principles. This system helps manage programs, projects, facilities, equipment, services, and participants in an innovation hub environment.

## 🏗️ Architecture

This project follows Clean Architecture principles, with the following structure:

```
core/
├── domain/           # Enterprise business rules
│   ├── entities/     # Core business entities
│   └── value_objects/# Value objects used by entities
├── application/      # Application business rules
│   ├── interfaces/   # Repository interfaces
│   ├── services/     # Application services
│   └── use_cases/    # Business use cases
├── infrastructure/   # External frameworks and tools
│   ├── models/       # Django ORM models
│   ├── repositories/ # Repository implementations
│   └── forms/        # Django forms
└── interfaces/       # Interface adapters
    ├── controllers/  # View controllers
    ├── presenters/   # View presenters
    └── serializers/  # Data serializers
```

## 🚀 Features

- **Program Management**: Create and manage innovation programs
- **Project Tracking**: Track projects within programs
- **Facility Management**: Manage innovation hub facilities
- **Equipment Inventory**: Track and manage equipment
- **Service Catalog**: Manage services offered
- **Participant Management**: Track project participants

## 🛠️ Technology Stack

- Python 3.9+
- Django 4.2+
- SQLite (Development)
- pytest for testing
- Clean Architecture

## 📋 Prerequisites

- Python 3.9 or higher
- pip package manager
- Virtual environment tool

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/CSC-Advanced-Programming/Group_3.git
cd Group_3
```

2. Create and activate a virtual environment:
```bash
python -m venv venve
# On Windows:
venve\\Scripts\\activate
# On Unix or MacOS:
source venve/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

## 🏃‍♂️ Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Access the application at http://127.0.0.1:8000/

## 🧪 Testing

Run the tests using pytest:
```bash
pytest
```

Or using Django's test runner:
```bash
python manage.py test
```

## 📁 Project Structure

- `core/`: Main application directory
  - `domain/`: Business entities and rules
  - `application/`: Use cases and interfaces
  - `infrastructure/`: External frameworks implementation
  - `interfaces/`: Controllers and presenters
  - `templates/`: HTML templates
  - `tests/`: Test files

## 🔍 Key Models

- **Program**: Innovation programs with focus areas and phases
- **Project**: Projects under programs, with innovation focus and stages
- **Facility**: Physical locations with capabilities
- **Equipment**: Tools and machines available in facilities
- **Service**: Services offered at facilities
- **Participant**: Project participants and their roles

## 🌐 API Endpoints

### Programs
- `GET /programs/`: List all programs
- `POST /programs/create/`: Create new program
- `GET /programs/<id>/`: View program details
- `PUT /programs/<id>/update/`: Update program
- `DELETE /programs/<id>/delete/`: Delete program

### Projects
- `GET /projects/`: List all projects
- `POST /projects/create/`: Create new project
- `GET /projects/<id>/`: View project details
- `PUT /projects/<id>/update/`: Update project
- `DELETE /projects/<id>/delete/`: Delete project

*(Similar patterns for Facilities, Equipment, Services, and Participants)*

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ✨ Clean Architecture Benefits

- **Independence of Frameworks**: The core business logic is independent of Django
- **Testability**: Business rules can be tested without the UI, database, or any external element
- **Independence of UI**: The UI can change without changing the rest of the system
- **Independence of Database**: Business rules are not bound to the database

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
