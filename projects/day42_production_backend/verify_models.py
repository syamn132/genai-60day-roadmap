
from app.db.models import Base, User, Job


def main():

    print("=" * 50)
    print("DAY 42 — ORM MODEL VERIFICATION")
    print("=" * 50)

    print("\n1. REGISTERED TABLES")
    print(sorted(Base.metadata.tables.keys()))

    print("\n2. USER COLUMNS")
    print(list(User.__table__.columns.keys()))

    print("\n3. JOB COLUMNS")
    print(list(Job.__table__.columns.keys()))

    print("\n4. FOREIGN KEY")

    foreign_key = next(
        iter(Job.__table__.c.user_id.foreign_keys)
    )

    print(foreign_key.target_fullname)

    print("\n5. ORM RELATIONSHIPS")

    print(
        "User.jobs ->",
        User.jobs.property.mapper.class_.__name__,
    )

    print(
        "Job.user ->",
        Job.user.property.mapper.class_.__name__,
    )

    assert set(Base.metadata.tables.keys()) == {
        "users",
        "jobs",
    }

    assert foreign_key.target_fullname == "users.id"

    print("\nORM MODELS VERIFIED SUCCESSFULLY")


if __name__ == "__main__":
    main()
