# 🗓️ Event Scheduling API

A RESTful API for managing events, attendees, time slots, and analytics. Built with Django, Django REST Framework, and PostgreSQL.

---

## 🚀 Features

- ✅ Create, read, update, delete events
- 👥 Add/remove attendees to/from events
- 🛑 Prevent double-booking of attendees
- 🔁 Recurring events: none, daily, weekly, monthly
- 🔍 Search events by title, date range, or attendee
- 📅 Find available time slots (conflict-aware)
- 📊 Analytics: average attendance, popular times, top attendees
- ⚙️ Pagination, input validation, and error handling
- 🔐 (Optional) Ready for authentication and token-based access
- 🧪 Fully testable with Postman or Swagger

---

## 🧰 Tech Stack

- Python 3.x
- Django 4.x
- Django REST Framework
- PostgreSQL
- drf-spectacular (optional API docs)
- django-environ (env-based config)

---

## 🛠️ Installation

```bash
git clone https://github.com/Sufail07/Event-Management-System.git
cd Event-Management-System
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ⚙️ Environment Configuration

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/eventdb
```

Make sure `.env` is in `.gitignore`.

---

## 🔄 Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## 🚦 Run the Server

```bash
python manage.py runserver
```

Access the API at:  
`http://localhost:8000/api/`

---

## 🔌 API Endpoints Overview

### 🧱 Event CRUD

| Method | Endpoint               | Description          |
|--------|------------------------|----------------------|
| GET    | `/api/events/`         | List events          |
| POST   | `/api/events/`         | Create event         |
| GET    | `/api/events/<id>/`    | Event details        |
| PUT    | `/api/events/<id>/`    | Update event         |
| DELETE | `/api/events/<id>/`    | Delete event         |

### 👥 Attendees

| Method | Endpoint                              | Description              |
|--------|----------------------------------------|--------------------------|
| POST   | `/api/events/<id>/add_attendee/`       | Add user to event        |
| POST   | `/api/events/<id>/remove_attendee/`    | Remove user from event   |

### 🔍 Search & Availability

| Method | Endpoint                                                   | Description                    |
|--------|------------------------------------------------------------|--------------------------------|
| GET    | `/api/events/search/?title=...&start_date=...&attendee_id=...` | Search events dynamically |
| GET    | `/api/events/availability/?date=YYYY-MM-DD`               | Free 1-hour time slots         |

### 📊 Analytics

| Method | Endpoint                  | Description                          |
|--------|---------------------------|--------------------------------------|
| GET    | `/api/events/analytics/`  | Avg attendance, top times, top users |

---

## 📄 Sample Event Payload

```json
{
  "title": "Weekly Sync",
  "description": "Team catch-up",
  "date": "2025-06-24",
  "start_time": "09:00",
  "end_time": "09:30",
  "location": "Zoom",
  "attendees": [1, 2],
  "recurrence": "weekly"
}
```

---

## 📦 Sample Search Request

```http
GET /api/events/search/?title=planning&start_date=2025-06-20&end_date=2025-06-25&attendee_id=2
```

---

## ✅ Coming Soon / Ideas

- [ ] Token or JWT Authentication
- [ ] ICS calendar export
- [ ] User-specific calendar view
- [ ] CSV export for analytics
- [ ] Admin dashboard

---

## 🤝 Contributing

Pull requests are welcome.  
Please open an issue first to discuss major changes.

---

## 🛡 License

This project is licensed under the MIT License.

---

## 👤 Author

Built with ❤️ by Sufail :))
