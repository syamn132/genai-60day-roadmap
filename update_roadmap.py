
from pathlib import Path

source = Path("Pasted markdown.md")
output = Path("GenAI_60_Day_Roadmap_Updated_Day38.md")

if not source.exists():
    raise FileNotFoundError(
        f"Place {source.name} in the same folder as this script."
    )

content = source.read_text(encoding="utf-8")

# ---------------------------------------
# STEP 1: UPDATE CURRENT ROADMAP STATUS
# ---------------------------------------

replacements = {
    "**Last updated:** 2026-10-21":
        "**Last updated:** 2026-10-22",

    "**Overall progress:** Days 1–37 completed (61.7%). 23 days remaining.":
        "**Overall progress:** Days 1–38 completed (63.3%). 22 days remaining.",

    "**Next exact step:** Day 38 — Part 1 SQLAlchemy; Part 2 Alembic.":
        "**Next exact step:** Day 39 — Part 1 Authentication; Part 2 JWT; Part 3 OAuth.",

    "⬜ Day 38":
        "✅ Day 38",
}

for old, new in replacements.items():
    if content.count(old) != 1:
        raise ValueError(
            f"Expected exactly one occurrence of: {old}"
        )
    content = content.replace(old, new, 1)


# ---------------------------------------
# STEP 2: PREPARE DAY 38 COMPLETION RECORD
# ---------------------------------------

day38 = """
**Day 38 status:** ✅ Completed — SQLAlchemy (Part 1) and Alembic (Part 2).

**Day 38 project:** `projects/day38_sqlalchemy_alembic/`

**Database:** `genai_day37_new`

**Day 38 Part 1 status:** ✅ Completed — SQLAlchemy.

**Day 38 Part 1 topics completed:**

- SQLAlchemy fundamentals: Core vs ORM.
- ORM purpose and object-relational mapping.
- PostgreSQL integration with psycopg 3.
- SQLAlchemy Engine and database connectivity.
- Connection pooling and pool_pre_ping.
- DeclarativeBase, Mapped, and mapped_column.
- PostgreSQL data types and Python type mapping.
- Primary keys and Identity(always=True).
- SQLAlchemy Session lifecycle.
- ORM SELECT, WHERE, ORDER BY, and primary-key lookup.
- ORM CREATE, READ, UPDATE, and DELETE.
- session.add(), flush(), commit(), refresh(), and rollback().
- ORM object lifecycle and change tracking.
- Transaction rollback and data integrity.
- Customer, Product, and Order ORM models.
- Foreign-key relationships and back_populates.
- One-to-many relationships.
- selectinload() and N+1 query awareness.
- FastAPI database dependency injection.
- Session management using Depends() and yield.
- Pydantic request and response schemas.
- PostgreSQL-backed FastAPI CRUD endpoints.
- Swagger UI endpoint verification.
- Real-world backend engineering and interview review.

**Day 38 Part 1 project files:**

- `database.py` — SQLAlchemy Engine and database connection.
- `models.py` — Product, Customer, and Order ORM models.
- `verify_connection.py` — PostgreSQL connection testing.
- `orm_read.py` — ORM retrieval and filtering.
- `orm_crud.py` — ORM CREATE, READ, UPDATE, DELETE.
- `orm_transactions.py` — transaction and rollback testing.
- `orm_relationships.py` — related data retrieval.
- `dependencies.py` — FastAPI Session dependency.
- `schemas.py` — Pydantic API schemas.
- `main.py` — database-backed FastAPI Product API.

**Day 38 Part 1 directly verified terminal results:**

- Successfully connected to `genai_day37_new`.
- Retrieved three existing products.
- Laptop stock was 13.
- Mouse stock was 25.
- Keyboard stock was 15.
- ORM filtering price > 1000 returned Laptop and Keyboard.
- session.get(Product, 1) returned Laptop.
- Created temporary ORM product with ID 5.
- Read temporary product with stock 5.
- Updated temporary product stock from 5 to 8.
- Deleted temporary product.
- Post-deletion lookup returned None.
- Original three product records remained unchanged.

**Day 38 transaction verification:**

- Original Laptop stock: 13.
- Stock after session.flush(): 11.
- Transaction successfully rolled back.
- Stock after rollback: 13.
- Uncommitted stock update was correctly undone.

**Day 38 relationship verification:**

- Arjun — Bengaluru — Laptop — quantity 1.
- Arjun order total: 65000.00.
- Priya — Mysuru — Mouse — quantity 3.
- Priya order total: 1500.00.
- Arjun order count: 1.
- Priya order count: 1.

**Day 38 FastAPI practicals:** ✅ User-confirmed completed.

- GET /products — read all products.
- POST /products — create product.
- GET /products/{product_id} — read one product.
- PATCH /products/{product_id} — update product.
- DELETE /products/{product_id} — delete practice product.
- GET after deletion — 404 verification.
- Original PostgreSQL records preserved.

**Day 38 Part 1 Git status:**

- Git commit: `e5a723d`.
- Commit message: `Day 38 Part 1 Compelted`.
- Successfully pushed to GitHub main branch.

**Day 38 Part 2 status:** ✅ Completed — Alembic.

**Day 38 Part 2 topics completed:**

- Database schema version control.
- Why schema migrations are necessary.
- SQLAlchemy versus Alembic responsibilities.
- Alembic installation and initialization.
- alembic.ini and env.py configuration.
- SQLAlchemy Base.metadata integration.
- Alembic versions directory and revision files.
- Baseline revision for an existing database.
- alembic stamp head.
- Migration upgrade() and downgrade() functions.
- Adding a nullable description column.
- ALTER TABLE concepts.
- alembic revision and revision history.
- alembic upgrade head.
- alembic downgrade -1.
- Checking the current revision.
- Reapplying migrations.
- Updating SQLAlchemy ORM models after migration.
- Updating FastAPI Pydantic schemas.
- Preserving existing database records.
- Backup and migration safety considerations.

**Day 38 Part 2 practical verification:**

- Alembic successfully connected to PostgreSQL.
- Database schema migration was applied.
- `alembic current` returned `b35d2f0f74e7 (head)`.
- The products table contained the description column.
- Laptop, Mouse, and Keyboard remained intact.
- Existing description values were NULL.
- Downgrade and re-upgrade practicals were user-confirmed.
- FastAPI description-field API tests were user-confirmed.

**Day 38 troubleshooting:**

- Diagnosed PostgreSQL 17 startup failure.
- Identified a stale postmaster.pid reference.
- Verified the recorded PID was assigned to MacDroid,
  rather than a running PostgreSQL server.
- PostgreSQL became accessible again for Alembic testing.

**Day 38 one-pagers:** ✅ Completed — Two visual revision
infographics covering SQLAlchemy, Alembic, ORM operations,
sessions, relationships, transactions, FastAPI integration,
database migrations, and practical verification.

**Day 38 learning outcome:**

Integrated Python and FastAPI with the existing PostgreSQL
database using SQLAlchemy ORM. Implemented and verified
persistent CRUD, transaction rollback, and ORM relationships.
Used Alembic to version and evolve the database schema
while preserving existing records.

**Day 39 roadmap:**

- Part 1: Authentication — NEXT.
- Part 2: JWT — Pending.
- Part 3: OAuth — Pending.

"""


