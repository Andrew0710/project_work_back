# project_work_back
![Схема бази даних ](./docs/er_diagram.png)

## REST API (DRF + JWT + Swagger)

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Swagger / OpenAPI

- Swagger UI: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- OpenAPI schema: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

### Authentication (JWT)

Request tokens:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"phone":"+380001112233","password":"your_password"}'
```

Refresh token:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<refresh_token>"}'
```

### Key business scenarios

1. **Conflict detection for lessons**
   - Create two lessons for the same teacher with overlapping time.
   - Expected: API rejects the second lesson (`400`) with teacher conflict error.

2. **Branch consistency rules**
   - Try to schedule a lesson where `subject`, `student`, or `group` belongs to another branch.
   - Expected: API rejects request (`400`) with field-level validation error.

3. **Subscription rule**
   - Create `StudentSubscription` where subject is not included in selected plan.
   - Expected: API rejects request (`400`) with subject-plan mismatch error.

4. **Permission checks**
   - Use TEACHER token to create lessons/attendance (allowed).
   - Use TEACHER token to modify branches/students/plans (denied).
   - Use ADMIN token for full CRUD access.

### Frontend integration

- `/login/` authenticates via JWT and stores tokens in `localStorage`.
- `/lessons/` fetches lesson data from `/api/lessons/` with `Authorization: Bearer <token>`.
- `/` provides quick links to Swagger and API-backed pages.