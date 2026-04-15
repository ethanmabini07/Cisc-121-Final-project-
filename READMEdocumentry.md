# Grade Sorter — QuickSort Visualizer

## 📌 Problem Overview
This project helps users understand how the QuickSort algorithm works by visualizing how a list of student grades is sorted step by step. The dataset represents exam or assignment grades (integers from 0–100), and the goal is to sort them from lowest to highest while showing how the algorithm makes decisions.

---

## 🧠 Why QuickSort Fits This Problem

QuickSort is a good fit for this problem because:

- Grades are stored as a list of numbers, which is exactly what QuickSort works with.
- It efficiently handles unsorted data and large lists.
- It uses a divide-and-conquer approach, making it easier to break the problem into visible steps for learning.

### Assumptions:
- All input values are valid integers between 0 and 100.
- The list is initially unsorted.
- Duplicate grades are allowed and handled normally.

---

## ⚙️ Preconditions

Before sorting:
- The input must be a comma-separated list of numbers (e.g., `90, 70, 85, 60`).
- The values must be numeric.

The app enforces this by:
- Splitting the input string into values.
- Converting each value into an integer.
- Showing an error message if conversion fails.

No pre-sorting is required.

---

## 👀 What the User Sees During Simulation

During the simulation, the user sees:

- The original list before sorting begins
- The pivot selection at each step
- How the list is divided into left and right sublists
- The final sorted result

### Highlight meanings:
- **Pivot** → the reference value used to split the list
- **Left side** → values smaller than the pivot
- **Right side** → values greater than the pivot
- **Final state** → fully sorted list

This helps users understand how QuickSort breaks a problem into smaller parts instead of sorting everything at once.

---

## 🧩 Computational Thinking Plan

### 1. Decomposition
The algorithm is broken into smaller steps:
- Choose a pivot
- Split the list into left, middle, and right parts
- Recursively sort each part
- Combine results into a final sorted list

---

### 2. Pattern Recognition
QuickSort repeatedly:
- Selects a pivot
- Compares each element to the pivot
- Groups elements into smaller or larger values
- Applies the same process to sublists

This repeating structure is what makes it recursive.

---

### 3. Abstraction
Shown to the user:
- Input list
- Pivot selection
- Sorted output

Hidden from the user:
- Internal recursion calls
- Memory handling
- Sublist creation process

This keeps the visualization simple and focused on learning.

---

### 4. Algorithm Design (Input → Process → Output)

**Input:**
- A string of comma-separated numbers from the user

**Process:**
- Convert input into a list of integers
- Apply QuickSort recursively
- Record key steps (start, pivot selection, final result)

**Output:**
- Sorted list
- Step-by-step explanation of sorting process

---

## 🔄 Flowchart (look at code side)

START
  ↓
User enters comma-separated grades
  ↓
Convert input string → list of integers
  ↓
Is list valid?
  ├── No → Show error message → END
  └── Yes
         ↓
    QuickSort starts
         ↓
    Choose pivot (middle element)
         ↓
    Split list into:
        - Left (smaller than pivot)
        - Middle (equal to pivot)
        - Right (greater than pivot)
         ↓
    Recursively apply QuickSort to Left and Right
         ↓
    Combine: Left + Middle + Right
         ↓
    Return sorted list
         ↓
Display:
    - Sorted result
    - Steps/messages
  ↓
END