"""
Unit tests for PawPal+ Pet Care Management System
"""

import pytest
from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Scheduler


class TestTaskCompletion:
    """Tests for Task completion functionality."""

    def test_task_completion(self):
        """
        Test that a task starts incomplete and can be marked complete.
        
        Steps:
        1. Create a Task object
        2. Verify completed is initially False
        3. Call mark_complete()
        4. Assert completed is now True
        """
        # Create a task
        task = Task(name="Feed Dog", duration=10, priority=5)
        
        # Verify initial state
        assert task.completed is False, "Task should start as incomplete"
        
        # Mark task as complete
        task.mark_complete()
        
        # Verify it's now complete
        assert task.completed is True, "Task should be marked as complete"


class TestPetTaskManagement:
    """Tests for Pet task management functionality."""

    def test_pet_task_addition(self):
        """
        Test that tasks can be added to a pet.
        
        Steps:
        1. Create a Pet object
        2. Record initial task count
        3. Add a Task to the Pet
        4. Assert task count increases by 1
        5. Verify the last task added is correct
        """
        # Create a pet
        pet = Pet(name="Fluffy", species="Dog", age=3)
        
        # Record initial task count
        initial_task_count = len(pet.tasks)
        assert initial_task_count == 0, "New pet should have no tasks"
        
        # Create and add a task
        task = Task(name="Morning Walk", duration=30, priority=5)
        pet.add_task(task)
        
        # Assert task count increased by 1
        new_task_count = len(pet.tasks)
        assert new_task_count == initial_task_count + 1, "Task count should increase by 1"
        
        # Verify the last task added is correct
        assert pet.tasks[-1].name == "Morning Walk", "Last task should be the one we added"
        assert pet.tasks[-1].duration == 30, "Task duration should match"
        assert pet.tasks[-1].priority == 5, "Task priority should match"


class TestSortTasksByTime:
    """Tests for sorting tasks by due_time in chronological order."""

    def test_sort_tasks_chronological_order(self):
        """
        Test that tasks are sorted by due_time in chronological order (earliest first).
        
        Steps:
        1. Create tasks with different due times
        2. Sort using scheduler.sort_tasks_by_time()
        3. Assert tasks are in chronological order
        """
        scheduler = Scheduler()
        
        # Create tasks with different times (not in order)
        task1 = Task(name="Feed Dog", duration=10, priority=5, 
                     due_time=datetime(2026, 3, 29, 9, 0))
        task2 = Task(name="Morning Walk", duration=30, priority=5, 
                     due_time=datetime(2026, 3, 29, 8, 0))
        task3 = Task(name="Playtime", duration=20, priority=3, 
                     due_time=datetime(2026, 3, 29, 10, 0))
        
        unsorted_tasks = [task1, task2, task3]
        sorted_tasks = scheduler.sort_tasks_by_time(unsorted_tasks)
        
        # Assert chronological order
        assert sorted_tasks[0].name == "Morning Walk", "8:00 task should be first"
        assert sorted_tasks[1].name == "Feed Dog", "9:00 task should be second"
        assert sorted_tasks[2].name == "Playtime", "10:00 task should be third"

    def test_sort_tasks_mixed_with_none(self):
        """
        Test that tasks with due_time=None are placed at the end.
        
        Steps:
        1. Create tasks with and without due_time
        2. Sort using scheduler.sort_tasks_by_time()
        3. Assert scheduled tasks come first, unscheduled last
        """
        scheduler = Scheduler()
        
        # Mix of scheduled and unscheduled tasks
        task1 = Task(name="Walk", duration=30, priority=5, 
                     due_time=datetime(2026, 3, 29, 9, 0))
        task2 = Task(name="Playtime", duration=20, priority=3, due_time=None)
        task3 = Task(name="Feed", duration=10, priority=5, 
                     due_time=datetime(2026, 3, 29, 8, 0))
        task4 = Task(name="Groom", duration=45, priority=2, due_time=None)
        
        unsorted_tasks = [task1, task2, task3, task4]
        sorted_tasks = scheduler.sort_tasks_by_time(unsorted_tasks)
        
        # Assert scheduled tasks come first (in time order), unscheduled last
        assert sorted_tasks[0].due_time is not None, "First should be scheduled"
        assert sorted_tasks[1].due_time is not None, "Second should be scheduled"
        assert sorted_tasks[2].due_time is None, "Third should be unscheduled"
        assert sorted_tasks[3].due_time is None, "Fourth should be unscheduled"
        assert sorted_tasks[0].name == "Feed", "8:00 should be first"
        assert sorted_tasks[1].name == "Walk", "9:00 should be second"

    def test_sort_tasks_same_time(self):
        """
        Test that tasks with the same due_time are both preserved.
        
        Steps:
        1. Create multiple tasks with the same due_time
        2. Sort using scheduler.sort_tasks_by_time()
        3. Assert all tasks are returned
        """
        scheduler = Scheduler()
        
        # Two tasks at the same time
        task1 = Task(name="Feed Dog", duration=10, priority=5, 
                     due_time=datetime(2026, 3, 29, 9, 0))
        task2 = Task(name="Feed Cat", duration=10, priority=4, 
                     due_time=datetime(2026, 3, 29, 9, 0))
        
        tasks = [task1, task2]
        sorted_tasks = scheduler.sort_tasks_by_time(tasks)
        
        # Assert all tasks preserved and both at 9:00
        assert len(sorted_tasks) == 2, "Both tasks should be returned"
        assert all(t.due_time.hour == 9 for t in sorted_tasks), "Both should be at 9:00"


