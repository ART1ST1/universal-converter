import os
import threading
from PyQt5.QtCore import QObject, pyqtSignal
from converters.document_converter import DocumentConverter
from converters.image_converter import ImageConverter
from converters.audio_converter import AudioConverter
from converters.video_converter import VideoConverter
from converters.archive_converter import ArchiveConverter
from converters.code_converter import CodeConverter

class ConversionManager(QObject):
    conversion_started = pyqtSignal()
    conversion_progress = pyqtSignal(int, str)
    conversion_finished = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
        self.converters = {
            'document': DocumentConverter(),
            'spreadsheet': DocumentConverter(),
            'presentation': DocumentConverter(),
            'image': ImageConverter(),
            'audio': AudioConverter(),
            'video': VideoConverter(),
            'archive': ArchiveConverter(),
            'code': CodeConverter()
        }
        self.is_converting = False
        self.current_thread = None
        self.settings = {}

    def update_settings(self, settings):
        """Update conversion settings."""
        self.settings = settings
        # Pass settings to converters that need them
        for converter in self.converters.values():
            if hasattr(converter, 'update_settings'):
                converter.update_settings(settings)

    def start_conversion(self, files_info, output_format, output_directory=None):
        """Start the conversion process in a separate thread."""
        if self.is_converting:
            return False

        self.is_converting = True
        self.conversion_started.emit()

        # Start conversion in separate thread
        self.current_thread = threading.Thread(
            target=self._convert_files,
            args=(files_info, output_format, output_directory)
        )
        self.current_thread.daemon = True
        self.current_thread.start()

        return True

    def _convert_files(self, files_info, output_format, output_directory):
        """Internal method to handle file conversion."""
        try:
            total_files = len(files_info)
            success_count = 0

            for i, file_info in enumerate(files_info):
                try:
                    # Update progress
                    progress = int((i / total_files) * 100)
                    self.conversion_progress.emit(progress, f"Converting {file_info['name']}...")

                    # Get appropriate converter
                    file_type = file_info['type']
                    if file_type not in self.converters:
                        continue

                    converter = self.converters[file_type]

                    # Determine output path
                    if output_directory:
                        output_dir = output_directory
                    else:
                        output_dir = os.path.dirname(file_info['path'])

                    # Convert file
                    success = converter.convert(
                        file_info['path'],
                        output_format.lower(),
                        output_dir
                    )

                    if success:
                        success_count += 1

                except Exception as e:
                    print(f"Error converting {file_info['name']}: {str(e)}")
                    continue

            # Final progress update
            self.conversion_progress.emit(100, f"Completed {success_count}/{total_files} conversions")

            # Emit completion signal
            success_message = f"Successfully converted {success_count} out of {total_files} files."
            self.conversion_finished.emit(True, success_message)

        except Exception as e:
            error_message = f"Conversion failed: {str(e)}"
            self.conversion_finished.emit(False, error_message)

        finally:
            self.is_converting = False

    def stop_conversion(self):
        """Stop the current conversion process."""
        if self.is_converting and self.current_thread:
            self.is_converting = False
            # Note: Actual thread termination would need more sophisticated handling
            return True
        return False

    def get_conversion_status(self):
        """Get the current conversion status."""
        return self.is_converting