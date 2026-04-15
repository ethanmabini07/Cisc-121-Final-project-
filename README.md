

# Grade Sorter — Quick Sort Visualizer

An interactive Python app that demonstrates the **Quick Sort algorithm** by applying it to a real computing problem: **ranking student grades**.

Built with Streamlit and Plotly. Runs live on Hugging Face Spaces.

---

## What it does

- Enter up to 15 student names and grades (or generate a random class)
- Watch Quick Sort work through the array **step by step**
- Each step highlights the **pivot** (gold), elements being **compared** (teal), and elements in their **final sorted position** (green)
- Step through manually or use **auto-play** at adjustable speeds
- See the final **ranked leaderboard** with letter grades when sorting is complete

---

## Algorithm

**Quick Sort** — Lomuto partition scheme  
Average time complexity: **O(n log n)**  
Space complexity: **O(log n)** (call stack)

The pivot is always the last element of the current sub-array. For each partition step:
1. Scan the sub-array left to right
2. Swap elements smaller than the pivot to the left side
3. Place the pivot in its final position
4. Recurse on the left and right halves

---

## Running locally

```bash
git clone https://github.com/YOUR_USERNAME/grade-sorter
cd grade-sorter
pip install -r requirements.txt
streamlit run app.py
```

---

## Project structure

```
grade-sorter/
├── app.py           # Streamlit UI and controls
├── quicksort.py     # Algorithm + step recorder
├── visualizer.py    # Plotly chart builder
├── requirements.txt
└── README.md


---

## Deploying to Hugging Face

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Choose **Streamlit** as the SDK
3. Push this repo to the Space's Git remote
4. Hugging Face builds and deploys automatically

---

## Testing

The core algorithm is tested by verifying that the final step's array matches Python's built-in `sorted()` result:

```python
from quicksort import record_quicksort

grades = [72, 88, 61, 95, 47, 83]
steps = record_quicksort(grades)
assert steps[-1]["array"] == sorted(grades)
print("All tests passed.")
```