class TestRecurringTasks:
    """Tests for recurring task logic (daily/weekly patterns)."""

    def test_handle_daily_recurring_task(self):
        """
        Test that a daily recurring task creates a new task for the next day.
        
        Steps:
        1. Create a daily recurring task at 9:00
        2. Call scheduler.handle_recurring_task()
        3. Assert next task is 1 day later at same time
        """
        scheduler = Scheduler()
        
        original_task = Task(
            name="Feed Dog",
            duration=10,
            priority=5,
            due_time=datetime(2026, 3, 29, 9, 0),
            recurring="daily"
        )
        
        next_task = scheduler.handle_recurring_task(original_task)
        
        # Assert next task exists and is correct
        assert next_task is not None, "Daily recurring should create next task"
        assert next_task.name == "Feed Dog", "Name should be preserved"
        assert next_task.duration == 10, "Duration should be preserved"
        assert next_task.priority == 5, "Priority should be preserved"
        assert next_task.recurring == "daily", "Recurrence should be preserved"
        assert next_task.due_time == datetime(2026, 3, 30, 9, 0), "Should be 1 day later"

    def test_handle_weekly_recurring_task(self):
        """
        Test that a weekly recurring task creates a new task for the next week.
        
        Steps:
        1. Create a weekly recurring task on Monday at 10:00
        2. Call scheduler.handle_recurring_task()
        3. Assert next task is 7 days later at same time
        """
        scheduler = Scheduler()
        
        original_task = Task(
            name="Vet Visit",
            duration=30,
            priority=5,
            due_time=datetime(2026, 3, 29, 10, 0),  # Sunday
            recurring="weekly"
        )
        
        next_task = scheduler.handle_recurring_task(original_task)
        
        # Assert next task exists and is correct
        assert next_task is not None, "Weekly recurring should create next task"
        assert next_task.due_time == datetime(2026, 4, 5, 10, 0), "Should be 7 days later"
        assert next_task.recurring == "weekly", "Recurrence should be preserved"

    def test_handle_recurring_no_due_time(self):
        """
        Test that a recurring task without due_time returns None (cannot reschedule).
        
        Steps:
        1. Create a daily recurring task with due_time=None
        2. Call scheduler.handle_recurring_task()
        3. Assert it returns None (safe fallback)
        """
        scheduler = Scheduler()
        
        task = Task(
            name="Feed Dog",
            duration=10,
            priority=5,
            due_time=None,
            recurring="daily"
        )
        
        result = scheduler.handle_recurring_task(task)
        
        # Assert safe fallback
        assert result is None, "Cannot reschedule task without due_time"

    def test_handle_non_recurring_task(self):
        """
        Test that a non-recurring task returns None.
        
        Steps:
        1. Create a task with recurring=None
        2. Call scheduler.handle_recurring_task()
        3. Assert it returns None
        """
        scheduler = Scheduler()
        
        task = Task(
            name="One-time Walk",
            duration=30,
            priority=5,
            due_time=datetime(2026, 3, 29, 9, 0),
            recurring=None
        )
        
        result = scheduler.handle_recurring_task(task)
        
        # Assert returns None for non-recurring
        assert result is None, "Non-recurring task should return None"

    def test_handle_invalid_recurring_type(self):
        """
        Test that an invalid recurring type (e.g., 'monthly') returns None gracefully.
        
        Steps:
        1. Create a task with recurring='monthly' (unsupported)
        2. Call scheduler.handle_recurring_task()
        3. Assert it returns None (safe fallback)
        """
        scheduler = Scheduler()
        
        task = Task(
            name="Monthly Checkup",
            duration=20,
            priority=4,
            due_time=datetime(2026, 3, 29, 9, 0),
            recurring="monthly"  # Unsupported
        )
        
        result = scheduler.handle_recurring_task(task)
        
        # Assert safe fallback for invalid type
        assert result is None, "Invalid recurring type should return None"


