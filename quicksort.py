def quicksort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quicksort(left) + middle + quicksort(right)


def record_quicksort(grades):
    # simplified version: just return steps of sorted states
    steps = []

    arr = grades[:]

    steps.append({
        "array": arr[:],
        "message": "Starting sort"
    })

    sorted_arr = quicksort(arr)

    steps.append({
        "array": sorted_arr[:],
        "message": "Finished sorting"
    })

    return steps


def grade_to_letter(grade):
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