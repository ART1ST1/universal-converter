import os
import mimetypes
from pathlib import Path

class FileDetector:
    def __init__(self):
        # Initialize mimetypes
        mimetypes.init()

        # Define supported conversions by category
        self.format_mappings = {
            'document': {
                'extensions': ['.docx', '.doc', '.pdf', '.txt', '.odt', '.rtf', '.html', '.md'],
                'output_formats': ['PDF', 'DOCX', 'TXT', 'RTF', 'HTML', 'ODT']
            },
            'spreadsheet': {
                'extensions': ['.xlsx', '.xls', '.csv', '.ods'],
                'output_formats': ['XLSX', 'CSV', 'ODS', 'PDF']
            },
            'presentation': {
                'extensions': ['.pptx', '.ppt', '.odp'],
                'output_formats': ['PPTX', 'PDF', 'ODP']
            },
            'image': {
                'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.ico'],
                'output_formats': ['JPG', 'PNG', 'GIF', 'BMP', 'TIFF', 'WEBP', 'ICO', 'PDF']
            },
            'audio': {
                'extensions': ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.wma', '.m4a'],
                'output_formats': ['MP3', 'WAV', 'OGG', 'FLAC', 'AAC']
            },
            'video': {
                'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.webm', '.flv', '.m4v'],
                'output_formats': ['MP4', 'AVI', 'MKV', 'MOV', 'WEBM', 'MP3', 'WAV']
            },
            'archive': {
                'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.tar.gz', '.tar.bz2'],
                'output_formats': ['ZIP', '7Z', 'TAR.GZ']
            },
            'code': {
                'extensions': ['.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.php', '.rb', '.go'],
                'output_formats': ['PDF', 'DOCX', 'HTML', 'TXT']
            }
        }

    def get_file_type(self, file_path):
        """Detect the file type based on extension and mime type."""
        extension = Path(file_path).suffix.lower()

        for category, info in self.format_mappings.items():
            if extension in info['extensions']:
                return category

        # Fallback to mime type detection
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            if mime_type.startswith('image/'):
                return 'image'
            elif mime_type.startswith('audio/'):
                return 'audio'
            elif mime_type.startswith('video/'):
                return 'video'
            elif mime_type.startswith('text/'):
                return 'document'

        return 'unknown'

    def get_supported_formats(self, file_type):
        """Get supported output formats for a given file type."""
        if file_type in self.format_mappings:
            return self.format_mappings[file_type]['output_formats']
        return []

    def get_suggested_formats(self, file_paths):
        """Get suggested output formats based on the input files."""
        if not file_paths:
            return []

        # Analyze all files and find common output formats
        all_formats = set()
        file_types = set()

        for file_path in file_paths:
            file_type = self.get_file_type(file_path)
            file_types.add(file_type)
            formats = self.get_supported_formats(file_type)
            if not all_formats:
                all_formats = set(formats)
            else:
                all_formats &= set(formats)

        # If no common formats, return formats for the most common file type
        if not all_formats:
            if len(file_types) == 1:
                file_type = list(file_types)[0]
                return self.get_supported_formats(file_type)
            else:
                # Return most universal formats
                return ['PDF', 'ZIP']

        return sorted(list(all_formats))

    def is_supported(self, file_path):
        """Check if a file is supported for conversion."""
        return self.get_file_type(file_path) != 'unknown'

    def get_file_info(self, file_path):
        """Get detailed information about a file."""
        if not os.path.exists(file_path):
            return None

        file_type = self.get_file_type(file_path)
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        extension = Path(file_path).suffix.lower()

        return {
            'name': file_name,
            'path': file_path,
            'type': file_type,
            'extension': extension,
            'size': file_size,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'supported_formats': self.get_supported_formats(file_type)
        }