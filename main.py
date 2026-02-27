from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                              QHBoxLayout, QLabel, QSpinBox, QMessageBox, QGroupBox)
from PyQt6.QtGui import QFont, QPalette, QColor
import sys


class PomodoroTimer(QWidget):
    # Session types
    WORK = "Work Session"
    SHORT_BREAK = "Short Break"
    LONG_BREAK = "Long Break"

    def __init__(self):
        super().__init__()

        # Timer settings (in seconds)
        self.work_duration = 25 * 60  # 25 minutes
        self.short_break_duration = 5 * 60  # 5 minutes
        self.long_break_duration = 15 * 60  # 15 minutes
        self.pomodoros_until_long_break = 4

        # State variables
        self.time_remaining = self.work_duration
        self.is_running = False
        self.current_session = self.WORK
        self.pomodoro_count = 0
        self.session_count = 0  # Track sessions for long break

        # Setup timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.init_ui()
        self.update_display()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Pomodoro Timer")
        self.setFixedSize(450, 600)
        self.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Session type label
        self.session_label = QLabel(self.WORK)
        self.session_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        session_font = QFont("Arial", 21, QFont.Weight.Bold)
        self.session_label.setFont(session_font)
        self.session_label.setStyleSheet("color: #ff6b6b; padding: 10px;")
        main_layout.addWidget(self.session_label)

        # Timer display
        self.timer_label = QLabel("25:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_font = QFont("Arial", 72, QFont.Weight.Bold)
        self.timer_label.setFont(timer_font)
        self.timer_label.setStyleSheet("color: #4ecdc4; padding: 20px;")
        main_layout.addWidget(self.timer_label)

        # Pomodoro counter
        counter_layout = QHBoxLayout()
        counter_label = QLabel("Pomodoros Completed:")
        counter_label.setFont(QFont("Arial", 12))
        self.pomodoro_count_label = QLabel("0")
        self.pomodoro_count_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.pomodoro_count_label.setStyleSheet("color: #ffe66d;")
        counter_layout.addStretch()
        counter_layout.addWidget(counter_label)
        counter_layout.addWidget(self.pomodoro_count_label)
        counter_layout.addStretch()
        main_layout.addLayout(counter_layout)

        # Progress indicator
        self.progress_label = QLabel("Session 1 of 4 until long break")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setFont(QFont("Arial", 10))
        self.progress_label.setStyleSheet("color: #95e1d3;")
        main_layout.addWidget(self.progress_label)

        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.start_button = QPushButton("▶ Start")
        self.start_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4ecdc4;
                color: #2b2b2b;
                border: none;
                border-radius: 8px;
                padding: 15px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45b7af;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
        """)
        self.start_button.clicked.connect(self.start_timer)

        self.pause_button = QPushButton("⏸ Pause")
        self.pause_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.pause_button.setStyleSheet("""
            QPushButton {
                background-color: #ffe66d;
                color: #2b2b2b;
                border: none;
                border-radius: 8px;
                padding: 15px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #f5d742;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
        """)
        self.pause_button.clicked.connect(self.pause_timer)
        self.pause_button.setEnabled(False)

        self.reset_button = QPushButton("↻ Reset")
        self.reset_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6b6b;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 15px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #ee5a52;
            }
        """)
        self.reset_button.clicked.connect(self.reset_timer)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)
        main_layout.addLayout(button_layout)

        # Skip session button
        self.skip_button = QPushButton("⏭ Skip Session")
        self.skip_button.setFont(QFont("Arial", 12))
        self.skip_button.setStyleSheet("""
            QPushButton {
                background-color: #95e1d3;
                color: #2b2b2b;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #7dd3c0;
            }
        """)
        self.skip_button.clicked.connect(self.skip_session)
        main_layout.addWidget(self.skip_button)

        # Settings group
        settings_group = QGroupBox("Settings (minutes)")
        settings_group.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        settings_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                border: 2px solid #4ecdc4;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        settings_layout = QVBoxLayout()

        # Work duration setting
        work_layout = QHBoxLayout()
        work_label = QLabel("Work Duration:")
        work_label.setFont(QFont("Arial", 11))
        self.work_spinbox = QSpinBox()
        self.work_spinbox.setRange(1, 60)
        self.work_spinbox.setValue(25)
        self.work_spinbox.setSuffix(" min")
        self.work_spinbox.setStyleSheet("background-color: #3b3b3b; border: 1px solid #4ecdc4; padding: 5px;")
        self.work_spinbox.valueChanged.connect(self.update_settings)
        work_layout.addWidget(work_label)
        work_layout.addStretch()
        work_layout.addWidget(self.work_spinbox)

        # Short break setting
        short_break_layout = QHBoxLayout()
        short_break_label = QLabel("Short Break:")
        short_break_label.setFont(QFont("Arial", 11))
        self.short_break_spinbox = QSpinBox()
        self.short_break_spinbox.setRange(1, 30)
        self.short_break_spinbox.setValue(5)
        self.short_break_spinbox.setSuffix(" min")
        self.short_break_spinbox.setStyleSheet("background-color: #3b3b3b; border: 1px solid #4ecdc4; padding: 5px;")
        self.short_break_spinbox.valueChanged.connect(self.update_settings)
        short_break_layout.addWidget(short_break_label)
        short_break_layout.addStretch()
        short_break_layout.addWidget(self.short_break_spinbox)

        # Long break setting
        long_break_layout = QHBoxLayout()
        long_break_label = QLabel("Long Break:")
        long_break_label.setFont(QFont("Arial", 11))
        self.long_break_spinbox = QSpinBox()
        self.long_break_spinbox.setRange(1, 60)
        self.long_break_spinbox.setValue(15)
        self.long_break_spinbox.setSuffix(" min")
        self.long_break_spinbox.setStyleSheet("background-color: #3b3b3b; border: 1px solid #4ecdc4; padding: 5px;")
        self.long_break_spinbox.valueChanged.connect(self.update_settings)
        long_break_layout.addWidget(long_break_label)
        long_break_layout.addStretch()
        long_break_layout.addWidget(self.long_break_spinbox)

        settings_layout.addLayout(work_layout)
        settings_layout.addLayout(short_break_layout)
        settings_layout.addLayout(long_break_layout)
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def start_timer(self):
        """Start the timer"""
        if not self.is_running:
            self.is_running = True
            self.timer.start(1000)  # Update every second
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)

    def pause_timer(self):
        """Pause the timer"""
        if self.is_running:
            self.is_running = False
            self.timer.stop()
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)

    def reset_timer(self):
        """Reset the timer to the beginning of current session"""
        self.timer.stop()
        self.is_running = False

        # Reset to current session's duration
        if self.current_session == self.WORK:
            self.time_remaining = self.work_duration
        elif self.current_session == self.SHORT_BREAK:
            self.time_remaining = self.short_break_duration
        else:
            self.time_remaining = self.long_break_duration

        self.update_display()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)

    def skip_session(self):
        """Skip to the next session"""
        self.timer.stop()
        self.is_running = False
        self.session_complete()

    def update_timer(self):
        """Update the timer every second"""
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_display()
        else:
            self.session_complete()

    def session_complete(self):
        """Handle session completion"""
        self.timer.stop()
        self.is_running = False

        # Show notification
        if self.current_session == self.WORK:
            self.pomodoro_count += 1
            self.session_count += 1
            self.pomodoro_count_label.setText(str(self.pomodoro_count))

            # Determine next break type
            if self.session_count >= self.pomodoros_until_long_break:
                self.current_session = self.LONG_BREAK
                self.session_count = 0
                message = f"🎉 Great work! You've completed {self.pomodoros_until_long_break} pomodoros!\nTime for a long break!"
            else:
                self.current_session = self.SHORT_BREAK
                message = "✅ Work session complete!\nTime for a short break!"

            QMessageBox.information(self, "Session Complete", message)
        else:
            self.current_session = self.WORK
            message = "☕ Break is over!\nReady for another work session?"
            QMessageBox.information(self, "Break Complete", message)

        # Set up next session
        if self.current_session == self.WORK:
            self.time_remaining = self.work_duration
            self.session_label.setStyleSheet("color: #ff6b6b; padding: 10px;")
        elif self.current_session == self.SHORT_BREAK:
            self.time_remaining = self.short_break_duration
            self.session_label.setStyleSheet("color: #4ecdc4; padding: 10px;")
        else:
            self.time_remaining = self.long_break_duration
            self.session_label.setStyleSheet("color: #95e1d3; padding: 10px;")

        self.update_display()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)

    def update_display(self):
        """Update the display with current time and session info"""
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
        self.session_label.setText(self.current_session)

        # Update progress label
        if self.current_session == self.WORK:
            sessions_left = self.pomodoros_until_long_break - self.session_count
            self.progress_label.setText(
                f"Session {self.session_count + 1} of {self.pomodoros_until_long_break} until long break"
            )
        else:
            self.progress_label.setText("Take a break and relax! 😌")

    def update_settings(self):
        """Update timer settings from spinboxes"""
        if not self.is_running:
            self.work_duration = self.work_spinbox.value() * 60
            self.short_break_duration = self.short_break_spinbox.value() * 60
            self.long_break_duration = self.long_break_spinbox.value() * 60

            # Update current time if in the corresponding session
            if self.current_session == self.WORK:
                self.time_remaining = self.work_duration
            elif self.current_session == self.SHORT_BREAK:
                self.time_remaining = self.short_break_duration
            else:
                self.time_remaining = self.long_break_duration

            self.update_display()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    window = PomodoroTimer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


