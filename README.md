## OS Case Study Simulator

<p align="center">
   <img alt="Python" src="https://img.shields.io/badge/-Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
</p>

**Overview**

This repository delivers a Tkinter-based page replacement algorithm simulator designed to visualize **FIFO**, **LRU**, and **OPT** strategies. This is a case study for the subject Operating Systems.

[⬇️ Get the latest Windows EXE](https://github.com/Ensues/OS-Case-Study/releases/download/v1.0.1/main.exe)

---

## Features

* **Modular Architecture**: Utilizes a multi-frame design (`Loading`, `MainMenu`, `Simulator`, `Credits`) for clear separation of concerns.
* **Algorithm Support**: Implements **First-In-First-Out (FIFO)**, **Least Recently Used (LRU)**, and **Optimal (OPT)** replacement policies.
* **Interactive Controls**: Input validation ensures frame count (1–9) and reference length (1–30) adhere to constraints.
* **Visual Feedback**: Animated page movements, color-coded hit/miss indicators, and status updates.
* **Easter Egg & Credits**: Hidden title button and dedicated credits page with external link integration.

---

## Prerequisites

1. **Python** 3.9+
2. **Tkinter** (bundled with standard Python installation)

---

## Installation & Build

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Ensues/OS-Case-Study.git
   cd OS-Case-Study
   ```

2. **(Optional) Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/Scripts/activate   # Windows PowerShell
   ```

3. **Install dependencies** (none beyond standard library).
   If you plan to generate an executable, install:

   ```bash
   pip install pyinstaller
   ```

4. **Build executable** (one-file bundle):

   ```bash
   py -m PyInstaller main.py --onefile
   ```

---

## Usage

* **Run from source**:

  ```bash
  python main.py
  ```

* **Run the compiled binary**:

  ```bash
  ./dist/main.exe           # Windows
  ```

**Simulator Workflow**:

1. Configure **Number of Frames** and **Reference Length**.
2. Click **Start FIFO**, **Start LRU**, or **Start OPT**.
3. Observe animated page allocation and replacement.
4. Click **CLEAR** to reset or **Exit** to terminate the app.

---

## Repository Structure

```
├── main.py            # Entry point and frame-controller
├── main.spec          # PyInstaller build script for generating the standalone executable
├── README.md          # This document
├── dist/              # Compiled executable (post-build)
├── documentation/     # Paper documentation
└── build/             # PyInstaller build artifact
```

---

## Roadmap & Next Steps

* **Custom Reference Strings**: Inject user-defined sequences.
* **Statistics Dashboard**: Track hit/miss rates, graphs for post-mortem.
* **Automated CI/CD**: GitHub Actions workflow for build, test, and release automation.

---

## License

Distributed under the MIT License. See `LICENSE` for full terms.

---

**OS Case Study Simulator** • Ensues Development Team
