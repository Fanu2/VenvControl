# Venv Manager GUI

A simple Python application to **list, view, and manage virtual environments** on your system.  
The app provides a GUI interface to make virtual environment management easier and more interactive.

## Features

- Automatically scans your home directory for virtual environments (`venv`, `.venv`, `env`).  
- Displays virtual environments along with their sizes.  
- Allows you to delete virtual environments interactively.  
- Shows warnings for system or small environments.  
- Built using Python with a **Tkinter GUI**.  

## Requirements

- Python 3.10+  
- `rich` for terminal output  
- `psutil` for system info  

Optional (if adding web GUI features):

- `streamlit`  

Example `requirements.txt`:

```txt
rich==13.7.2
psutil==5.9.6
# streamlit==1.26.1  # optional for web GUI
