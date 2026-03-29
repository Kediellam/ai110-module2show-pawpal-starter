# PawPal+ Project Reflection

## 1. System Design
Three core actions a user should be able to perform are:
1. Create and manage care tasks
The user can add daily tasks and each task can include details like priority and duration.
2. Add and manage pets
The user can create a pet profile for each pet and they can view or update pet information as needed.
3. Generate and view a daily schedule
The system will create a daily plan based on task priority and scheduling constraints. The user can view the plan and see why tasks were ordered that way.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
My initial UML design included four main classes:
The Task class represents a specific action, such as feeding, walking, or medication. 
The Owner class manages user information and their pets.
The Scheduler class is responsible for generating a daily plan. 
The Pet class represents an individual pet and stores attributes such as name, type, and age.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
One important change was recognizing the need for unique identifiers for both Pet and Task objects. At first, I used names to find things and remove them, but this can be problematic if more than one pet or task has the same name. Adding unique IDs to objects would make looking them up more accurate and allow more users. I also saw that my method for finding Task conflicts was missing some parts because it relied on optional due_time values. In situations where time information is missing, this made it hard to see how to handle conflicts. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One tradeoff in my scheduler is between simplicity and making sure that conflicts are handled correctly. My current implementation only checks for exact matches in task start times (due_time) to identify conflicts. This tradeoff is reasonable for this scenario because the project prioritizes clarity, maintainability, and design that is easy for beginners over full real-world scheduling complexity.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
