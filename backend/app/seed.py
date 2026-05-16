"""Seed database with initial users and sample data."""

from app.auth import hash_password
from app.database import SessionLocal, init_db
from app.models import Project, Task, User


def run():
    init_db()
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print("Already seeded")
            return
        admin = User(
            email="admin@taskflow.local",
            username="admin",
            password_hash=hash_password("admin"),
            display_name="Administrator",
            is_admin=True,
            wallet_balance=1000.0,
        )
        alice = User(
            email="alice@example.com",
            username="alice",
            password_hash=hash_password("password123"),
            display_name="Alice",
            wallet_balance=50.0,
        )
        bob = User(
            email="bob@example.com",
            username="bob",
            password_hash=hash_password("password123"),
            display_name="Bob",
            wallet_balance=25.0,
        )
        db.add_all([admin, alice, bob])
        db.flush()

        proj = Project(name="Q2 Launch", description="Main initiative", owner_id=alice.id)
        db.add(proj)
        db.flush()

        tasks = [
            Task(title="Design mockups", owner_id=alice.id, project_id=proj.id, status="done"),
            Task(title="API integration", owner_id=alice.id, project_id=proj.id, status="in_progress"),
            Task(title="Write docs", owner_id=bob.id, status="todo"),
            Task(title="Security review", owner_id=admin.id, status="todo", priority=3),
        ]
        db.add_all(tasks)
        db.commit()
        print("Seeded admin/alice/bob and sample tasks")
    finally:
        db.close()


if __name__ == "__main__":
    run()