class TestConflictDetection:
    """Tests for detecting task scheduling conflicts."""

    def test_detect_same_time_conflict(self):
        """
        Test that two tasks at the exact same time are detected as conflicting.
        
        Steps:
        1. Create two tasks at 9:00
        2. Call scheduler.detect_conflicts()
        3. Assert conflict is detected
        """
        scheduler = Scheduler()
        
        task1 = Task(name="Feed Dog", duration=10, priority=5, 
                     due_time=datetime(2026, 3, 29, 9, 0))
        task2 = Task(name="Feed Cat", duration=10, priority=4, 
                     due_time=datetime(2026, 3, 29, 9, 0))
        
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # Assert conflict detected
        assert len(conflicts) == 1, "Should detect 1 conflict"
        assert (task1, task2) in conflicts or (task2, task1) in conflicts, "Should detect task pair"

    def test_detect_overlapping_conflict(self):
        """
        Test that overlapping tasks (with durations) are detected as conflicting.
        
        Steps:
        1. Create task1: 9:00-9:30 (30 min)
        2. Create task2: 9:15-9:45 (30 min)
        3. Call scheduler.detect_conflicts()
        4. Assert overlap is detected
        """
        scheduler = Scheduler()
        
        task1 = Task(name="Walk", duration=30, priority=5, 
                     due_time=datetime(2026, 3, 29, 9, 0))
        task2 = Task(name="Feed", duration=30, priority=5, 
                     due_time=datetime(2026, 3, 29, 9, 15))
        
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # Assert overlap detected (9:00-9:30 overlaps with 9:15-9:45)
        assert len(conflicts) == 1, "Should detect overlapping tasks"

    def test_detect_no_conflict_back_to_back(self):
        """
        Test that back-to-back tasks (touching but not overlapping) are NOT conflicting.
        
        Steps:
        1. Create task1: 9:00-9:30 (30 min)
        2. Create task2: 9:30-10:00 (starts exactly when task1 ends)
        3. Call scheduler.detect_conflicts()
        4. Assert NO conflict is detected
        """
        scheduler = Scheduler()
        
        task1 = Task(name="Walk", duration=30, priority=5, 
                     due_time=datetime(2026, 3, 29, 9, 0))
        task2 = Task(name="Feed", duration=30, priority=5, 
                     due_time=datetime(2026, 3, 29, 9, 30))
        
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # Assert NO conflict (tasks are sequential, not overlapping)
        assert len(conflicts) == 0, "Back-to-back tasks should not conflict"

    def test_detect_no_conflict_tasks_without_time(self):
        """
        Test that tasks without due_time do not create conflicts.
        
        Steps:
        1. Create two tasks with due_time=None
        2. Call scheduler.detect_conflicts()
        3. Assert NO conflict (flexible scheduling)
        """
        scheduler = Scheduler()
        
        task1 = Task(name="Playtime", duration=20, priority=3, due_time=None)
        task2 = Task(name="Grooming", duration=45, priority=2, due_time=None)
        
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # Assert NO conflict (unscheduled tasks don't conflict)
        assert len(conflicts) == 0, "Tasks without due_time should not conflict"

    def test_detect_multiple_conflicts(self):
        """
        Test that multiple conflicts are all detected.
        
        Steps:
        1. Create 3 tasks all at 9:00
        2. Call scheduler.detect_conflicts()
        3. Assert all pairs are detected (3 conflicts: A-B, A-C, B-C)
        """
        scheduler = Scheduler()
        
        task1 = Task(name="Walk", duration=30, priority=5, 
                     due_time=datetime(2026, 3, 29, 9, 0))
        task2 = Task(name="Feed Dog", duration=10, priority=5, 
                     due_time=datetime(2026, 3, 29, 9, 0))
        task3 = Task(name="Feed Cat", duration=10, priority=4, 
                     due_time=datetime(2026, 3, 29, 9, 0))
        
        conflicts = scheduler.detect_conflicts([task1, task2, task3])
        
        # Assert all 3 conflict pairs detected
        assert len(conflicts) == 3, "Should detect 3 conflicts (all pairs)"
