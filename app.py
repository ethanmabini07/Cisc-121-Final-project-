import gradio as gr

def quicksort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quicksort(left) + middle + quicksort(right)


def record_quicksort(text):
    try:
        grades = [int(x.strip()) for x in text.split(",")]

        steps = []
        steps.append(f"Starting: {grades}")

        sorted_arr = quicksort(grades)

        steps.append(f"Sorted: {sorted_arr}")

        return str(sorted_arr), "\n".join(steps)

    except:
        return "Error", "Invalid input. Use: 90, 70, 85"


with gr.Blocks() as app:
    gr.Markdown("# 📊 QuickSort Visualizer ")

    input_box = gr.Textbox(label="Enter numbers (comma separated)")
    output = gr.Textbox(label="Sorted Result")
    steps = gr.Textbox(label="Steps")

    btn = gr.Button("Run QuickSort")

    btn.click(record_quicksort, input_box, [output, steps])

app.launch(server_name="0.0.0.0", server_port=7860)