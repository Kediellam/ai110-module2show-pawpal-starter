"""
Unit tests for PawPal+ Pet Care Management System
"""

import pytest
from pawpal_system import Task, Pet


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
