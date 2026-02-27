# Pomodoro Timer App

A modern, feature-rich Pomodoro Timer application built with PyQt6 that helps you manage your time using the Pomodoro Technique.

## Features

### Core Functionality
- **Complete Pomodoro Cycle**: Automatically alternates between work sessions, short breaks, and long breaks
- **Customizable Timers**: Adjust work duration (1-60 min), short breaks (1-30 min), and long breaks (1-60 min)
- **Session Tracking**: Tracks completed pomodoros and progress toward long breaks
- **Smart Notifications**: Pop-up alerts when sessions complete 
### User Interface
- **Modern Dark Theme**: Clean, professional design with vibrant accent colors
- **Large Timer Display**: Easy-to-read 72pt countdown timer
- **Session Indicators**: Color-coded labels showing current session type
  - Red for work sessions
  - Cyan for short breaks
  - Light cyan for long breaks
- **Progress Tracking**: Shows which session you're on (e.g., "Session 2 of 4 until long break")

### Controls
- **Start/Pause**: Begin or pause the current session
- **Reset**: Restart the current session from the beginning
- **Skip Session**: Jump to the next session in the cycle
- **Live Settings**: Adjust timer durations on the fly (when timer is not running)

## Installation

### Requirements
- Python 3.7+
- PyQt6

### Setup
```bash
# Install PyQt6
pip install PyQt6

# Run the application
python main.py
```

## Usage

### The Pomodoro Technique
1. **Work Session** (default: 25 minutes) - Focus on your task
2. **Short Break** (default: 5 minutes) - Take a quick break
3. Repeat steps 1-2 for 4 cycles
4. **Long Break** (default: 15 minutes) - Take an extended break
5. Start the cycle again

### How to Use the App
1. **Start a Session**: Click the "▶ Start" button to begin your work session
2. **Pause if Needed**: Click "⏸ Pause" to temporarily stop the timer
3. **Reset Current Session**: Click "↻ Reset" to restart the current session
4. **Skip to Next Session**: Click "⏭ Skip Session" to move to the next phase
5. **Customize Settings**: Adjust the duration spinboxes in the Settings section

### Customization
You can customize the timer durations in the Settings panel:
- **Work Duration**: Set how long each work session lasts (1-60 minutes)
- **Short Break**: Set the duration of short breaks (1-30 minutes)
- **Long Break**: Set the duration of long breaks (1-60 minutes)

Note: Settings can only be changed when the timer is not running.

## Code Structure

### Main Class: `PomodoroTimer`
The application is built around a single `PomodoroTimer` class that inherits from `QWidget`.

#### Session Types
```python
WORK = "Work Session"
SHORT_BREAK = "Short Break"
LONG_BREAK = "Long Break"
```

#### Key Methods
- `init_ui()`: Initializes the user interface with all widgets and layouts
- `start_timer()`: Starts the countdown timer
- `pause_timer()`: Pauses the running timer
- `reset_timer()`: Resets the current session to its full duration
- `skip_session()`: Skips to the next session in the cycle
- `update_timer()`: Called every second to update the display
- `session_complete()`: Handles session completion and transitions
- `update_display()`: Updates the timer display and session information
- `update_settings()`: Updates timer durations from the settings spinboxes

#### State Variables
- `work_duration`: Duration of work sessions in seconds
- `short_break_duration`: Duration of short breaks in seconds
- `long_break_duration`: Duration of long breaks in seconds
- `time_remaining`: Current time left in the session
- `is_running`: Boolean indicating if timer is active
- `current_session`: Current session type (WORK, SHORT_BREAK, or LONG_BREAK)
- `pomodoro_count`: Total number of completed work sessions
- `session_count`: Number of sessions completed toward the next long break
