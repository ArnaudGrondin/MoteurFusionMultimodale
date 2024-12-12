# Elio Genson - nov/dec 2024
# basé sur le code de Michael Ortega

import os
import tkinter as tk
from tkinter import messagebox
from collections import defaultdict


m_window = tk.Tk()
m_canvas = None
result_txt = None
drawn_strokes = []
cb_var_1 = tk.IntVar()
cb_var_2 = tk.IntVar()
model_dict = defaultdict(list)
canvases = []


def drawing(event):
    h = m_canvas.winfo_height()
    drawn_strokes[-1].append([float(event.x), float(h - event.y)])
    m_canvas.create_line(
        drawn_strokes[-1][-2][0],
        h - drawn_strokes[-1][-2][1],
        drawn_strokes[-1][-1][0],
        h - drawn_strokes[-1][-1][1],
    )


def get_models():
    names = []
    datas = []
    global model_dict
    model_dict = {}
    with open("data.dat", "r") as file:
        for line in file:
            name, data = line.split(";")
            if name not in model_dict:
                model_dict.setdefault(name, [])
            model_dict[name].append(eval(data))
            names.append(name)
            datas.append(eval(data))
        return names, datas


def learning():
    text_learned = text_entry.get().strip()
    if len(drawn_strokes) and text_learned:
        with open("data.dat", "a") as file:
            file.write(text_learned + ";" + str(drawn_strokes) + "\n")
            clean()
    else:
        messagebox.showwarning(
            "Empty Input", "Please enter some text before submitting."
        )


def start_drawing(event):
    drawn_strokes.append([[float(event.x), float(m_canvas.winfo_height() - event.y)]])


def create_canvas_with_strokes(name):
    # Create a new canvas and add it to the side panel
    for canvas in canvases:
        canvas.destroy()  # Destroy each canvas
    canvases.clear()  # Clear the list

    # Draw random strokes on the canvas
    model = model_dict[name]

    for strokes in model:
        canva_w = 200
        canva_h = 200
        new_canvas = tk.Canvas(canvas_frame, width=canva_w, height=canva_h, bg="white")
        new_canvas.pack(pady=5)
        canvases.append(new_canvas)

        for stroke in strokes:
            all_x = [point[0] for stroke in strokes for point in stroke]
            all_y = [point[1] for stroke in strokes for point in stroke]
            min_x, max_x = min(all_x), max(all_x)
            min_y, max_y = min(all_y), max(all_y)

            # Calculate scale factors to normalize the strokes within the canvas
            scale_x = canva_w / (max_x - min_x) if max_x != min_x else 1
            scale_y = canva_h / (max_y - min_y) if max_y != min_y else 1
            scale = min(scale_x, scale_y)

            for i in range(len(stroke) - 1):
                x1 = (stroke[i][0] - min_x) * scale
                y1 = canva_h - (stroke[i][1] - min_y) * scale
                x2 = (stroke[i + 1][0] - min_x) * scale
                y2 = canva_h - (stroke[i + 1][1] - min_y) * scale
                new_canvas.create_line(x1, y1, x2, y2, fill="black", width=2)


def stop_drawing(event):
    # print(drawn_strokes)
    pass


def clean():
    global drawn_strokes
    m_canvas.delete("all")
    drawn_strokes = []


def close(event):
    os._exit(os.EX_OK)


# Interactive window
m_window.title("$N Trainer")
m_window.bind("<Escape>", close)
frame_cb = tk.Frame(m_window, borderwidth=2, relief=tk.FLAT)
frame_cb.pack()
text_entry = tk.Entry(frame_cb)
text_entry.pack()

side_panel = tk.Frame(m_window, width=200, relief=tk.SUNKEN)
side_panel.pack(side=tk.LEFT, fill=tk.X)

canvas = tk.Canvas(side_panel, width=200)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(side_panel, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

menu_label = tk.Label(side_panel, text="Menu", font=("Arial", 12, "bold"))
menu_label.pack(pady=10)

models, datas = get_models()
# Create buttons based on the list of names and add to the side panel
for name in set(models):
    button = tk.Button(
        side_panel, text=name, command=lambda n=name: create_canvas_with_strokes(n)
    )
    button.pack(fill=tk.X, padx=5, pady=2)

canvas_frame = tk.Frame(side_panel)
canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

m_canvas = tk.Canvas(m_window, width=500, height=500, background="white")
m_canvas.pack()
m_canvas.bind("<ButtonPress-1>", start_drawing)
m_canvas.bind("<ButtonRelease-1>", stop_drawing)
m_canvas.bind("<B1-Motion>", drawing)

frame_bt = tk.Frame(m_window, borderwidth=2, relief=tk.FLAT)
frame_bt.pack()
tk.Button(frame_bt, text="Train", command=learning).pack(side=tk.RIGHT)
tk.Button(frame_bt, text="Clean", command=clean).pack(side=tk.LEFT)

result_txt = tk.Label(m_window, text="")
result_txt.pack()

m_window.mainloop()
