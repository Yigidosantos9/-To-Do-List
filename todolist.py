from tkinter import *
from PIL import Image, ImageTk
import json
import os

def load_data():
    global tasks_list, current_theme
    if os.path.exists('data.json'):
        with open('data.json', 'r') as file:
            data = json.load(file)
            tasks_list = data.get('tasks_list', [])
            theme_name = data.get('theme', 'light')
            current_theme = light_theme if theme_name == 'light' else dark_theme
    else:
        tasks_list = []
        current_theme = light_theme

def save_data():
    data = {
        'tasks_list': tasks_list,
        'theme': 'light' if current_theme == light_theme else 'dark'
    }
    with open('data.json', 'w') as file:
        json.dump(data, file)

def add_task():
    task = entry_task.get()
    if task != "":
        tasks_list.append({"task": task, "completed": False})
        update_task_list(animation=True)
        entry_task.delete(0, END)
        save_data()

def delete_task():
    global task_widgets
    selected_indices = [i for i, (task_frame, var, _) in enumerate(task_widgets) if var.get()]
    for index in selected_indices[::-1]:
        del tasks_list[index]
    update_task_list(animation=True)
    save_data()

def update_task_list(animation=False):
    for widget in frame_tasks.winfo_children():
        widget.destroy()
    
    global task_widgets
    task_widgets = []
    
    for task_info in tasks_list + [{"task": "", "completed": False}] * (6 - len(tasks_list)):
        task = task_info["task"]
        completed = task_info["completed"]
        
        highlight_color = current_theme['highlight']
        
        task_frame = Frame(frame_tasks, bg=current_theme['frame_bg'], highlightbackground=highlight_color, highlightthickness=1, padx=5, pady=5)
        task_frame.pack(fill=X, pady=5, padx=20)
        if animation:
            animate_widget(task_frame, direction="in")
        
        check_var = BooleanVar(value=completed)
        icon = check_icon if completed else empty_icon
        check_button = Button(task_frame, image=icon, bg=current_theme['frame_bg'], command=lambda var=check_var, task_info=task_info: toggle_task(var, task_info))
        check_button.pack(side=LEFT, padx=5)
        
        task_label = Label(task_frame, text=task if task else " ________________ ", font=font_regular, bg=current_theme['frame_bg'], fg=current_theme['fg'])
        task_label.pack(side=LEFT, fill=X, expand=True)
        
        if task:
            edit_button = Button(task_frame, text="Edit", command=lambda t=task_info: edit_task(t), font=font_regular, bg=current_theme['edit_button_bg'], fg=current_theme['fg'], bd=0, padx=10, pady=5)
            edit_button.pack(side=LEFT, padx=5)
        
        if completed:
            task_label.config(font=font_regular + ("overstrike",), fg='red')
        
        task_widgets.append((task_frame, check_var, task_label))

def animate_widget(widget, direction="in"):
    alpha = 0
    if direction == "in":
        while alpha < 1:
            alpha += 0.1
            widget.update()
            widget.winfo_toplevel().after(10, lambda: widget.config(bg=f"#{int(alpha * 255):02x}0000"))
    elif direction == "out":
        while alpha > 0:
            alpha -= 0.1
            widget.update()
            widget.winfo_toplevel().after(10, lambda: widget.config(bg=f"#{int(alpha * 255):02x}0000"))

def toggle_task(var, task_info):
    task_info["completed"] = not task_info["completed"]
    update_task_list()
    save_data()

def edit_task(task_info):
    edit_window = Toplevel(window)
    edit_window.title("Edit Task")
    edit_window.geometry("300x200")
    
    entry_edit_task = Entry(edit_window, width=30, font=("Verdana", 14))
    entry_edit_task.pack(pady=20)
    entry_edit_task.insert(0, task_info["task"])
    
    def save_task():
        new_task = entry_edit_task.get()
        if new_task != "":
            task_info["task"] = new_task
            update_task_list()
            edit_window.destroy()
            save_data()
    
    button_save_task = Button(edit_window, text="Save", command=save_task, font=("Verdana", 12), bg=current_theme['save_button_bg'], fg=current_theme['fg'], bd=0, padx=10, pady=5)
    button_save_task.pack(pady=20)

def switch_theme():
    global current_theme
    if current_theme == light_theme:
        current_theme = dark_theme
        button_switch_theme.config(image=moon_icon)
        button_frame.config(bg=dark_theme['bg'])
    else:
        current_theme = light_theme
        button_switch_theme.config(image=sun_icon)
        button_frame.config(bg=light_theme['bg'])
    update_theme()
    save_data()

def update_theme():
    window.config(bg=current_theme['bg'])
    label.config(bg=current_theme['bg'], fg=current_theme['fg'])
    entry_task.config(bg=current_theme['entry_bg'], fg=current_theme['fg'])
    button_add_task.config(bg=current_theme['add_button_bg'], fg=current_theme['fg'], activebackground=current_theme['add_button_active_bg'], image=add_icon)
    button_delete_task.config(bg=current_theme['delete_button_bg'], fg=current_theme['fg'], activebackground=current_theme['delete_button_active_bg'], image=delete_icon)
    button_switch_theme.config(bg=current_theme['switch_button_bg'], fg=current_theme['fg'], activebackground=current_theme['switch_button_active_bg'])
    update_task_list()
    update_frame_colors()

