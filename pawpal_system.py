"""
PawPal+ Pet Care Management System

A system for managing pet care tasks with owner and scheduler support.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from datetime import timedelta, datetime


@dataclass
class Task:
    """Represents a single pet care task."""
    name: str
    duration: float  # in minutes
    priority: int  # 1-5, where 5 is highest
    recurring: Optional[str] = None  # "daily", "weekly", or None
    due_time: Optional[datetime] = None
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_conflicting(self, other: "Task") -> bool:
        """Return True if this task overlaps in time with another task."""
        # Tasks without due_time don't conflict (can be scheduled flexibly)
        if self.due_time is None or other.due_time is None:
            return False
        
        # Calculate end times
        self_end = self.due_time.timestamp() + (self.duration * 60)  # duration is in minutes
        other_end = other.due_time.timestamp() + (other.duration * 60)
        
        # Check for overlap: self starts before other ends AND other starts before self ends
        self_start = self.due_time.timestamp()
        other_start = other.due_time.timestamp()
        
        return self_start < other_end and other_start < self_end

    def __str__(self) -> str:
        """Return a formatted string representation of the task with status and details."""
        status = "✓" if self.completed else "○"
        recurring_tag = " (recurring)" if self.recurring else ""
        due_str = f" @ {self.due_time.strftime('%H:%M')}" if self.due_time else ""
        return f"{status} {self.name} ({self.duration}min, priority {self.priority}){due_str}{recurring_tag}"


@dataclass
class Pet:
    """Represents a pet and its associated tasks."""
    name: str
    species: str
    age: float
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> None:
        """Remove all tasks with the given name from this pet's task list."""
        self.tasks = [task for task in self.tasks if task.name != task_name]

    def get_tasks(self) -> List[Task]:
        """Return this pet's complete list of tasks."""
        return self.tasks


class Owner:
    """Represents a pet owner who manages one or more pets."""

    def __init__(self, name: str, available_time: float) -> None:
        """Initialize an owner with a name and available daily time in minutes."""
        self.name: str = name
        self.available_time: float = available_time
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Append a pet to the owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove all pets with the given name from the owner's list."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_all_tasks(self) -> List[Task]:
        """Aggregate and return all tasks from all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Handles scheduling and optimization of pet care tasks."""

    def generate_daily_plan(
        self, tasks: List[Task], available_time: float
    ) -> List[Task]:
        """Return pending tasks sorted by priority that fit within the available time."""
        # Filter out completed tasks
        pending_tasks = [task for task in tasks if not task.completed]
        
        # Sort by priority (highest first)
        sorted_tasks = self.sort_tasks_by_priority(pending_tasks)
        
        # Fit tasks within available time
        scheduled_plan = []
        total_time = 0.0
        
        for task in sorted_tasks:
            if total_time + task.duration <= available_time:
                scheduled_plan.append(task)
                total_time += task.duration
        
        return scheduled_plan

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by priority in descending order (highest first)."""
        return sorted(tasks, key=lambda task: task.priority, reverse=True)

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by due_time (earliest first), placing tasks without due_time at the end."""
        return sorted(tasks, key=lambda task: (task.due_time is None, task.due_time))

    def filter_tasks_by_status(self, tasks: List[Task], completed: bool) -> List[Task]:
        """Return tasks filtered by completion status. If completed=True, return completed tasks; else return pending tasks."""
        return [task for task in tasks if task.completed == completed]

    def filter_tasks_by_pet(self, tasks: List[Task], pet: Pet) -> List[Task]:
        """Return only tasks belonging to the specified pet."""
        """Filter tasks by assigned pet."""
        pet_tasks = set(pet.get_tasks())
        return [task for task in tasks if task in pet_tasks]

    def detect_conflicts(self, tasks: List[Task]) -> List[Tuple[Task, Task]]:
        """Detect scheduling conflicts between tasks with the same time."""
        conflicts = []
        
        # Check each pair of tasks
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if tasks[i].is_conflicting(tasks[j]):
                    conflicts.append((tasks[i], tasks[j]))
        
        return conflicts

    def explain_plan(self, plan: List[Task]) -> str:
        """Return a formatted summary of the scheduled tasks and total duration."""
        if not plan:
            return "No tasks scheduled."
        
        explanation = "Daily Schedule:\n"
        total_duration = sum(task.duration for task in plan)
        
        for i, task in enumerate(plan, 1):
            explanation += f"{i}. {task.name} ({task.duration}min, priority {task.priority})\n"
        
        explanation += f"\nTotal scheduled time: {total_duration} minutes"
        return explanation

    def handle_recurring_task(self, task: Task) -> Optional[Task]:
        """Generate the next occurrence of a recurring task."""
        if not task.recurring:
            return None

        if task.recurring == "daily":
            next_due = task.due_time + timedelta(days=1) if task.due_time else None
        elif task.recurring == "weekly":
            next_due = task.due_time + timedelta(weeks=1) if task.due_time else None
        else:
            return None

        return Task(
            name=task.name,
            duration=task.duration,
            priority=task.priority,
            due_time=next_due,
            recurring=task.recurring
        )
