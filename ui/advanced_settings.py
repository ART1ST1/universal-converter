from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QGroupBox, QLabel, QSpinBox, QSlider, QCheckBox,
                             QComboBox, QPushButton, QFormLayout, QLineEdit,
                             QTextEdit, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
import json
import os
from pathlib import Path

class AdvancedSettingsDialog(QDialog):
    settings_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_file = os.path.join(Path.home(), '.universal_converter_settings.json')
        self.load_settings()
        self.setup_ui()
        self.load_ui_values()

    def setup_ui(self):
        self.setWindowTitle("Advanced Settings")
        self.setModal(True)
        self.resize(600, 500)

        layout = QVBoxLayout(self)

        # Create tab widget
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Image settings tab
        image_tab = self.create_image_settings_tab()
        tab_widget.addTab(image_tab, "Image Settings")

        # Audio/Video settings tab
        media_tab = self.create_media_settings_tab()
        tab_widget.addTab(media_tab, "Audio/Video Settings")

        # Document settings tab
        document_tab = self.create_document_settings_tab()
        tab_widget.addTab(document_tab, "Document Settings")

        # General settings tab
        general_tab = self.create_general_settings_tab()
        tab_widget.addTab(general_tab, "General Settings")

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.reset_btn = QPushButton("Reset to Defaults")

        button_layout.addStretch()
        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)

        layout.addLayout(button_layout)

        # Connect buttons
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn.clicked.connect(self.reject)
        self.reset_btn.clicked.connect(self.reset_to_defaults)

    def create_image_settings_tab(self):
        tab = QGroupBox()
        layout = QFormLayout(tab)

        # Image quality
        self.image_quality_slider = QSlider(Qt.Horizontal)
        self.image_quality_slider.setRange(10, 100)
        self.image_quality_slider.setValue(95)
        self.image_quality_label = QLabel("95")
        self.image_quality_slider.valueChanged.connect(
            lambda v: self.image_quality_label.setText(str(v))
        )

        quality_layout = QHBoxLayout()
        quality_layout.addWidget(self.image_quality_slider)
        quality_layout.addWidget(self.image_quality_label)

        layout.addRow("JPEG Quality:", quality_layout)

        # Image resize options
        self.resize_images = QCheckBox("Resize images during conversion")
        layout.addRow(self.resize_images)

        self.max_width = QSpinBox()
        self.max_width.setRange(100, 10000)
        self.max_width.setValue(1920)
        self.max_width.setEnabled(False)
        layout.addRow("Max Width (px):", self.max_width)

        self.max_height = QSpinBox()
        self.max_height.setRange(100, 10000)
        self.max_height.setValue(1080)
        self.max_height.setEnabled(False)
        layout.addRow("Max Height (px):", self.max_height)

        self.maintain_aspect_ratio = QCheckBox("Maintain aspect ratio")
        self.maintain_aspect_ratio.setChecked(True)
        self.maintain_aspect_ratio.setEnabled(False)
        layout.addRow(self.maintain_aspect_ratio)

        # Connect resize checkbox
        self.resize_images.toggled.connect(self.max_width.setEnabled)
        self.resize_images.toggled.connect(self.max_height.setEnabled)
        self.resize_images.toggled.connect(self.maintain_aspect_ratio.setEnabled)

        return tab

    def create_media_settings_tab(self):
        tab = QGroupBox()
        layout = QFormLayout(tab)

        # Audio quality
        self.audio_bitrate = QComboBox()
        self.audio_bitrate.addItems(["128k", "192k", "256k", "320k"])
        self.audio_bitrate.setCurrentText("192k")
        layout.addRow("Audio Bitrate:", self.audio_bitrate)

        # Video quality
        self.video_crf = QSpinBox()
        self.video_crf.setRange(0, 51)
        self.video_crf.setValue(23)
        layout.addRow("Video CRF (0=lossless, 51=worst):", self.video_crf)

        # Video preset
        self.video_preset = QComboBox()
        self.video_preset.addItems(["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"])
        self.video_preset.setCurrentText("medium")
        layout.addRow("Video Encoding Preset:", self.video_preset)

        # Hardware acceleration
        self.hardware_acceleration = QCheckBox("Use hardware acceleration (if available)")
        layout.addRow(self.hardware_acceleration)

        return tab

    def create_document_settings_tab(self):
        tab = QGroupBox()
        layout = QFormLayout(tab)

        # PDF options
        self.pdf_compression = QCheckBox("Compress PDF files")
        self.pdf_compression.setChecked(True)
        layout.addRow(self.pdf_compression)

        # OCR options
        self.ocr_enabled = QCheckBox("Enable OCR for scanned documents")
        layout.addRow(self.ocr_enabled)

        self.ocr_language = QComboBox()
        self.ocr_language.addItems(["eng", "por", "spa", "fra", "deu"])
        self.ocr_language.setCurrentText("eng")
        self.ocr_language.setEnabled(False)
        layout.addRow("OCR Language:", self.ocr_language)

        self.ocr_enabled.toggled.connect(self.ocr_language.setEnabled)

        # Font settings for code conversion
        self.code_font = QLineEdit("Courier New")
        layout.addRow("Code Font:", self.code_font)

        self.code_font_size = QSpinBox()
        self.code_font_size.setRange(8, 24)
        self.code_font_size.setValue(10)
        layout.addRow("Code Font Size:", self.code_font_size)

        return tab

    def create_general_settings_tab(self):
        tab = QGroupBox()
        layout = QFormLayout(tab)

        # Thread count
        self.thread_count = QSpinBox()
        self.thread_count.setRange(1, 16)
        self.thread_count.setValue(4)
        layout.addRow("Conversion Threads:", self.thread_count)

        # Output naming
        self.output_naming = QComboBox()
        self.output_naming.addItems(["Keep original name", "Add format suffix", "Add timestamp"])
        layout.addRow("Output File Naming:", self.output_naming)

        # Overwrite behavior
        self.overwrite_files = QComboBox()
        self.overwrite_files.addItems(["Ask before overwriting", "Always overwrite", "Never overwrite"])
        layout.addRow("File Overwrite Behavior:", self.overwrite_files)

        # Temporary directory
        self.temp_directory = QLineEdit()
        self.temp_directory.setPlaceholderText("Use system default")
        layout.addRow("Temporary Directory:", self.temp_directory)

        # Auto-cleanup
        self.auto_cleanup = QCheckBox("Auto-cleanup temporary files")
        self.auto_cleanup.setChecked(True)
        layout.addRow(self.auto_cleanup)

        # History retention
        self.history_retention = QSpinBox()
        self.history_retention.setRange(10, 1000)
        self.history_retention.setValue(100)
        layout.addRow("History Retention (entries):", self.history_retention)

        return tab

    def load_settings(self):
        """Load settings from file."""
        self.settings = {
            'image_quality': 95,
            'resize_images': False,
            'max_width': 1920,
            'max_height': 1080,
            'maintain_aspect_ratio': True,
            'audio_bitrate': '192k',
            'video_crf': 23,
            'video_preset': 'medium',
            'hardware_acceleration': False,
            'pdf_compression': True,
            'ocr_enabled': False,
            'ocr_language': 'eng',
            'code_font': 'Courier New',
            'code_font_size': 10,
            'thread_count': 4,
            'output_naming': 'Keep original name',
            'overwrite_files': 'Ask before overwriting',
            'temp_directory': '',
            'auto_cleanup': True,
            'history_retention': 100
        }

        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    saved_settings = json.load(f)
                    self.settings.update(saved_settings)
        except Exception:
            pass

    def load_ui_values(self):
        """Load settings values into UI controls."""
        self.image_quality_slider.setValue(self.settings['image_quality'])
        self.image_quality_label.setText(str(self.settings['image_quality']))
        self.resize_images.setChecked(self.settings['resize_images'])
        self.max_width.setValue(self.settings['max_width'])
        self.max_height.setValue(self.settings['max_height'])
        self.maintain_aspect_ratio.setChecked(self.settings['maintain_aspect_ratio'])
        self.audio_bitrate.setCurrentText(self.settings['audio_bitrate'])
        self.video_crf.setValue(self.settings['video_crf'])
        self.video_preset.setCurrentText(self.settings['video_preset'])
        self.hardware_acceleration.setChecked(self.settings['hardware_acceleration'])
        self.pdf_compression.setChecked(self.settings['pdf_compression'])
        self.ocr_enabled.setChecked(self.settings['ocr_enabled'])
        self.ocr_language.setCurrentText(self.settings['ocr_language'])
        self.code_font.setText(self.settings['code_font'])
        self.code_font_size.setValue(self.settings['code_font_size'])
        self.thread_count.setValue(self.settings['thread_count'])
        self.output_naming.setCurrentText(self.settings['output_naming'])
        self.overwrite_files.setCurrentText(self.settings['overwrite_files'])
        self.temp_directory.setText(self.settings['temp_directory'])
        self.auto_cleanup.setChecked(self.settings['auto_cleanup'])
        self.history_retention.setValue(self.settings['history_retention'])

    def save_settings(self):
        """Save settings and close dialog."""
        # Update settings from UI
        self.settings['image_quality'] = self.image_quality_slider.value()
        self.settings['resize_images'] = self.resize_images.isChecked()
        self.settings['max_width'] = self.max_width.value()
        self.settings['max_height'] = self.max_height.value()
        self.settings['maintain_aspect_ratio'] = self.maintain_aspect_ratio.isChecked()
        self.settings['audio_bitrate'] = self.audio_bitrate.currentText()
        self.settings['video_crf'] = self.video_crf.value()
        self.settings['video_preset'] = self.video_preset.currentText()
        self.settings['hardware_acceleration'] = self.hardware_acceleration.isChecked()
        self.settings['pdf_compression'] = self.pdf_compression.isChecked()
        self.settings['ocr_enabled'] = self.ocr_enabled.isChecked()
        self.settings['ocr_language'] = self.ocr_language.currentText()
        self.settings['code_font'] = self.code_font.text()
        self.settings['code_font_size'] = self.code_font_size.value()
        self.settings['thread_count'] = self.thread_count.value()
        self.settings['output_naming'] = self.output_naming.currentText()
        self.settings['overwrite_files'] = self.overwrite_files.currentText()
        self.settings['temp_directory'] = self.temp_directory.text()
        self.settings['auto_cleanup'] = self.auto_cleanup.isChecked()
        self.settings['history_retention'] = self.history_retention.value()

        # Save to file
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception:
            pass

        # Emit signal and close
        self.settings_changed.emit(self.settings)
        self.accept()

    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self.load_settings()  # Reload defaults
        self.load_ui_values()

    def get_settings(self):
        """Get current settings."""
        return self.settings.copy()