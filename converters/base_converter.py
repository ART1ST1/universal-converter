import os
from abc import ABC, abstractmethod

class BaseConverter(ABC):
    def __init__(self):
        self.supported_input_formats = []
        self.supported_output_formats = []

    @abstractmethod
    def convert(self, input_path, output_format, output_directory):
        """Convert a file from input_path to output_format in output_directory."""
        pass

    def is_format_supported(self, input_format, output_format):
        """Check if conversion from input_format to output_format is supported."""
        return (input_format.lower() in [fmt.lower() for fmt in self.supported_input_formats] and
                output_format.lower() in [fmt.lower() for fmt in self.supported_output_formats])

    def get_output_filename(self, input_path, output_format, output_directory):
        """Generate output filename based on input file and desired format."""
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        extension = output_format.lower()

        # Handle special cases for extensions
        if extension == 'jpg':
            extension = 'jpeg'
        elif extension == 'tiff':
            extension = 'tif'

        output_filename = f"{base_name}.{extension}"
        return os.path.join(output_directory, output_filename)

    def ensure_output_directory(self, output_directory):
        """Ensure the output directory exists."""
        if not os.path.exists(output_directory):
            os.makedirs(output_directory, exist_ok=True)
        return os.path.exists(output_directory)

    def get_file_extension(self, file_path):
        """Get file extension without the dot."""
        return os.path.splitext(file_path)[1][1:].lower()