def update_frame_colors():
    highlight_color = current_theme['highlight']
    for task_frame, _, _ in task_widgets:
        task_frame.config(highlightbackground=highlight_color, bg=current_theme['frame_bg'])

window = Tk()
window.geometry("600x800")
icon = PhotoImage(file="C:\\Users\\Yiğit\\Desktop\\x\\Fotoğraflar\\Coding photos\\to-do.png")
window.iconphoto(True, icon)
window.title("To-do List App by Yiğidosantos")

# İkonları yükleme
icon1 = Image.open("C:\\Users\\Yiğit\\Desktop\\x\\Fotoğraflar\\Coding photos\\plus.png")
add_icon = ImageTk.PhotoImage(icon1.resize((30, 30), Image.LANCZOS))

icon2 = Image.open("C:\\Users\\Yiğit\\Desktop\\x\\Fotoğraflar\\Coding photos\\trash.png")
delete_icon = ImageTk.PhotoImage(icon2.resize((30, 30), Image.LANCZOS))

icon3 = Image.open("C:\\Users\\Yiğit\\Desktop\\x\\Fotoğraflar\\Coding photos\\sun.png")
sun_icon = ImageTk.PhotoImage(icon3.resize((30, 30), Image.LANCZOS))

icon4 = Image.open("C:\\Users\\Yiğit\\Desktop\\x\\Fotoğraflar\\Coding photos\\moon.png")
moon_icon = ImageTk.PhotoImage(icon4.resize((30, 30), Image.LANCZOS))

icon5 = Image.open("C:\\Users\\Yiğit\\Desktop\\x\\Fotoğraflar\\Coding photos\\check.png")
check_icon = ImageTk.PhotoImage(icon5.resize((30, 30), Image.LANCZOS))

icon6 = Image.open("C:\\Users\\Yiğit\\Desktop\\x\\Fotoğraflar\\Coding photos\\empty.png")
empty_icon = ImageTk.PhotoImage(icon6.resize((30, 30), Image.LANCZOS))

font_bold = ("Verdana", 18, "bold")
font_regular = ("Verdana", 18)

light_theme = {
    'bg': '#ebdaae',
    'fg': 'black',
    'frame_bg': '#f7eed7',
    'entry_bg': 'white',
    'add_button_bg': '#4CAF50',
    'add_button_active_bg': '#45a049',
    'delete_button_bg': '#f44336',
    'delete_button_active_bg': '#e57373',
    'switch_button_bg': '#6A5ACD',
    'switch_button_active_bg': '#836FFF',
    'edit_button_bg': '#FFA500',
    'save_button_bg': '#4CAF50',
    'highlight': '#ccc'
}

dark_theme = {
    'bg': '#2e2e2e',
    'fg': 'white',
    'frame_bg': '#3e3e3e',
    'entry_bg': '#4e4e4e',
    'add_button_bg': '#4CAF50',
    'add_button_active_bg': '#45a049',
    'delete_button_bg': '#f44336',
    'delete_button_active_bg': '#e57373',
    'switch_button_bg': '#6A5ACD',
    'switch_button_active_bg': '#836FFF',
    'edit_button_bg': '#FFA500',
    'save_button_bg': '#4CAF50',
    'highlight': '#3e3e3e'
}

load_data()

labelPhoto = PhotoImage(file="C:\\Users\\Yiğit\\Desktop\\x\\Fotoğraflar\\Coding photos\\ayıran çizgi.png")
label = Label(window,
              text="• THINGS TO DO • ",
              font=font_bold,
              fg=current_theme['fg'],
              bg=current_theme['bg'],
              relief=RAISED,
              bd=10,
              image=labelPhoto,
              compound='bottom')
label.pack(pady=10)

frame_tasks = Frame(window, bg=current_theme['bg'])
frame_tasks.pack(pady=10)

entry_task = Entry(window, width=40, font=('Verdana', 14), bg=current_theme['entry_bg'], fg=current_theme['fg'])
entry_task.pack(pady=10)

button_frame = Frame(window, bg=current_theme['bg'])
button_frame.pack(pady=10)

button_add_task = Button(button_frame, text="Add Task", command=add_task, font=('Verdana', 12), bg=current_theme['add_button_bg'], fg=current_theme['fg'], activebackground=current_theme['add_button_active_bg'], bd=0, padx=20, pady=10, image=add_icon, compound=LEFT)
button_add_task.pack(side=LEFT, padx=10)

button_delete_task = Button(button_frame, text="Delete Task", command=delete_task, font=('Verdana', 12), bg=current_theme['delete_button_bg'], fg=current_theme['fg'], activebackground=current_theme['delete_button_active_bg'], bd=0, padx=20, pady=10, image=delete_icon, compound=LEFT)
button_delete_task.pack(side=LEFT, padx=10)

button_switch_theme = Button(window, text="Switch Theme", command=switch_theme, font=('Verdana', 12), bg=current_theme['switch_button_bg'], fg=current_theme['fg'], activebackground=current_theme['switch_button_active_bg'], bd=0, padx=20, pady=10, image=sun_icon, compound=LEFT)
button_switch_theme.pack(pady=10)

update_task_list()

window.config(bg=current_theme['bg'])
window.mainloop()
