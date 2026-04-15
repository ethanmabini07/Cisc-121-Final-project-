"""
app.py
------
Grade Sorter — Quick Sort Visualizer
CISC 121 Project | Queen's University

A Gradio app that demonstrates Quick Sort by ranking student grades.
Users can enter grades, step through the sort visually, or jump to
any step using the slider.

Run locally:  python app.py
Deploy to:    Hugging Face Spaces (SDK: Gradio)
"""

import random
import gradio as gr
import plotly.graph_objects as go

from quicksort import record_quicksort, grade_to_letter


# ── Color palette ──────────────────────────────────────────────────────────────
COLOR_DEFAULT = "#6C8EBF"   # unsorted element
COLOR_PIVOT   = "#F5A623"   # current pivot
COLOR_COMPARE = "#2EC4B6"   # element being compared
COLOR_SORTED  = "#57CC99"   # confirmed in final position


# ── Chart builder ──────────────────────────────────────────────────────────────

def build_chart(step: dict, names: list) -> go.Figure:
    """
    Build a Plotly bar chart for one step snapshot.

    Each bar = one student. Bar color encodes the algorithm state:
      Gold  = pivot being placed
      Teal  = element being compared against pivot
      Green = confirmed in final sorted position
      Blue  = not yet touched in this pass

    Args:
        step:  A step dict from record_quicksort().
        names: Student names matching the original grade order.

    Returns:
        A Plotly Figure for gr.Plot().
    """
    arr        = step["array"]
    pivot_idx  = step["pivot_idx"]
    left       = step["left"]
    right      = step["right"]
    sorted_set = step["sorted"]
    n          = len(arr)

    # Assign a color to each bar based on its role this step
    colors = []
    for i in range(n):
        if i in sorted_set:
            colors.append(COLOR_SORTED)
        elif i == pivot_idx:
            colors.append(COLOR_PIVOT)
        elif i in (left, right):
            colors.append(COLOR_COMPARE)
        else:
            colors.append(COLOR_DEFAULT)

    fig = go.Figure(
        go.Bar(
            x=list(range(n)),
            y=arr,
            marker_color=colors,
            text=[str(v) for v in arr],
            textposition="outside",
            hovertemplate="<b>%{customdata}</b><extra></extra>",
            customdata=[
                f"{names[i]}: {arr[i]} ({grade_to_letter(arr[i])})"
                for i in range(n)
            ],
        )
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(n)),
            ticktext=names,
            tickfont=dict(size=12),
        ),
        yaxis=dict(range=[0, 115], title="Grade", gridcolor="#eeeeee"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=40, b=60, l=50, r=20),
        height=420,
        showlegend=False,
        title=dict(
            text=(
                "<span style='color:#F5A623'>■ Pivot</span>  "
                "<span style='color:#2EC4B6'>■ Comparing</span>  "
                "<span style='color:#57CC99'>■ Sorted</span>  "
                "<span style='color:#6C8EBF'>■ Unsorted</span>"
            ),
            font=dict(size=13),
            x=0,
        ),
    )
    return fig


# ── Input parsing ──────────────────────────────────────────────────────────────

def parse_input(names_raw: str, grades_raw: str):
    """
    Parse and validate the user's text input.

    Names: comma-separated strings.
    Grades: comma-separated integers 0-100.

    Returns:
        (names list, grades list) on success.
        Raises gr.Error with a helpful message on any problem.
    """
    names = [n.strip() for n in names_raw.split(",") if n.strip()]

    if len(names) < 2:
        raise gr.Error("Please enter at least 2 student names, separated by commas.")
    if len(names) > 20:
        raise gr.Error("Please enter 20 or fewer students.")

    grade_parts = [g.strip() for g in grades_raw.split(",") if g.strip()]

    if len(grade_parts) != len(names):
        raise gr.Error(
            f"You entered {len(names)} names but {len(grade_parts)} grades. "
            "These counts must match."
        )

    grades = []
    for i, g in enumerate(grade_parts):
        if not g.isdigit():
            raise gr.Error(
                f"Grade for '{names[i]}' must be a whole number, got '{g}'."
            )
        val = int(g)
        if not 0 <= val <= 100:
            raise gr.Error(
                f"Grade for '{names[i]}' must be between 0 and 100, got {val}."
            )
        grades.append(val)

    return names, grades


# ── Sort runner ────────────────────────────────────────────────────────────────

def run_sort(names_raw: str, grades_raw: str):
    """
    Parse inputs, run Quick Sort, return first step to display.

    Returns 7 values matching the Gradio output component list.
    """
    names, grades = parse_input(names_raw, grades_raw)
    steps = record_quicksort(grades)
    total = len(steps)

    fig = build_chart(steps[0], names)
    msg = f"**Step 1 of {total}:** {steps[0]['message']}"

    return (
        fig,
        msg,
        0,            # current step index
        steps,        # full step list (hidden state)
        names,        # names list (hidden state)
        gr.update(value=0, maximum=total - 1),
        "",           # ranking (empty until final step)
    )


# ── Step navigation ────────────────────────────────────────────────────────────

def go_to_step(step_idx: int, steps: list, names: list):
    """Render chart + message for any step index. Returns 4 outputs."""
    if not steps:
        raise gr.Error("Run the sort first by clicking ▶ Start Sort.")

    step_idx = max(0, min(step_idx, len(steps) - 1))
    step  = steps[step_idx]
    total = len(steps)
    fig   = build_chart(step, names)
    msg   = f"**Step {step_idx + 1} of {total}:** {step['message']}"

    ranking = ""
    if step_idx == total - 1:
        ranking = build_ranking_table(step["array"], names)

    return fig, msg, step_idx, ranking


