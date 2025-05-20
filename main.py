# Libraries
import tkinter as tk
from tkinter import ttk
import random
import webbrowser

# Constants for drawing and animation settings.
FRAME_WIDTH = 60
FRAME_HEIGHT = 60
FRAME_SPACING = 20
START_X = 50
START_Y = 150
ANIMATION_DELAY = 50  
ANIMATION_STEPS = 25
MAX_FRAMES_ALLOWED = 9
MAX_REF_LENGTH = 30

# Button and label styling for less repetitiveness 

HIDDEN_BUTTON_STYLE = {
    'foreground': 'black',
    'background': 'white',
    'activebackground': 'black',
    'activeforeground': 'white',
    'highlightthickness': 1,
    'highlightbackground': 'black',
    'highlightcolor': 'black',
    'borderwidth': 0,
    'cursor': 'hand1',
    'font': ('Arial', 32, 'bold')
}

BUTTON_STYLE = {
    'foreground': 'white',
    'background': 'black',
    'activebackground': 'white',
    'activeforeground': 'black',
    'highlightthickness': 3,
    'highlightbackground': 'black',
    'highlightcolor': 'black',
    'borderwidth': 3,
    'cursor': 'hand1',
    'font': ('Arial', 16, 'bold')
}

LABEL_STYLE = {
    'foreground': 'black',
    'background': 'white',
    'font': ('Arial', 16, 'bold')
}

# Link opening function

def open_link(url):
    webbrowser.open_new(url)

def create_link_label(parent, text, url):
    link_label = tk.Label(
        parent, 
        text=text, 
        foreground="white",
        background="black",
        activebackground="white",
        activeforeground="black",
        highlightthickness= 3,
        highlightbackground="black",
        highlightcolor="black",
        borderwidth=3,
        font=("Arial", 16, "bold"), 
        cursor="hand2",
        pady=20,
    )
    link_label.bind("<Button-1>", lambda e: open_link(url))
    return link_label

# Main application instantiation
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulator Application")
        self.geometry("1024x640")
        self.resizable(False, False)

        # Create and store frames
        self.frames = {}
        for F in (LoadingFrame, MainMenuFrame, SimulatorFrame, CreditsFrame):
            frame = F(parent=self, controller=self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        # Start with loading screen
        self.show_frame(LoadingFrame)

    # Shows the frame
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

# Instantiation of loading screen frame
class LoadingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        # Title label
        title = tk.Label(
            self,
            text="Loading",
            font=("Arial", 32, "bold"),
            fg="black",
            bg="white"
        )
        title.pack(pady=200)

        # Progress bar background
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.canvas.place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.05)

        # Draw outline
        self.canvas.create_rectangle(0, 0, 818, 30, outline="black")
        self.bar = self.canvas.create_rectangle(0, 0, 0, 30, fill="black", width=0)
        self.progress = 0
        self.max_width = 900
        self.step = self.max_width // 150
        self.animate()

    # Fills the bar and switch to main menu when done
    def animate(self):
        if self.progress < self.max_width:
            self.progress += self.step
            self.canvas.coords(self.bar, 0, 0, self.progress, 30)
            self.after(30, self.animate)
        else:
            self.controller.show_frame(MainMenuFrame)

# Instantiation of main menu frame
class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        # Credits Button
        back_btn = tk.Button(
            self,
            text="!!!",
            command=lambda: controller.show_frame(CreditsFrame),
            **BUTTON_STYLE
        )
        back_btn.place(x=10, y=10)

        # Title Easter Egg Button
        title = tk.Button(
            self,
            command=lambda: controller.show_frame(CreditsFrame),
            text="The Simulator",
            **HIDDEN_BUTTON_STYLE
        )
        title.pack(pady=200)

        # Button container
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack()

        # Play button → transitions to simulator frame
        play_btn = tk.Button(
            btn_frame,
            command=lambda: controller.show_frame(SimulatorFrame),
            text="Play",
            **BUTTON_STYLE
        )
        play_btn.grid(row=0, column=0, padx=20)

        # Exit button → clean shutdown
        exit_btn = tk.Button(
            btn_frame,
            command=self.quit,
            text="Exit",
            **BUTTON_STYLE
        )
        exit_btn.grid(row=0, column=1, padx=20)

