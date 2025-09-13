import os
import zipfile
import tarfile
import shutil
from .base_converter import BaseConverter

try:
    import py7zr
    PY7ZR_AVAILABLE = True
except ImportError:
    PY7ZR_AVAILABLE = False

try:
    import rarfile
    RARFILE_AVAILABLE = True
except ImportError:
    RARFILE_AVAILABLE = False

class ArchiveConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = [
            'zip', 'rar', '7z', 'tar', 'gz', 'tar.gz', 'tar.bz2'
        ]
        self.supported_output_formats = [
            'zip', '7z', 'tar.gz'
        ]

    def convert(self, input_path, output_format, output_directory):
        """Convert archive files between different formats."""
        try:
            if not self.ensure_output_directory(output_directory):
                return False

            # Extract to temporary directory first
            temp_extract_dir = os.path.join(output_directory, 'temp_extract')
            if not self._extract_archive(input_path, temp_extract_dir):
                return False

            # Create new archive in desired format
            output_path = self.get_output_filename(input_path, output_format, output_directory)
            success = self._create_archive(temp_extract_dir, output_path, output_format)

            # Clean up temporary directory
            if os.path.exists(temp_extract_dir):
                shutil.rmtree(temp_extract_dir)

            return success

        except Exception as e:
            print(f"Archive conversion error: {str(e)}")
            return False

    def _extract_archive(self, archive_path, extract_dir):
        """Extract archive to specified directory."""
        try:
            os.makedirs(extract_dir, exist_ok=True)
            file_extension = self.get_file_extension(archive_path).lower()

            if file_extension == 'zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                return True

            elif file_extension == '7z':
                if not PY7ZR_AVAILABLE:
                    print("py7zr not available for 7z extraction")
                    return False
                with py7zr.SevenZipFile(archive_path, mode='r') as archive:
                    archive.extractall(path=extract_dir)
                return True

            elif file_extension == 'rar':
                if not RARFILE_AVAILABLE:
                    print("rarfile not available for RAR extraction")
                    return False
                with rarfile.RarFile(archive_path) as rf:
                    rf.extractall(extract_dir)
                return True

            elif file_extension in ['tar', 'tar.gz', 'tar.bz2', 'gz']:
                mode = 'r'
                if archive_path.endswith('.gz'):
                    mode = 'r:gz'
                elif archive_path.endswith('.bz2'):
                    mode = 'r:bz2'

                with tarfile.open(archive_path, mode) as tar:
                    tar.extractall(path=extract_dir)
                return True

            return False

        except Exception as e:
            print(f"Archive extraction error: {str(e)}")
            return False

    def _create_archive(self, source_dir, output_path, output_format):
        """Create archive from directory contents."""
        try:
            if output_format.lower() == 'zip':
                return self._create_zip(source_dir, output_path)
            elif output_format.lower() == '7z':
                return self._create_7z(source_dir, output_path)
            elif output_format.lower() == 'tar.gz':
                return self._create_tar_gz(source_dir, output_path)

            return False

        except Exception as e:
            print(f"Archive creation error: {str(e)}")
            return False

    def _create_zip(self, source_dir, output_path):
        """Create ZIP archive."""
        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arc_name)
            return True

        except Exception as e:
            print(f"ZIP creation error: {str(e)}")
            return False

    def _create_7z(self, source_dir, output_path):
        """Create 7Z archive."""
        if not PY7ZR_AVAILABLE:
            print("py7zr not available for 7z creation")
            return False

        try:
            with py7zr.SevenZipFile(output_path, 'w') as archive:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, source_dir)
                        archive.write(file_path, arc_name)
            return True

        except Exception as e:
            print(f"7Z creation error: {str(e)}")
            return False

    def _create_tar_gz(self, source_dir, output_path):
        """Create TAR.GZ archive."""
        try:
            with tarfile.open(output_path, 'w:gz') as tar:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, source_dir)
                        tar.add(file_path, arcname=arc_name)
            return True

        except Exception as e:
            print(f"TAR.GZ creation error: {str(e)}")
            return False

    def extract_archive(self, archive_path, extract_dir):
        """Public method to extract any supported archive."""
        return self._extract_archive(archive_path, extract_dir)

    def create_archive_from_files(self, file_list, output_path, archive_format):
        """Create archive from list of files."""
        try:
            if archive_format.lower() == 'zip':
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in file_list:
                        if os.path.exists(file_path):
                            zipf.write(file_path, os.path.basename(file_path))
                return True

            elif archive_format.lower() == '7z' and PY7ZR_AVAILABLE:
                with py7zr.SevenZipFile(output_path, 'w') as archive:
                    for file_path in file_list:
                        if os.path.exists(file_path):
                            archive.write(file_path, os.path.basename(file_path))
                return True

            return False

        except Exception as e:
            print(f"Archive creation from files error: {str(e)}")
            return False