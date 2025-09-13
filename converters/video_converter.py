import os
import subprocess
from .base_converter import BaseConverter

class VideoConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = [
            'mp4', 'avi', 'mkv', 'mov', 'wmv', 'webm', 'flv', 'm4v', '3gp'
        ]
        self.supported_output_formats = [
            'mp4', 'avi', 'mkv', 'mov', 'webm', 'mp3', 'wav'
        ]

    def convert(self, input_path, output_format, output_directory):
        """Convert video files using ffmpeg."""
        try:
            if not self.ensure_output_directory(output_directory):
                return False

            if not self._check_ffmpeg():
                print("FFmpeg not found. Please install FFmpeg for video conversion.")
                return False

            output_path = self.get_output_filename(input_path, output_format, output_directory)

            # Handle audio extraction from video
            if output_format.lower() in ['mp3', 'wav', 'aac']:
                return self._extract_audio(input_path, output_path, output_format)

            # Build ffmpeg command for video conversion
            cmd = ['ffmpeg', '-i', input_path, '-y']

            # Add format-specific options
            if output_format.lower() == 'mp4':
                cmd.extend([
                    '-codec:v', 'libx264',
                    '-codec:a', 'aac',
                    '-crf', '23',
                    '-preset', 'medium'
                ])
            elif output_format.lower() == 'avi':
                cmd.extend([
                    '-codec:v', 'libxvid',
                    '-codec:a', 'libmp3lame',
                    '-q:v', '5'
                ])
            elif output_format.lower() == 'mkv':
                cmd.extend([
                    '-codec:v', 'libx264',
                    '-codec:a', 'aac',
                    '-crf', '23'
                ])
            elif output_format.lower() == 'webm':
                cmd.extend([
                    '-codec:v', 'libvpx-vp9',
                    '-codec:a', 'libopus',
                    '-crf', '30',
                    '-b:v', '0'
                ])
            elif output_format.lower() == 'mov':
                cmd.extend([
                    '-codec:v', 'libx264',
                    '-codec:a', 'aac',
                    '-crf', '23'
                ])

            cmd.append(output_path)

            # Execute conversion
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 minutes timeout

            if result.returncode == 0:
                return os.path.exists(output_path)
            else:
                print(f"FFmpeg error: {result.stderr}")
                return False

        except Exception as e:
            print(f"Video conversion error: {str(e)}")
            return False

    def _extract_audio(self, input_path, output_path, audio_format):
        """Extract audio from video file."""
        try:
            cmd = ['ffmpeg', '-i', input_path, '-vn', '-y']

            if audio_format.lower() == 'mp3':
                cmd.extend(['-codec:a', 'libmp3lame', '-b:a', '192k'])
            elif audio_format.lower() == 'wav':
                cmd.extend(['-codec:a', 'pcm_s16le'])
            elif audio_format.lower() == 'aac':
                cmd.extend(['-codec:a', 'aac', '-b:a', '192k'])

            cmd.append(output_path)

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            return result.returncode == 0 and os.path.exists(output_path)

        except Exception as e:
            print(f"Audio extraction error: {str(e)}")
            return False

    def _check_ffmpeg(self):
        """Check if ffmpeg is available."""
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False

    def compress_video(self, input_path, output_path, crf=28):
        """Compress video to reduce file size."""
        try:
            if not self._check_ffmpeg():
                return False

            cmd = [
                'ffmpeg', '-i', input_path,
                '-codec:v', 'libx264',
                '-crf', str(crf),
                '-codec:a', 'aac',
                '-b:a', '128k',
                '-preset', 'slow',
                '-y', output_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            return result.returncode == 0

        except Exception as e:
            print(f"Video compression error: {str(e)}")
            return False

    def resize_video(self, input_path, output_path, width, height):
        """Resize video to specified dimensions."""
        try:
            if not self._check_ffmpeg():
                return False

            cmd = [
                'ffmpeg', '-i', input_path,
                '-vf', f'scale={width}:{height}',
                '-codec:a', 'copy',
                '-y', output_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            return result.returncode == 0

        except Exception as e:
            print(f"Video resize error: {str(e)}")
            return False