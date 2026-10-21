
from pathlib import Path

source = Path("Pasted markdown.md")
output = Path("GenAI_60_Day_Roadmap_Updated_Day37.md")

if not source.exists():
    raise FileNotFoundError(
        f"Place {source.name} in the same folder as this script."
    )

content = source.read_text(encoding="utf-8")

replacements = {
    "**Last updated:** 2026-10-15":
        "**Last updated:** 2026-10-21",

    "**Overall progress:** Days 1–36 completed.":
        "**Overall progress:** Days 1–37 completed (61.7%). 23 days remaining.",

    "**Next exact step:** Day 37 — PostgreSQL":
        "**Next exact step:** Day 38 — Part 1 SQLAlchemy; Part 2 Alembic.",

    "⬜ Day 37":
        "✅ Day 37",
}

for old, new in replacements.items():
    if old not in content:
        raise ValueError(f"Expected text not found: {old}")
    content = content.replace(old, new, 1)

day37 = """
**Day 37 status:** ✅ Completed — PostgreSQL (official Part 1).

**Day 37 project:** `projects/day37_postgresql/`

**Database:** `genai_day37_new`

**Day 37 topics completed:**

- PostgreSQL and relational database fundamentals.
- Database architecture, schemas, tables, rows, and columns.
- Data types: INTEGER, VARCHAR, NUMERIC, TIMESTAMPTZ.
- Primary keys, foreign keys, and relational design.
- Constraints: NOT NULL, CHECK, DEFAULT, PRIMARY KEY.
- Homebrew PostgreSQL setup and the `psql` client.
- Database creation and table creation.
- Sample data insertion.
- SELECT, WHERE, ORDER BY, LIMIT.
- UPDATE and DELETE.
- INNER JOIN and LEFT JOIN.
- COUNT, SUM, AVG, GROUP BY, aggregation.
- EXPLAIN, indexes, query planning.
- Transactions: BEGIN, COMMIT, ROLLBACK.
- ACID properties and MVCC.
- Concurrency-safe inventory update concepts.
- Real-world database engineering and interview review.

**Day 37 project files:**

- `schema.sql` — products, customers, and orders.
- `seed.sql` — sample records.
- `queries.sql` — retrieval, joins, aggregation, EXPLAIN.
- `mutations.sql` — UPDATE exercise.
- `step21_delete.sql` — DELETE exercise.
- `step25_transactions.sql` — transaction exercise.
- `README.md` — project documentation.

**Day 37 directly verified terminal results:**

- SELECT returned Laptop, Mouse, and Keyboard.
- WHERE price > 1000 returned Laptop and Keyboard.
- ORDER BY price DESC LIMIT 2 returned Laptop and Keyboard.
- UPDATE changed Laptop stock from 10 to 15.
- PostgreSQL reported `UPDATE 1`.

**Day 37 user-confirmed remaining practicals:**

- DELETE and deletion verification.
- SQL JOINs and aggregation.
- Indexes and EXPLAIN.
- Transactions, COMMIT, and ROLLBACK.
- ACID and MVCC concepts.
- Engineering and interview exercises.

The remaining exercise outputs were user-confirmed as
completed, not individually captured in the conversation.

**Day 37 one-pagers:** ✅ Completed — Two PostgreSQL
visual revision infographics covering concepts, project setup,
SQL practicals, transactions, ACID, MVCC, and interviews.

**Day 37 learning outcome:** Built and practiced a
persistent relational PostgreSQL database in preparation
for Python/FastAPI integration through SQLAlchemy.

**Day 38 roadmap:**
- Part 1: SQLAlchemy — NEXT.
- Part 2: Alembic — Pending.

"""

old_section = (
    "**Day 37 roadmap:**\n\n"
    "- Part 1: PostgreSQL — NEXT"
)

if old_section not in content:
    raise ValueError("Could not find original Day 37 section.")

content = content.replace(old_section, day37.strip(), 1)

output.write_text(content, encoding="utf-8")

assert output.exists()
assert "genai_day37_new" in output.read_text(encoding="utf-8")
assert "✅ Day 37" in content
assert "⬜ Day 38" in content

print(f"Created: {output.resolve()}")
print(f"Size: {output.stat().st_size:,} bytes")
print("Status: Day 37 completed; Day 38 next.")
