┌────────────────────┐
│   FitnessClass     │
├────────────────────┤
│ id (PK)            │
│ class_type         │
│ capacity           │
│ instructor         │
└────────┬───────────┘
         │ 1
         │
         │
         │ N
┌────────▼───────────┐
│       Slot         │
├────────────────────┤
│ id (PK)            │
│ fitness_class_id (FK → FitnessClass.id) │
│ date               │
│ start_time         │
│ end_time           │
└────────┬───────────┘
         │ 1
         │
         │
         │ N
┌────────▼───────────┐       ┌────────────┐
│     Booking        │◄─────►│   Client    │
├────────────────────┤       ├────────────┤
│ id (PK)            │       │ id (PK)     │
│ client_id (FK)     │       │ name        │
│ slot_id (FK)       │       │ email (unique) │
│ status             │
│ created_at         │
└────────────────────┘
📌 Notes
available_slots is a dynamic property in Slot:

pgsql
Copy
Edit
fitness_class.capacity - slot.bookings.filter(status='confirmed').count()
Clients cannot book the same slot more than once (unique_together).

Confirmed bookings are considered for slot availability.

The schema is normalized and scalable for future features like:

Payments

Attendance tracking
