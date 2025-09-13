import os
from .base_converter import BaseConverter

try:
    from PIL import Image, ImageEnhance
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class ImageConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = [
            'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'ico'
        ]
        self.supported_output_formats = [
            'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'ico', 'pdf'
        ]

    def convert(self, input_path, output_format, output_directory):
        """Convert image files using PIL/Pillow."""
        if not PIL_AVAILABLE:
            print("PIL/Pillow not available for image conversion")
            return False

        try:
            if not self.ensure_output_directory(output_directory):
                return False

            output_path = self.get_output_filename(input_path, output_format, output_directory)

            # Open the image
            with Image.open(input_path) as img:
                # Convert image mode if necessary
                if output_format.lower() in ['jpg', 'jpeg']:
                    if img.mode in ['RGBA', 'LA', 'P']:
                        # Create white background for transparent images
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background

                elif output_format.lower() == 'png':
                    if img.mode not in ['RGBA', 'RGB', 'L']:
                        img = img.convert('RGBA')

                elif output_format.lower() == 'gif':
                    if img.mode not in ['P', 'RGB']:
                        img = img.convert('P', palette=Image.ADAPTIVE)

                elif output_format.lower() == 'bmp':
                    if img.mode not in ['RGB', 'L']:
                        img = img.convert('RGB')

                # Handle PDF conversion
                if output_format.lower() == 'pdf':
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.save(output_path, 'PDF', resolution=100.0)
                else:
                    # Save with appropriate quality settings
                    save_kwargs = {}
                    if output_format.lower() in ['jpg', 'jpeg']:
                        save_kwargs['quality'] = 95
                        save_kwargs['optimize'] = True

                    img.save(output_path, **save_kwargs)

            return os.path.exists(output_path)

        except Exception as e:
            print(f"Image conversion error: {str(e)}")
            return False

    def resize_image(self, input_path, output_path, width, height, maintain_aspect=True):
        """Resize an image to specified dimensions."""
        if not PIL_AVAILABLE:
            return False

        try:
            with Image.open(input_path) as img:
                if maintain_aspect:
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                else:
                    img = img.resize((width, height), Image.Resampling.LANCZOS)

                img.save(output_path, quality=95, optimize=True)
            return True

        except Exception as e:
            print(f"Image resize error: {str(e)}")
            return False

    def compress_image(self, input_path, output_path, quality=85):
        """Compress an image to reduce file size."""
        if not PIL_AVAILABLE:
            return False

        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary for JPEG compression
                if img.mode in ['RGBA', 'LA']:
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background

                img.save(output_path, 'JPEG', quality=quality, optimize=True)
            return True

        except Exception as e:
            print(f"Image compression error: {str(e)}")
            return False