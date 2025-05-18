import tkinter as tk
import random

# Constants for drawing and animation settings.
FRAME_WIDTH = 60
FRAME_HEIGHT = 60
FRAME_SPACING = 20
START_X = 50
START_Y = 150
ANIMATION_DELAY = 50   # Time delay (ms) between animation moves.
ANIMATION_STEPS = 20   # Number of steps in the move animation.
MAX_FRAMES_ALLOWED = 9
MAX_REF_LENGTH = 30

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

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulator Application")
        self.geometry("800x600")
        self.resizable(False, False)

        # Create and store frames
        self.frames = {}
        for F in (LoadingFrame, MainMenuFrame, SimulatorFrame):
            frame = F(parent=self, controller=self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        # Start with loading screen
        self.show_frame(LoadingFrame)

    def show_frame(self, frame_class):
        """Bring the given frame to the front."""
        frame = self.frames[frame_class]
        frame.tkraise()


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
        self.canvas.create_rectangle(0, 0, 700, 30, outline="black")
        self.bar = self.canvas.create_rectangle(0, 0, 0, 30, fill="black", width=0)

        self.progress = 0
        self.max_width = 700
        self.step = self.max_width // 100
        self.animate()

    def animate(self):
        """Fill the bar and switch to main menu when done."""
        if self.progress < self.max_width:
            self.progress += self.step
            self.canvas.coords(self.bar, 0, 0, self.progress, 30)
            self.after(30, self.animate)
        else:
            self.controller.show_frame(MainMenuFrame)


class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Title label
        title = tk.Label(
            self,
            text="Simulator",
            font=("Arial", 32, "bold"),
            fg="black",
            bg="white"
        )
        title.pack(pady=200)

        # Button container
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack()

        # Play button → transitions to blank frame
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


class SimulatorFrame(tk.Frame):
    """
    Integrated Page Replacement Simulator.
    Foreground elements are black, background is white.
    """
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

        # Controls frame on top
        ctrl = tk.Frame(self, bg="white")
        ctrl.pack(pady=40)

        tk.Label(
            ctrl, text="Number of Frames (1-9):",
            fg="black", bg="white",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5)
        self.frames_entry = tk.Entry(ctrl, width=5, font=("Arial", 11))
        self.frames_entry.insert(0, "3")
        self.frames_entry.grid(row=0, column=1, padx=5)

        tk.Label(
            ctrl, text="Reference Length (1-30):",
            fg="black", bg="white",
            font=("Arial", 11)
        ).grid(row=0, column=2, padx=5)
        self.length_entry = tk.Entry(ctrl, width=5, font=("Arial", 11))
        self.length_entry.insert(0, "10")
        self.length_entry.grid(row=0, column=3, padx=5)

        # Clear Button
        tk.Button(
            ctrl,
            text="CLEAR",
            command=self.clear,
            **BUTTON_STYLE
        ).grid(row=1, column=0, pady=5, padx=5)
        # Algorithm Buttons
        tk.Button(
            ctrl,
            text="Start FIFO",
            command=self.start_fifo,
            **BUTTON_STYLE
        ).grid(row=1, column=1, pady=5, padx=5)
        tk.Button(
            ctrl,
            text="Start LRU",
            command=self.start_lru,
            **BUTTON_STYLE
        ).grid(row=1, column=2, pady=5, padx=5)
        tk.Button(
            ctrl,
            text="Start OPT",
            command=self.start_opt,
            **BUTTON_STYLE
        ).grid(row=1, column=3, pady=5, padx=5)

        # Canvas area
        self.canvas = tk.Canvas(
            self,
            width=780, height=350,
            bg="white",
            highlightthickness=1,
            highlightbackground="black"
        )
        self.canvas.pack(pady=10)

        # Status label
        self.status = tk.Label(
            self,
            text="Status: Ready",
            fg="black", bg="white"
        )
        self.status.pack(pady=5)

        # Simulation state
        self.reset_state()

    def reset_state(self):
        self.max_frames = 3
        self.frames = []
        self.fifo_queue = []
        self.lru_order = []
        self.reference_string = []
        self.current = 0
        self.algorithm = None
        self.frame_boxes = []

    def setup_frames(self):
        self.canvas.delete("frames")
        self.canvas.delete("ref")
        self.canvas.delete("warning")
        self.frame_boxes.clear()
        for i in range(self.max_frames):
            x = START_X + i * (FRAME_WIDTH + FRAME_SPACING)
            y = START_Y
            rect = self.canvas.create_rectangle(
                x, y, x+FRAME_WIDTH, y+FRAME_HEIGHT,
                fill="lightgrey",
                tags=("frame_box","frames")
            )
            txt = self.canvas.create_text(
                x+FRAME_WIDTH/2, y+FRAME_HEIGHT/2,
                text="", font=("Arial", 16),
                tags=("frame_box","frames")
            )
            self.frame_boxes.append((rect, txt))

    def validate_inputs(self):
        """Check if user inputs are within allowed ranges."""
        try:
            frames = int(self.frames_entry.get())
            length = int(self.length_entry.get())
        except ValueError:
            return False
        return 1 <= frames <= MAX_FRAMES_ALLOWED and 1 <= length <= MAX_REF_LENGTH

    def show_warning(self):
        """Display warning on canvas and update status."""
        # clear canvas
        self.canvas.delete("all")
        warning = f"Inputs out of range!\nFrames: 1-{MAX_FRAMES_ALLOWED}, Length: 1-{MAX_REF_LENGTH}"
        self.canvas.create_text(
            390, 175,
            text=warning,
            font=("Arial", 16),
            fill="red",
            justify="center",
            tags="warning"
        )
        self.status.config(text="Status: Invalid input, simulation aborted.")

    def start_fifo(self):
        self.canvas.delete("all")
        self.algorithm = "FIFO"
        self.status.config(text="FIFO Algorithm starting")
        self.start_sim()

    def start_lru(self):
        self.canvas.delete("all")
        self.algorithm = "LRU"
        self.status.config(text="LRU Algorithm starting")
        self.start_sim()

    def start_opt(self):
        self.canvas.delete("all")
        self.algorithm = "OPT"
        self.status.config(text="OPT Algorithm starting")
        self.start_sim()
        
    def clear(self):
        # clear canvas 
        self.canvas.delete("all")
        self.status.config(text="Simulation Interrupted")

    def start_sim(self):
        """Initialize simulation and display reference string if inputs valid."""
        # Validate before proceeding
        if not self.validate_inputs():
            self.show_warning()
            return

        # Clear warning only
        self.canvas.delete("warning")
        self.status.config(text="Status: Ready")

        # Read values
        self.max_frames = int(self.frames_entry.get())
        length = int(self.length_entry.get())

        self.setup_frames()
        # Generate reference string
        self.reference_string = [random.randint(0,9) for _ in range(length)]
        self.frames = [None]*self.max_frames
        self.fifo_queue.clear()
        self.lru_order.clear()
        self.current = 0
        self.status.config(text=f"Ref String: {self.reference_string}")
        self.canvas.create_text(
            400, 20,
            text="Ref String: "+str(self.reference_string),
            font=("Arial",14),
            tags=("ref","frames")
        )
        self.after(1000, self.next_step)

    def next_step(self):
        if self.current >= len(self.reference_string):
            self.status.config(text="Simulation complete")
            return
        page = self.reference_string[self.current]
        self.status.config(text=f"Processing {page} ({self.algorithm})")
        if page in self.frames:
            idx = self.frames.index(page)
            self.highlight(idx, "green")
            if self.algorithm=="LRU":
                self.lru_order.remove(idx)
                self.lru_order.append(idx)
            self.current +=1
            self.after(1000, self.next_step)
        else:
            if None in self.frames:
                idx = self.frames.index(None)
                self.frames[idx]=page
                if self.algorithm=="FIFO": self.fifo_queue.append(idx)
                if self.algorithm=="LRU": self.lru_order.append(idx)
                self.animate(page, idx)
            else:
                if self.algorithm=="FIFO":
                    idx=self.fifo_queue.pop(0)
                    self.frames[idx]=page
                    self.fifo_queue.append(idx)
                elif self.algorithm=="LRU":
                    idx=self.lru_order.pop(0)
                    self.frames[idx]=page
                    self.lru_order.append(idx)
                else:  # OPT
                    future=[]
                    for i in range(self.max_frames):
                        try:
                            next_use=self.reference_string[self.current+1:].index(self.frames[i])
                        except ValueError:
                            next_use=float('inf')
                        future.append(next_use)
                    idx=future.index(max(future))
                    self.frames[idx]=page
                self.animate(page, idx)

    def animate(self, page, frame_idx):
        start_x, start_y = 50, 550
        moving = self.canvas.create_text(start_x, start_y, text=str(page), font=("Arial",16), fill="red")
        rect, txt = self.frame_boxes[frame_idx]
        coords=self.canvas.coords(rect)
        tx=(coords[0]+coords[2])/2
        ty=(coords[1]+coords[3])/2
        dx=(tx-start_x)/ANIMATION_STEPS
        dy=(ty-start_y)/ANIMATION_STEPS
        def step(i=0):
            if i<ANIMATION_STEPS:
                self.canvas.move(moving, dx, dy)
                self.after(ANIMATION_DELAY, step, i+1)
            else:
                self.canvas.itemconfig(txt, text=str(page))
                self.canvas.delete(moving)
                self.current+=1
                self.after(500, self.next_step)
        step()

    def highlight(self, idx, color):
        rect, _ = self.frame_boxes[idx]
        orig = self.canvas.itemcget(rect, "fill")
        self.canvas.itemconfig(rect, fill=color)
        self.after(300, lambda: self.canvas.itemconfig(rect, fill=orig))


if __name__ == "__main__":
    app = App()
    app.mainloop()