# ---------------------------------------
# STEP 3: REPLACE DAY 38 ROADMAP PLACEHOLDER
# ---------------------------------------

old_section = (
    "**Day 38 roadmap:**\n"
    "- Part 1: SQLAlchemy — NEXT.\n"
    "- Part 2: Alembic — Pending."
)

if content.count(old_section) != 1:
    raise ValueError(
        "Could not find exactly one original Day 38 section."
    )

content = content.replace(
    old_section,
    day38.strip(),
    1,
)


# ---------------------------------------
# STEP 4: VERIFY ALL UPDATES
# ---------------------------------------

checks = [
    "Days 1–38 completed (63.3%)",
    "✅ Day 37",
    "✅ Day 38",
    "⬜ Day 39",
    "**Day 38 status:** ✅ Completed",
    "**Day 38 Part 1 status:** ✅ Completed",
    "**Day 38 Part 2 status:** ✅ Completed",
    "**Day 38 one-pagers:** ✅ Completed",
    "genai_day37_new",
    "b35d2f0f74e7 (head)",
    "**Day 39 roadmap:**",
]

for item in checks:
    if item not in content:
        raise AssertionError(
            f"Verification failed: {item}"
        )

assert "**Day 37 status:**" in content
assert "**Day 36 status:**" in content
assert "Day 39 — Part 1 Authentication" in content


# ---------------------------------------
# STEP 5: WRITE UPDATED MARKDOWN
# ---------------------------------------

if output.exists():
    raise FileExistsError(
        f"{output.name} already exists. "
        "Rename the existing output before rerunning."
    )

output.write_text(content, encoding="utf-8")

assert output.exists()
assert output.stat().st_size > 0

print()
print("=" * 55)
print("DAY 38 ROADMAP UPDATE SUCCESSFUL")
print("=" * 55)
print(f"Created: {output.resolve()}")
print(f"Size: {output.stat().st_size:,} bytes")
print("Progress: Days 1–38 completed (63.3%)")
print("Remaining: 22 days")
print("Day 38 Part 1: SQLAlchemy completed")
print("Day 38 Part 2: Alembic completed")
print("Day 38 one-pagers: completed")
print("Next: Day 39 — Authentication, JWT, OAuth")
print("Original Markdown file preserved.")
print("=" * 55)
