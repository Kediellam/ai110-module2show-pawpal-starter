from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create owner
    owner = Owner(name="Hannah", available_time=180)  # 3 hours

    # Create pets
    dog = Pet(name="fluffy", species="Dog", age=3)
    cat = Pet(name="blue", species="Cat", age=2)

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create tasks (different times + priorities)
    task1 = Task(
        name="Morning Walk",
        duration=30,
        priority=5,
        due_time=datetime(2026, 3, 29, 8, 0)
    )

    task2 = Task(
        name="Feed Dog",
        duration=10,
        priority=5,
        due_time=datetime(2026, 3, 29, 9, 0)
    )

    task3 = Task(
        name="Feed Cat",
        duration=10,
        priority=4,
        due_time=datetime(2026, 3, 29, 9, 30)
    )

    task4 = Task(
        name="Playtime",
        duration=20,
        priority=3
    )

    task5 = Task(
        name="Feed Dog (Recurring)",
        duration=10,
        priority=5,
        due_time=datetime(2026, 3, 29, 9, 0),
        recurring="daily"
    )

    task6 = Task(
        name="Vet Visit",
        duration=30,
        priority=5,
        due_time=datetime(2026, 3, 29, 9, 0)
    )

    task7 = Task(
        name="Dog Grooming",
        duration=45,
        priority=4,
        due_time=datetime(2026, 3, 29, 9, 0)
    )

    # Assign tasks to pets
    dog.add_task(task4)
    cat.add_task(task3)
    dog.add_task(task2)
    dog.add_task(task1)

    # Create scheduler
    scheduler = Scheduler()

    # Get all tasks from owner
    all_tasks = owner.get_all_tasks()
    sorted_tasks = scheduler.sort_tasks_by_time(all_tasks)

    print("\n🔽 UNSORTED TASKS:")
    for t in all_tasks:
        print(t)

    print("\n🔼 SORTED TASKS:")
    for t in sorted_tasks:
        print(t)

    # Generate schedule
    plan = scheduler.generate_daily_plan(
        sorted_tasks,
        owner.available_time
    )

    # Print results
    print("\n🐾 TODAY'S SCHEDULE 🐾")
    print("-" * 30)

    print(scheduler.explain_plan(plan))

if __name__ == "__main__":
    main()