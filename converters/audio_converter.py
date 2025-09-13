import os
import subprocess
from .base_converter import BaseConverter

class AudioConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = [
            'mp3', 'wav', 'ogg', 'flac', 'aac', 'wma', 'm4a', 'mp4', 'avi', 'mkv'
        ]
        self.supported_output_formats = [
            'mp3', 'wav', 'ogg', 'flac', 'aac'
        ]

    def convert(self, input_path, output_format, output_directory):
        """Convert audio files using ffmpeg."""
        try:
            if not self.ensure_output_directory(output_directory):
                return False

            if not self._check_ffmpeg():
                print("FFmpeg not found. Please install FFmpeg for audio conversion.")
                return False

            output_path = self.get_output_filename(input_path, output_format, output_directory)

            # Build ffmpeg command
            cmd = ['ffmpeg', '-i', input_path, '-y']

            # Add format-specific options
            if output_format.lower() == 'mp3':
                cmd.extend(['-codec:a', 'libmp3lame', '-b:a', '192k'])
            elif output_format.lower() == 'wav':
                cmd.extend(['-codec:a', 'pcm_s16le'])
            elif output_format.lower() == 'ogg':
                cmd.extend(['-codec:a', 'libvorbis', '-q:a', '5'])
            elif output_format.lower() == 'flac':
                cmd.extend(['-codec:a', 'flac'])
            elif output_format.lower() == 'aac':
                cmd.extend(['-codec:a', 'aac', '-b:a', '192k'])

            cmd.append(output_path)

            # Execute conversion
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                return os.path.exists(output_path)
            else:
                print(f"FFmpeg error: {result.stderr}")
                return False

        except Exception as e:
            print(f"Audio conversion error: {str(e)}")
            return False

    def _check_ffmpeg(self):
        """Check if ffmpeg is available."""
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False

    def extract_audio_from_video(self, video_path, output_format, output_directory):
        """Extract audio from video file."""
        try:
            if not self.ensure_output_directory(output_directory):
                return False

            if not self._check_ffmpeg():
                return False

            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(output_directory, f"{base_name}.{output_format}")

            cmd = ['ffmpeg', '-i', video_path, '-vn', '-y']

            # Add format-specific options for audio extraction
            if output_format.lower() == 'mp3':
                cmd.extend(['-codec:a', 'libmp3lame', '-b:a', '192k'])
            elif output_format.lower() == 'wav':
                cmd.extend(['-codec:a', 'pcm_s16le'])
            elif output_format.lower() == 'aac':
                cmd.extend(['-codec:a', 'aac', '-b:a', '192k'])

            cmd.append(output_path)

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.returncode == 0 and os.path.exists(output_path)

        except Exception as e:
            print(f"Audio extraction error: {str(e)}")
            return False

    def change_audio_quality(self, input_path, output_path, bitrate='192k'):
        """Change audio quality/bitrate."""
        try:
            if not self._check_ffmpeg():
                return False

            cmd = [
                'ffmpeg', '-i', input_path,
                '-codec:a', 'libmp3lame',
                '-b:a', bitrate,
                '-y', output_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.returncode == 0

        except Exception as e:
            print(f"Audio quality change error: {str(e)}")
            return False