def step_forward(step_idx, steps, names):
    return go_to_step(min(step_idx + 1, len(steps) - 1) if steps else 0, steps, names)

def step_back(step_idx, steps, names):
    return go_to_step(max(step_idx - 1, 0), steps, names)

def jump_first(steps, names):
    return go_to_step(0, steps, names)

def jump_last(steps, names):
    return go_to_step(len(steps) - 1, steps, names)

def slider_moved(val, steps, names):
    return go_to_step(int(val), steps, names)


# ── Random data generator ──────────────────────────────────────────────────────

def generate_random():
    """Return a random set of names and grades as pre-filled strings."""
    pool = [
        "Alice", "Bob", "Carol", "David", "Eva", "Frank", "Grace",
        "Hiro", "Isla", "James", "Keiko", "Liam", "Maya", "Nour", "Oscar",
    ]
    chosen = random.sample(pool, 8)
    grades = [random.randint(40, 100) for _ in chosen]
    return ", ".join(chosen), ", ".join(str(g) for g in grades)


# ── Final ranking table ────────────────────────────────────────────────────────

def build_ranking_table(final_array: list, names: list) -> str:
    """Build a markdown ranking table from the sorted array."""
    ranked = sorted(zip(names, final_array), key=lambda x: x[1], reverse=True)
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    lines = [
        "### 🏆 Final Rankings\n",
        "| Rank | Student | Grade | Letter |",
        "|------|---------|-------|--------|",
    ]
    for i, (name, grade) in enumerate(ranked, 1):
        medal = medals.get(i, f"#{i}")
        lines.append(f"| {medal} | {name} | {grade} | {grade_to_letter(grade)} |")

    return "\n".join(lines)


# ── Gradio UI ──────────────────────────────────────────────────────────────────

with gr.Blocks(title="Grade Sorter — Quick Sort Visualizer", theme=gr.themes.Soft()) as demo:

    # Hidden state (not visible, just stores values between clicks)
    step_index  = gr.State(0)
    all_steps   = gr.State([])
    names_state = gr.State([])

    gr.Markdown("""
# 📊 Grade Sorter — Quick Sort Visualizer
**CISC 121 | Queen's University**

Enter student names and grades below, then step through Quick Sort to see how
it ranks the class. Each bar is a student — the colours show what the algorithm
is doing at each moment.
    """)

    # ── Data input ──
    with gr.Row():
        with gr.Column(scale=2):
            names_input = gr.Textbox(
                label="Student names (comma-separated)",
                placeholder="Alice, Bob, Carol, David, Eva",
                info="Enter 2–20 names.",
            )
        with gr.Column(scale=2):
            grades_input = gr.Textbox(
                label="Grades 0–100 (comma-separated, same order as names)",
                placeholder="72, 88, 61, 95, 47",
                info="One whole number per student.",
            )

    with gr.Row():
        random_btn = gr.Button("🎲 Generate random class", variant="secondary")
        sort_btn   = gr.Button("▶ Start Sort", variant="primary")

    gr.Markdown("---")

    # ── Visualization ──
    step_msg = gr.Markdown("*Enter student data above and click **▶ Start Sort** to begin.*")
    chart    = gr.Plot(label="")

    step_slider = gr.Slider(
        minimum=0, maximum=1, step=1, value=0,
        label="Jump to step",
        interactive=True,
    )

    with gr.Row():
        first_btn = gr.Button("⏮ First", scale=1)
        prev_btn  = gr.Button("◀ Prev",  scale=1)
        next_btn  = gr.Button("Next ▶",  scale=1)
        last_btn  = gr.Button("Last ⏭", scale=1)

    ranking_output = gr.Markdown("")

    # ── Explainer ──
    with gr.Accordion("ℹ️ How Quick Sort works", open=False):
        gr.Markdown("""
**Quick Sort** is a divide-and-conquer algorithm with average time complexity **O(n log n)**.

**In plain English:**
1. Pick a **pivot** (this app uses the last element of each sub-array — the Lomuto scheme).
2. **Partition**: scan left to right and move all grades smaller than the pivot to its left.
3. Place the pivot in its **final position** — it never moves again (shown in green).
4. **Recurse** on the left and right halves independently.
5. **Base case**: a sub-array of length 0 or 1 is already sorted — stop.

**Why it suits the grade-ranking problem:**
- Grades are integers — comparing two of them is instant.
- Quick Sort performs well on randomized data, which is typical for a real class.
- It sorts in place, so it works efficiently regardless of class size.
- The partition step is highly visual: you can watch grades move around the pivot in real time.

**Worst case** is O(n²) when the pivot is always the minimum or maximum (e.g., already-sorted input).
This app uses random data by default, so worst-case is very unlikely.
        """)

    # ── Wire up events ─────────────────────────────────────────────────────────

    nav_out = [chart, step_msg, step_index, ranking_output]

    sort_btn.click(
        fn=run_sort,
        inputs=[names_input, grades_input],
        outputs=[chart, step_msg, step_index, all_steps, names_state, step_slider, ranking_output],
    )
    random_btn.click(fn=generate_random, inputs=[], outputs=[names_input, grades_input])
    next_btn.click(fn=step_forward, inputs=[step_index, all_steps, names_state], outputs=nav_out)
    prev_btn.click(fn=step_back,    inputs=[step_index, all_steps, names_state], outputs=nav_out)
    first_btn.click(fn=jump_first,  inputs=[all_steps, names_state],             outputs=nav_out)
    last_btn.click(fn=jump_last,    inputs=[all_steps, names_state],             outputs=nav_out)
    step_slider.change(fn=slider_moved, inputs=[step_slider, all_steps, names_state], outputs=nav_out)


if __name__ == "__main__":
    demo.launch()
