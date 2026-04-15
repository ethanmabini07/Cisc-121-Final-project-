"""
quicksort.py
------------
Implements Quick Sort and records every step of the process
so the visualizer can replay them one at a time.

Each 'step' is a snapshot dict:
    {
        'array':    list of current grade values,
        'pivot_idx': index of the pivot element (or None),
        'left':     index scanning from the left (or None),
        'right':    index scanning from the right (or None),
        'sorted':   set of indices that are fully in their final position,
        'message':  human-readable description of what just happened
    }
"""


def record_quicksort(grades: list[int]) -> list[dict]:
    """
    Run Quick Sort on a copy of `grades` and return the full list
    of steps for playback.

    Args:
        grades: A list of integer grade values (0–100).

    Returns:
        A list of step dicts, one per meaningful state change.
    """
    arr = grades[:]
    steps = []
    sorted_indices = set()

    def snapshot(pivot_idx=None, left=None, right=None, message=""):
        steps.append({
            "array": arr[:],
            "pivot_idx": pivot_idx,
            "left": left,
            "right": right,
            "sorted": set(sorted_indices),
            "message": message,
        })

    def partition(low: int, high: int) -> int:
        """
        Lomuto partition scheme.
        Picks arr[high] as pivot, puts it in its correct position,
        and returns that position.
        """
        pivot = arr[high]
        snapshot(
            pivot_idx=high,
            message=f"Picked pivot: {pivot} (index {high})"
        )

        i = low - 1  # pointer for the smaller element

        for j in range(low, high):
            snapshot(
                pivot_idx=high,
                left=i + 1,
                right=j,
                message=f"Comparing grade {arr[j]} at index {j} with pivot {pivot}"
            )
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                if i != j:
                    snapshot(
                        pivot_idx=high,
                        left=i,
                        right=j,
                        message=f"Swapped {arr[j]} and {arr[i]} (index {j} ↔ {i})"
                    )

        # Place the pivot in its correct spot
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        pivot_final = i + 1
        sorted_indices.add(pivot_final)
        snapshot(
            pivot_idx=pivot_final,
            message=f"Pivot {pivot} is now in its final position at index {pivot_final}"
        )
        return pivot_final

    def quicksort(low: int, high: int):
        if low < high:
            pi = partition(low, high)
            quicksort(low, pi - 1)
            # Mark left side fully sorted when it's a single element
            if low == pi - 1:
                sorted_indices.add(low)
            quicksort(pi + 1, high)
            if pi + 1 == high:
                sorted_indices.add(high)
        elif low == high:
            sorted_indices.add(low)

    snapshot(message="Starting Quick Sort on student grades")
    quicksort(0, len(arr) - 1)

    # Final state — everything sorted
    sorted_indices.update(range(len(arr)))
    snapshot(message="Sorting complete! All grades are in order.")

    return steps


def grade_to_letter(grade: int) -> str:
    """Convert a numeric grade to a letter grade."""
    if grade >= 90:
        return "A"
    elif grade >= 80:
        return "B"
    elif grade >= 70:
        return "C"
    elif grade >= 60:
        return "D"
    else:
        return "F"
