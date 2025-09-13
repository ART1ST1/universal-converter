import os
import json
import datetime
from pathlib import Path

class HistoryManager:
    def __init__(self):
        self.history_file = os.path.join(Path.home(), '.universal_converter_history.json')
        self.load_history()

    def load_history(self):
        """Load conversion history from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            else:
                self.history = []
        except Exception:
            self.history = []

    def save_history(self):
        """Save conversion history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def add_conversion(self, source_files, output_format, output_directory, success=True):
        """Add a conversion record to history."""
        record = {
            'timestamp': datetime.datetime.now().isoformat(),
            'source_files': source_files,
            'output_format': output_format,
            'output_directory': output_directory,
            'success': success,
            'file_count': len(source_files)
        }

        self.history.insert(0, record)

        # Keep only last 100 records
        if len(self.history) > 100:
            self.history = self.history[:100]

        self.save_history()

    def get_history(self, limit=50):
        """Get recent conversion history."""
        return self.history[:limit]

    def clear_history(self):
        """Clear all conversion history."""
        self.history = []
        self.save_history()

    def remove_record(self, index):
        """Remove a specific record from history."""
        if 0 <= index < len(self.history):
            del self.history[index]
            self.save_history()
            return True
        return False

    def get_statistics(self):
        """Get conversion statistics."""
        if not self.history:
            return {
                'total_conversions': 0,
                'successful_conversions': 0,
                'failed_conversions': 0,
                'total_files_converted': 0,
                'most_used_format': 'None'
            }

        total_conversions = len(self.history)
        successful_conversions = sum(1 for record in self.history if record.get('success', False))
        failed_conversions = total_conversions - successful_conversions
        total_files_converted = sum(record.get('file_count', 0) for record in self.history)

        # Find most used format
        format_counts = {}
        for record in self.history:
            format_name = record.get('output_format', 'Unknown')
            format_counts[format_name] = format_counts.get(format_name, 0) + 1

        most_used_format = max(format_counts.keys(), key=format_counts.get) if format_counts else 'None'

        return {
            'total_conversions': total_conversions,
            'successful_conversions': successful_conversions,
            'failed_conversions': failed_conversions,
            'total_files_converted': total_files_converted,
            'most_used_format': most_used_format
        }