# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling
This project now includes an improved scheduling system. The scheduler can now sort tasks by due time, filter tasks by pet or completion status, and detect scheduling conflicts to prevent overlapping events. It also supports recurring tasks (daily and weekly), automatically generating the next time a task is completed.

## Testing PawPal+
To run the tests:
python -m pytest
The test suite covers:
- Conflict detection for tasks scheduled at the same time
- Sorting tasks in chronological order based on due time
- Recurring task logic
- Edge cases such as missing due times and empty task lists
Confidence Level: (4/5)

## Features

### 📅 Intelligent Task Scheduling
- **Priority-Based Planning**: The `Scheduler` generates daily plans by selecting high-priority tasks that fit within the owner's available time
- **Chronological Sorting**: Tasks can be sorted by due time (earliest first) via `sort_tasks_by_time()`, with flexible, unscheduled tasks placed at the end
- **Flexible Status Filtering**: Filter tasks by completion status using `filter_tasks_by_status()` to view pending or completed items independently

### ⏰ Real-Time Conflict Detection
- **Automatic Overlap Detection**: The `detect_conflicts()` method identifies when two tasks are scheduled at overlapping times and alerts the user
- **Time-Safe Validation**: Handles edge cases gracefully, including tasks without scheduled times, back-to-back tasks (which don't conflict), and concurrent multi-task scenarios
- **Temporal Collision Analysis**: The `Task.is_conflicting()` method uses precise timestamp arithmetic to detect even partial overlaps based on duration

### 🔄 Recurring Task Management
- **Daily & Weekly Patterns**: Support for tasks that repeat daily or weekly using Python's `timedelta` for precise date arithmetic via `handle_recurring_task()`
- **Automatic Generation**: Creates the next occurrence of a recurring task with all properties preserved (name, duration, priority, recurrence type)
- **Safe Rescheduling**: Gracefully handles invalid scenarios—returns `None` for tasks without due times or unsupported recurrence types

### 🎯 Advanced Filtering & Composition
- **Pet-Based Filtering**: View and manage tasks specific to each pet via `filter_tasks_by_pet()`, enabling per-pet scheduling
- **Composable Operations**: Multiple filtering and sorting methods return `List[Task]`, allowing method chaining for complex queries
- **Aggregate Task Management**: `Owner.get_all_tasks()` aggregates tasks across all pets for holistic planning

### 💻 Interactive User Interface
- **Streamlit Integration**: Clean, responsive web interface built with Streamlit for managing owners, pets, and tasks
- **Session State Persistence**: Uses `st.session_state` to maintain application state across user interactions without data loss
- **Real-Time Updates**: Task additions, sorting results, and scheduling conflicts display instantly with reactive UI updates

### 📊 Schedule Explanation & Reporting
- **Human-Readable Plans**: The `explain_plan()` method generates clear, numbered schedules with task details, durations, and total time calculations
- **Task Visibility**: Built-in `__str__()` formatting displays task status (✓ complete, ○ pending), priority, time, and recurrence information
- **Duration Analytics**: Automatically computes total scheduled time to help owners understand time allocation across tasks

## Testing

Run the comprehensive test suite:
```bash
pytest tests/test_pawpal.py -v
```

### Test Coverage

The test suite (15 tests) validates:
- ✓ **Sorting**: Chronological ordering, handling of unscheduled tasks, same-time task preservation
- ✓ **Conflict Detection**: Same-time conflicts, overlapping durations, back-to-back non-conflicts, multi-task scenarios
- ✓ **Recurring Tasks**: Daily/weekly recurrence generation, missing due times, invalid recurrence types
- ✓ **Status Filtering**: Completion status filtering, task aggregation
- ✓ **Edge Cases**: None-type handling, empty lists, boundary conditions

**Test Result**: 15/15 passing ✓

## 📸 Demo

<a href="/course_images/ai110/195534.png" target="_blank">
<img src='/course_images/ai110/195534.png'
title='PawPal App'
width=''
alt='PawPal App'
class='center-block' />
</a>