# Instantiation of credits frame, also includes the link to project repo
class CreditsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        # Return to menu button at top-left
        back_btn = tk.Button(
            self,
            text="←",
            command=lambda: controller.show_frame(MainMenuFrame),
            **BUTTON_STYLE
        )
        back_btn.place(x=10, y=10)

        MainTitle = tk.Frame(self, bg="white")
        MainTitle.pack(pady=50)
        
        title = tk.Label(
            MainTitle,
            text="CREDITS",
            font=("Arial", 32, "bold"),
            fg="black",
            bg="white"
        ).grid(row=0, column=0)
        subtitle = tk.Label(
            MainTitle,
            text="BSCS 3B OS Case Study",
            **LABEL_STYLE
        ).grid(row=1, column=0)
        
        ctrl = tk.Frame(self, bg="white")
        ctrl.pack(pady=40)
        
        tk.Label(
            ctrl, text="Tech Lead:",
            **LABEL_STYLE
        ).grid(row=0, column=0, padx=5)
        tk.Label(
            ctrl, text="Quiambao, Eric Janssen P.",
            **LABEL_STYLE
        ).grid(row=0, column=1, padx=5)
        tk.Label(
            ctrl, text="Programmer:",
            **LABEL_STYLE
        ).grid(row=1, column=0, padx=5)
        tk.Label(
            ctrl, text="Quiambao, Eric Janssen P.",
            **LABEL_STYLE
        ).grid(row=1, column=1, padx=5)
        tk.Label(
            ctrl, text="Designer:",
            **LABEL_STYLE
        ).grid(row=2, column=0, padx=5)
        tk.Label(
            ctrl, text="Quiambao, Eric Janssen P.",
            **LABEL_STYLE
        ).grid(row=2, column=1, padx=5)
        tk.Label(
            ctrl, text="Special Mention:",
            **LABEL_STYLE
        ).grid(row=3, column=0, padx=5)
        tk.Label(
            ctrl, text="Quiambao, Eric Janssen P.",
            **LABEL_STYLE
        ).grid(row=3, column=1, padx=5)
        tk.Label(
            ctrl, text="Submitted to:",
            **LABEL_STYLE
        ).grid(row=4, column=0, pady=20)
        tk.Label(
            ctrl, text="Jo Anne Cura",
            **LABEL_STYLE
        ).grid(row=4, column=1, pady=20)
        
        # Link to repo
        link1 = create_link_label(
            self, 
            "Visit Git Repo",
            "https://github.com/Ensues/OS-Case-Study"
        )     
        link1.pack(pady=50)   
        
