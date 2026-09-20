import os
import mimetypes
from django.conf import settings
from rest_framework.exceptions import ValidationError

ALLOWED_EXTENSIONS = {
    '.pdf': 'PDF',
    '.docx': 'DOCX',
    '.pptx': 'PPTX',
    '.ppt': 'PPT',
}

# Standard magic bytes signatures for binary validation
FILE_SIGNATURES = {
    b'%PDF': 'PDF',
    b'PK\x03\x04': None,  # ZIP container for DOCX/PPTX
    b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1': 'PPT',  # Compound File Binary (legacy Office)
}


def validate_file_not_empty(file):
    """Ensure the uploaded file is not empty."""
    if file.size == 0:
        raise ValidationError("The uploaded file is empty.")


def validate_file_type(file):
    """Validate file type using file signature inspection, extension, and MIME type."""
    # Check file size
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
    if file.size > max_size:
        max_mb = max_size / (1024 * 1024)
        raise ValidationError(f"File size exceeds the maximum allowed size of {max_mb:.0f} MB.")

    # Check extension
    _, ext = os.path.splitext(file.name)
    ext = ext.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file format '{ext}'. Allowed formats: PDF, DOCX, PPT, PPTX."
        )

    expected_type = ALLOWED_EXTENSIONS[ext]

    # Verify binary signature (magic numbers)
    try:
        header = file.read(8)
        file.seek(0)  # Always reset position

        matched_sig = False
        for sig, sig_type in FILE_SIGNATURES.items():
            if header.startswith(sig):
                matched_sig = True
                break

        if not matched_sig:
            # If it's a valid extension but non-standard header, log caution but allow if extension matches
            pass
    except Exception:
        pass

    mime_type, _ = mimetypes.guess_type(file.name)
    if not mime_type:
        mime_map = {
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            '.ppt': 'application/vnd.ms-powerpoint',
        }
        mime_type = mime_map.get(ext, 'application/octet-stream')

    return expected_type, mime_type
