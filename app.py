import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk

# Function to find venv directories
def find_venvs(start_path=os.path.expanduser("~")):
    venv_list = []
    for root, dirs, files in os.walk(start_path):
        for d in dirs:
            if d in ("venv", ".venv", "env"):
                full_path = os.path.join(root, d)
                venv_list.append(full_path)
    return venv_list

# Function to calculate folder size
def get_size(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            try:
                total += os.path.getsize(os.path.join(dirpath, f))
            except Exception:
                pass
    return total

# Refresh the full list of venvs
def refresh_list():
    global all_venvs
    all_venvs = find_venvs()
    update_list()

# Update treeview based on search filter
def update_list(event=None):
    search_term = search_var.get().lower()
    for item in tree.get_children():
        tree.delete(item)
    for v in all_venvs:
        if search_term in v.lower():
            size_mb = get_size(v) / (1024 * 1024)
            # Insert with color tags
            if size_mb > 500:
                tag = 'large'
            elif size_mb > 100:
                tag = 'medium'
            else:
                tag = 'small'
            tree.insert("", tk.END, values=(v, f"{size_mb:.2f} MB"), tags=(tag,))

# Show contents of selected venv
def show_contents(event=None):
    selected = tree.selection()
    if not selected:
        return
    # Show contents of first selected venv
    venv_path = tree.item(selected[0])['values'][0]
    content_listbox.delete(0, tk.END)
    for root, dirs, files in os.walk(venv_path):
        for d in dirs:
            rel_path = os.path.relpath(os.path.join(root, d), venv_path)
            content_listbox.insert(tk.END, f"[DIR] {rel_path}")
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), venv_path)
            content_listbox.insert(tk.END, f"      {rel_path}")

# Delete selected venv(s) with size preview
def delete_venvs():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select one or more virtual environments to delete.")
        return
    paths_to_delete = [tree.item(s)['values'][0] for s in selected]
    total_size = sum(get_size(p) for p in paths_to_delete) / (1024*1024)
    confirm = messagebox.askyesno(
        "Confirm Deletion",
        f"You are about to delete {len(paths_to_delete)} venv(s) totaling {total_size:.2f} MB.\n\n" +
        "Are you sure?"
    )
    if confirm:
        errors = []
        for venv_path in paths_to_delete:
            try:
                shutil.rmtree(venv_path)
            except Exception as e:
                errors.append(f"{venv_path}: {e}")
        if errors:
            messagebox.showerror("Errors", "Some venvs could not be deleted:\n" + "\n".join(errors))
        else:
            messagebox.showinfo("Deleted", f"Deleted {len(paths_to_delete)} venv(s) successfully.")
        refresh_list()

# Tkinter GUI setup
root = tk.Tk()
root.title("Virtual Environment Manager")
root.geometry("1000x600")

# Search bar
search_var = tk.StringVar()
search_var.trace_add("write", update_list)
search_entry = tk.Entry(root, textvariable=search_var, font=("Arial", 12))
search_entry.pack(fill=tk.X, padx=10, pady=5)
search_entry.insert(0, "Type to filter venvs...")

# Treeview for venv list with size
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

columns = ("path", "size")
tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="extended")
tree.heading("path", text="Virtual Environment Path")
tree.heading("size", text="Size")
tree.column("path", width=700)
tree.column("size", width=100, anchor=tk.CENTER)
tree.pack(fill=tk.BOTH, expand=True)
tree.bind('<<TreeviewSelect>>', show_contents)

# Color tags
tree.tag_configure('large', background='#ffcccc')   # red
tree.tag_configure('medium', background='#ffe0b3')  # orange
tree.tag_configure('small', background='#ccffcc')   # green

# Scrollbar for treeview
tree_scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=tree_scrollbar.set)
tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Frame for content of selected venv
content_frame = tk.Frame(root)
content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

content_scrollbar = tk.Scrollbar(content_frame)
content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

content_listbox = tk.Listbox(content_frame, font=("Courier", 10))
content_listbox.pack(fill=tk.BOTH, expand=True)
content_listbox.config(yscrollcommand=content_scrollbar.set)
content_scrollbar.config(command=content_listbox.yview)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

refresh_btn = tk.Button(btn_frame, text="Refresh List", command=refresh_list, width=20)
refresh_btn.pack(side=tk.LEFT, padx=5)

delete_btn = tk.Button(btn_frame, text="Delete Selected", command=delete_venvs, width=20)
delete_btn.pack(side=tk.LEFT, padx=5)

# Initial load
all_venvs = []
refresh_list()

root.mainloop()