# Instantiation of simulator frame, where the magic happens
class SimulatorFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Return to menu button at top-left
        back_btn = tk.Button(
            self,
            text="←",
            command=lambda: controller.show_frame(MainMenuFrame),
            **BUTTON_STYLE
        )
        back_btn.place(x=10, y=10)
        
        # initialize flag for history
        self.show_history = True
        
        # place toggle button at top‑right (adjust x offset as needed)
        self.toggle_btn = tk.Button(
            self,
            text="Hide History",
            command=self.toggle_history,
            **BUTTON_STYLE
        )
        # anchor NE: button’s top‑right corner sits at (x=780, y=10)
        self.toggle_btn.place(x=980, y=10, anchor="ne")

        # Control Panel
        ctrl = tk.Frame(self, bg="white")
        ctrl.pack(pady=20)
        
        # Number of frames input
        tk.Label(ctrl, text="Frames (1-9):", font=("Arial", 11), bg="white").grid(row=0, column=0)
        self.frames_entry = tk.Entry(ctrl, width=5, font=("Arial", 11))
        self.frames_entry.insert(0, "3")
        self.frames_entry.grid(row=0, column=1)

        # Reference string length input
        tk.Label(ctrl, text="Length (1-30):", font=("Arial", 11), bg="white").grid(row=0, column=2)
        self.length_entry = tk.Entry(ctrl, width=5, font=("Arial", 11))
        self.length_entry.insert(0, "10")
        self.length_entry.grid(row=0, column=3)

        # CLEAR / Algo buttons
        tk.Button(ctrl, text="CLEAR", command=self.clear, **BUTTON_STYLE).grid(row=1, column=0, pady=5, padx=5)
        tk.Button(ctrl, text="Start FIFO", command=self.start_fifo, **BUTTON_STYLE).grid(row=1, column=1, padx=5)
        tk.Button(ctrl, text="Start LRU", command=self.start_lru, **BUTTON_STYLE).grid(row=1, column=2, padx=5)
        tk.Button(ctrl, text="Start OPT", command=self.start_opt, **BUTTON_STYLE).grid(row=1, column=3, padx=5)

        # Scrollable canvas setup
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, pady=10)
        self.canvas = tk.Canvas(container, bg="white", height=300)
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Status Bar 
        self.status = tk.Label(self, text="Status: Ready", **BUTTON_STYLE)
        self.status.pack(pady=5)

        # Initialize all simulation state
        self.reset_state()

    # Clears all data structures and canvas tags for a fresh run
    def reset_state(self):
        self.max_frames = 3
        self.frames = []
        self.fifo_queue = []
        self.lru_order = []
        self.reference_string = []
        self.current = 0
        self.algorithm = None
        self.frame_history = []
        
        # Clear only frames tags and ref tags
        self.canvas.delete("frames")
        self.canvas.delete("ref")
        self.canvas.delete("warning")

    # Returns False if entries are non‑numeric or out of range
    def validate_inputs(self):
        try:
            f = int(self.frames_entry.get())
            l = int(self.length_entry.get())
        except ValueError:
            return False
        return 1 <= f <= MAX_FRAMES_ALLOWED and 1 <= l <= MAX_REF_LENGTH

    # Display an error when inputs are invalid
    def show_warning(self):
        self.canvas.delete("all")
        warning = f"Inputs out of range!\nFrames: 1-{MAX_FRAMES_ALLOWED}, Length: 1-{MAX_REF_LENGTH}"
        self.canvas.create_text(390, 175, text=warning, font=("Arial", 16), fill="red", tags="warning")
        self.status.config(text="Status: Invalid input, simulation aborted.")

    # Algorithm Starters 
    def start_fifo(self):
        self.algorithm = "FIFO"
        self.status.config(text="FIFO starting")
        self.start_sim()

    def start_lru(self):
        self.algorithm = "LRU"
        self.status.config(text="LRU starting")
        self.start_sim()

    def start_opt(self):
        self.algorithm = "OPT"
        self.status.config(text="OPT starting")
        self.start_sim()

    # User‑requested interruption
    def clear(self):
        self.reset_state()
        self.status.config(text="Simulation Interrupted")

    # Show or hide the full history vs. just the latest snapshot
    def toggle_history(self):
        self.show_history = not self.show_history
        self.toggle_btn.config(text="Hide History" if self.show_history else "Show History")
        self.draw_frame_history()

    # Validate inputs, reset state, generate reference string, and kick off stepping
    def start_sim(self):
        if not self.validate_inputs():
            self.show_warning()
            return
        self.reset_state()
        self.max_frames = int(self.frames_entry.get())
        length = int(self.length_entry.get())
        self.reference_string = [random.randint(0, 9) for _ in range(length)]
        self.frames = [None] * self.max_frames

        # Display algorithm name and reference string
        self.canvas.create_text(400, 5, text=self.algorithm, font=("Arial", 20), tags="ref")

        self.status.config(text=f"{self.algorithm} Ref String: {self.reference_string}")
        self.after(500, self.next_step)
 
    # Execute one page reference: hit or fault, record state, then schedule next
    def next_step(self):
        if self.current >= len(self.reference_string):
            self.status.config(text="Simulation complete")
            return
        page = self.reference_string[self.current]

        if page in self.frames:
            idx = self.frames.index(page)
            if self.algorithm == "LRU":
                self.lru_order.remove(idx)
                self.lru_order.append(idx)
            self.current += 1
        else:
            if None in self.frames:
                # fill first empty slot
                idx = self.frames.index(None)
                self.frames[idx] = page
                if self.algorithm == "FIFO":
                    self.fifo_queue.append(idx)
                if self.algorithm == "LRU":
                    self.lru_order.append(idx)
                self.current += 1
            else:
                 # all frames full → choose index by policy
                if self.algorithm == "FIFO":
                    idx = self.fifo_queue.pop(0)
                    self.frames[idx] = page
                    self.fifo_queue.append(idx)
                elif self.algorithm == "LRU":
                    idx = self.lru_order.pop(0)
                    self.frames[idx] = page
                    self.lru_order.append(idx)
                else: 
                    future = []
                    for f in self.frames:
                        try:
                            dist = self.reference_string[self.current+1:].index(f)
                        except ValueError:
                            dist = float('inf')
                        future.append(dist)
                    idx = future.index(max(future))
                    self.frames[idx] = page
                self.current += 1

        # Record & Redraw 
        self.frame_history.append(self.frames.copy())
        self.draw_frame_history()
        self.after(300, self.next_step)

    def draw_frame_history(self):
        # Clear only frames layer
        self.canvas.delete("frames")
        
        # choose what to draw
        if self.show_history:
            data = self.frame_history
        else:
            data = self.frame_history[-1:] if self.frame_history else []

        # draw each timestep vertically
        for t, snapshot in enumerate(data):
            y0 = START_Y + t * (FRAME_HEIGHT + FRAME_SPACING)
            for i, val in enumerate(snapshot):
                x0 = START_X + i * (FRAME_WIDTH + FRAME_SPACING)
                self.canvas.create_rectangle(
                    x0, y0, x0 + FRAME_WIDTH, y0 + FRAME_HEIGHT,
                    fill="lightgrey",
                    tags="frames"
                )
                self.canvas.create_text(
                    x0 + FRAME_WIDTH/2, y0 + FRAME_HEIGHT/2,
                    text=str(val) if val is not None else "",
                    font=("Arial", 16),
                    tags="frames"
                )

        # update scrollable region height
        total_h = START_Y + len(data) * (FRAME_HEIGHT + FRAME_SPACING)
        self.canvas.config(scrollregion=(0, 0, 800, total_h))

# app start
if __name__ == "__main__":
    app = App()
    app.mainloop()
