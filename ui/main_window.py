from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QListWidget, QListWidgetItem,
                             QComboBox, QProgressBar, QFileDialog, QMessageBox,
                             QGroupBox, QGridLayout, QTabWidget, QTextEdit,
                             QSplitter, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMimeData, QUrl
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor, QDragEnterEvent, QDropEvent
import os
from utils.file_detector import FileDetector
from utils.conversion_manager import ConversionManager
from utils.history_manager import HistoryManager
from ui.advanced_settings import AdvancedSettingsDialog

class DragDropListWidget(QListWidget):
    filesDropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DropOnly)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            if url.isLocalFile():
                files.append(url.toLocalFile())
        if files:
            self.filesDropped.emit(files)
        event.acceptProposedAction()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_detector = FileDetector()
        self.conversion_manager = ConversionManager()
        self.history_manager = HistoryManager()
        self.setup_ui()
        self.setup_connections()
        self.update_history_display()

    def setup_ui(self):
        self.setWindowTitle("Universal Converter")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)

        # Apply modern style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #333333;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QListWidget {
                border: 2px dashed #cccccc;
                border-radius: 8px;
                background-color: #fafafa;
                padding: 10px;
                min-height: 150px;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
                font-size: 14px;
            }
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 4px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("Universal Converter")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #333333; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        # Main content splitter
        content_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(content_splitter)

        # Left panel
        left_panel = self.create_conversion_panel()
        content_splitter.addWidget(left_panel)

        # Right panel (tabs)
        right_panel = self.create_right_panel()
        content_splitter.addWidget(right_panel)

        # Set splitter proportions
        content_splitter.setSizes([700, 500])

        # Status bar
        self.statusBar().showMessage("Ready")

    def create_conversion_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Files section
        files_group = QGroupBox("Files to Convert")
        files_layout = QVBoxLayout(files_group)

        # Drag & Drop area
        self.file_list = DragDropListWidget()
        self.file_list.filesDropped.connect(self.add_files)

        # Add placeholder text
        placeholder_item = QListWidgetItem("Drag & drop files here or click 'Add Files' below")
        placeholder_item.setFlags(Qt.NoItemFlags)
        placeholder_item.setTextAlignment(Qt.AlignCenter)
        self.file_list.addItem(placeholder_item)

        files_layout.addWidget(self.file_list)

        # File buttons
        file_buttons_layout = QHBoxLayout()
        self.add_files_btn = QPushButton("Add Files")
        self.remove_files_btn = QPushButton("Remove Selected")
        self.clear_files_btn = QPushButton("Clear All")

        file_buttons_layout.addWidget(self.add_files_btn)
        file_buttons_layout.addWidget(self.remove_files_btn)
        file_buttons_layout.addWidget(self.clear_files_btn)
        file_buttons_layout.addStretch()

        files_layout.addLayout(file_buttons_layout)
        layout.addWidget(files_group)

        # Conversion settings
        settings_group = QGroupBox("Conversion Settings")
        settings_layout = QGridLayout(settings_group)

        settings_layout.addWidget(QLabel("Output Format:"), 0, 0)
        self.output_format_combo = QComboBox()
        settings_layout.addWidget(self.output_format_combo, 0, 1)

        settings_layout.addWidget(QLabel("Output Directory:"), 1, 0)
        output_dir_layout = QHBoxLayout()
        self.output_dir_label = QLabel("Same as source files")
        self.browse_output_btn = QPushButton("Browse")
        output_dir_layout.addWidget(self.output_dir_label)
        output_dir_layout.addWidget(self.browse_output_btn)
        settings_layout.addLayout(output_dir_layout, 1, 1)

        layout.addWidget(settings_group)

        # Progress section
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready to convert")
        progress_layout.addWidget(self.status_label)

        layout.addWidget(progress_group)

        # Convert button
        self.convert_btn = QPushButton("Start Conversion")
        self.convert_btn.setMinimumHeight(50)
        self.convert_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                background-color: #2196F3;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        layout.addWidget(self.convert_btn)

        return panel

    def create_right_panel(self):
        tab_widget = QTabWidget()

        # History tab
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)

        self.history_list = QListWidget()
        history_layout.addWidget(QLabel("Conversion History:"))
        history_layout.addWidget(self.history_list)

        history_buttons = QHBoxLayout()
        self.clear_history_btn = QPushButton("Clear History")
        self.open_output_btn = QPushButton("Open Output Folder")
        history_buttons.addWidget(self.clear_history_btn)
        history_buttons.addWidget(self.open_output_btn)
        history_buttons.addStretch()

        history_layout.addLayout(history_buttons)
        tab_widget.addTab(history_tab, "History")

        # Settings tab
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)

        settings_info = QLabel("Configure advanced conversion settings for optimal results.")
        settings_layout.addWidget(settings_info)

        self.advanced_settings_btn = QPushButton("Open Advanced Settings")
        self.advanced_settings_btn.setMinimumHeight(40)
        settings_layout.addWidget(self.advanced_settings_btn)

        self.settings_text = QTextEdit()
        self.settings_text.setPlainText("Click 'Open Advanced Settings' to configure detailed conversion parameters.")
        self.settings_text.setReadOnly(True)
        settings_layout.addWidget(self.settings_text)

        tab_widget.addTab(settings_tab, "Advanced")

        return tab_widget

    def setup_connections(self):
        self.add_files_btn.clicked.connect(self.browse_files)
        self.remove_files_btn.clicked.connect(self.remove_selected_files)
        self.clear_files_btn.clicked.connect(self.clear_all_files)
        self.browse_output_btn.clicked.connect(self.browse_output_directory)
        self.convert_btn.clicked.connect(self.start_conversion)
        self.clear_history_btn.clicked.connect(self.clear_history)
        self.open_output_btn.clicked.connect(self.open_output_folder)
        self.advanced_settings_btn.clicked.connect(self.open_advanced_settings)
        self.file_list.itemSelectionChanged.connect(self.on_file_selection_changed)

    def add_files(self, file_paths):
        if self.file_list.count() == 1 and self.file_list.item(0).flags() == Qt.NoItemFlags:
            self.file_list.clear()

        for file_path in file_paths:
            if os.path.isfile(file_path):
                item = QListWidgetItem(os.path.basename(file_path))
                item.setData(Qt.UserRole, file_path)
                self.file_list.addItem(item)

        self.update_output_formats()

    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files to Convert",
            "",
            "All Files (*.*)"
        )
        if files:
            self.add_files(files)

    def remove_selected_files(self):
        for item in self.file_list.selectedItems():
            row = self.file_list.row(item)
            self.file_list.takeItem(row)

        if self.file_list.count() == 0:
            placeholder_item = QListWidgetItem("Drag & drop files here or click 'Add Files' below")
            placeholder_item.setFlags(Qt.NoItemFlags)
            placeholder_item.setTextAlignment(Qt.AlignCenter)
            self.file_list.addItem(placeholder_item)

        self.update_output_formats()

    def clear_all_files(self):
        self.file_list.clear()
        placeholder_item = QListWidgetItem("Drag & drop files here or click 'Add Files' below")
        placeholder_item.setFlags(Qt.NoItemFlags)
        placeholder_item.setTextAlignment(Qt.AlignCenter)
        self.file_list.addItem(placeholder_item)
        self.update_output_formats()

    def browse_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_dir_label.setText(directory)

    def update_output_formats(self):
        self.output_format_combo.clear()

        if self.file_list.count() == 0 or (self.file_list.count() == 1 and self.file_list.item(0).flags() == Qt.NoItemFlags):
            return

        file_paths = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.flags() != Qt.NoItemFlags:
                file_paths.append(item.data(Qt.UserRole))

        if file_paths:
            suggested_formats = self.file_detector.get_suggested_formats(file_paths)
            self.output_format_combo.addItems(suggested_formats)

    def on_file_selection_changed(self):
        self.remove_files_btn.setEnabled(len(self.file_list.selectedItems()) > 0)

    def start_conversion(self):
        if self.file_list.count() == 0 or (self.file_list.count() == 1 and self.file_list.item(0).flags() == Qt.NoItemFlags):
            QMessageBox.warning(self, "Warning", "Please add files to convert.")
            return

        if not self.output_format_combo.currentText():
            QMessageBox.warning(self, "Warning", "Please select an output format.")
            return

        # Prepare file information
        files_info = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.flags() != Qt.NoItemFlags:
                file_path = item.data(Qt.UserRole)
                file_info = self.file_detector.get_file_info(file_path)
                if file_info:
                    files_info.append(file_info)

        if not files_info:
            QMessageBox.warning(self, "Warning", "No valid files to convert.")
            return

        # Get output directory
        output_dir = None
        if self.output_dir_label.text() != "Same as source files":
            output_dir = self.output_dir_label.text()

        # Setup UI for conversion
        self.convert_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Starting conversion...")

        # Connect conversion manager signals
        self.conversion_manager.conversion_progress.connect(self.update_progress)
        self.conversion_manager.conversion_finished.connect(self.conversion_completed)

        # Start conversion
        success = self.conversion_manager.start_conversion(
            files_info,
            self.output_format_combo.currentText(),
            output_dir
        )

        if not success:
            QMessageBox.warning(self, "Warning", "Could not start conversion. Another conversion may be in progress.")
            self.reset_conversion_ui()

    def update_progress(self, progress, message):
        """Update progress bar and status message."""
        self.progress_bar.setValue(progress)
        self.status_label.setText(message)

    def conversion_completed(self, success, message):
        """Handle conversion completion."""
        self.progress_bar.setValue(100)
        self.status_label.setText(message)

        if success:
            QMessageBox.information(self, "Success", message)

            # Add to history
            file_paths = []
            for i in range(self.file_list.count()):
                item = self.file_list.item(i)
                if item.flags() != Qt.NoItemFlags:
                    file_paths.append(item.data(Qt.UserRole))

            output_dir = self.output_dir_label.text()
            if output_dir == "Same as source files":
                output_dir = "Various locations"

            self.history_manager.add_conversion(
                file_paths,
                self.output_format_combo.currentText(),
                output_dir,
                True
            )
            self.update_history_display()
        else:
            QMessageBox.critical(self, "Error", f"Conversion failed: {message}")

        self.reset_conversion_ui()

    def reset_conversion_ui(self):
        """Reset UI after conversion."""
        self.convert_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Ready to convert")

    def update_history_display(self):
        """Update the history list display."""
        self.history_list.clear()
        history = self.history_manager.get_history(20)

        for record in history:
            timestamp = record['timestamp'][:19].replace('T', ' ')
            file_count = record['file_count']
            output_format = record['output_format']
            status = "✓" if record['success'] else "✗"

            item_text = f"{status} {timestamp} - {file_count} file(s) → {output_format}"
            self.history_list.addItem(item_text)

    def clear_history(self):
        self.history_list.clear()
        self.history_manager.clear_history()

    def open_output_folder(self):
        """Open the output folder in file manager."""
        output_dir = self.output_dir_label.text()
        if output_dir == "Same as source files":
            if self.file_list.count() > 0:
                item = self.file_list.item(0)
                if item and item.flags() != Qt.NoItemFlags:
                    file_path = item.data(Qt.UserRole)
                    output_dir = os.path.dirname(file_path)
                else:
                    QMessageBox.information(self, "Info", "No output directory specified.")
                    return
            else:
                QMessageBox.information(self, "Info", "No files selected.")
                return

        if os.path.exists(output_dir):
            # Open folder in file manager (cross-platform)
            import subprocess
            import platform

            system = platform.system()
            if system == "Windows":
                subprocess.run(f'explorer "{output_dir}"', shell=True)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", output_dir])
            else:  # Linux and others
                subprocess.run(["xdg-open", output_dir])
        else:
            QMessageBox.warning(self, "Warning", f"Output directory does not exist: {output_dir}")

    def open_advanced_settings(self):
        """Open advanced settings dialog."""
        dialog = AdvancedSettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            settings = dialog.get_settings()
            self.settings_text.setPlainText(f"Settings updated successfully!\n\nCurrent configuration:\n- Image quality: {settings['image_quality']}%\n- Audio bitrate: {settings['audio_bitrate']}\n- Video CRF: {settings['video_crf']}\n- Threads: {settings['thread_count']}")

            # Apply settings to conversion manager
            self.conversion_manager.update_settings(settings)