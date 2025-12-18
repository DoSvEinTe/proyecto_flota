"""
Validadores de seguridad personalizados para archivos.

🔒 OWASP #4: Insecure Design - Validación de Uploads
"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os

try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False


# Extensiones permitidas por categoría
ALLOWED_EXTENSIONS = {
    'images': {'.jpg', '.jpeg', '.png', '.gif', '.webp'},
    'documents': {'.pdf', '.doc', '.docx', '.xlsx', '.xls', '.txt'},
    'certificates': {'.pdf', '.jpg', '.jpeg', '.png'},
}

# Tipos MIME permitidos (basado en extensión esperada)
ALLOWED_MIMETYPES = {
    'images': {'image/jpeg', 'image/png', 'image/gif', 'image/webp'},
    'documents': {'application/pdf', 'application/msword', 
                  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                  'application/vnd.ms-excel',
                  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                  'text/plain'},
}

# Tamaños máximos por tipo (en MB)
MAX_FILE_SIZES = {
    'images': 10,          # Fotos de cédula/licencia: 10 MB
    'documents': 50,       # PDFs y documentos: 50 MB
    'comprobantes': 10,    # Comprobantes: 10 MB
}


def validate_file_upload(file, file_type='documents'):
    """
    Validador personalizado para uploads.
    
    Verificar:
    1. Extensión del archivo
    2. Tipo MIME real (no solo extensión)
    3. Tamaño máximo
    4. No contiene malware (opcional)
    
    Args:
        file: El archivo subido (UploadedFile)
        file_type: 'images', 'documents', 'certificates', 'comprobantes'
    
    Raises:
        ValidationError: Si el archivo no cumple los criterios
    """
    
    if not file:
        return
    
    # 1. Verificar tamaño
    max_size_mb = MAX_FILE_SIZES.get(file_type, 10)
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if file.size > max_size_bytes:
        raise ValidationError(
            _('El archivo es demasiado grande. Máximo: %(max)s MB'),
            code='file_too_large',
            params={'max': max_size_mb}
        )
    
    # 2. Verificar extensión
    file_name = file.name.lower()
    file_ext = os.path.splitext(file_name)[1]
    
    allowed_exts = ALLOWED_EXTENSIONS.get(file_type, set())
    if file_ext not in allowed_exts:
        raise ValidationError(
            _('Extensión de archivo no permitida: %(ext)s. Permitidas: %(allowed)s'),
            code='invalid_extension',
            params={'ext': file_ext, 'allowed': ', '.join(allowed_exts)}
        )
    
    # 3. Verificar MIME type (con magic library si está disponible)
    if HAS_MAGIC:
        try:
            # Leer primeros bytes del archivo para detectar tipo real
            file.seek(0)
            file_content = file.read(4096)  # Leer 4KB
            file.seek(0)  # Volver al inicio
            
            # Detectar MIME type real
            mime = magic.from_buffer(file_content, mime=True)
            
            allowed_mimes = ALLOWED_MIMETYPES.get(file_type, set())
            if mime not in allowed_mimes:
                raise ValidationError(
                    _('Tipo de archivo no permitido: %(mime)s'),
                    code='invalid_mimetype',
                    params={'mime': mime}
                )
        except ValidationError:
            raise  # Re-lanzar errores de validación
        except Exception as e:
            # Si falla detección MIME, al menos verificamos extensión
            # (mejor que bloquear todo)
            if 'magic' not in str(e).lower():  # Si no es problema de librería
                raise
    
    # 4. Verificar que no sea ejecutable (protección adicional)
    dangerous_extensions = {'.exe', '.bat', '.cmd', '.sh', '.com', '.pif', '.scr', '.vbs', '.js'}
    if file_ext in dangerous_extensions:
        raise ValidationError(
            _('Tipo de archivo potencialmente peligroso no permitido.'),
            code='dangerous_file'
        )


def validate_image_file(file):
    """Validador para imágenes (cédulas, licencias, fotos)"""
    return validate_file_upload(file, file_type='images')


def validate_document_file(file):
    """Validador para documentos (PDFs, Word, Excel)"""
    return validate_file_upload(file, file_type='documents')


def validate_comprobante_file(file):
    """Validador para comprobantes (fotos, PDFs)"""
    return validate_file_upload(file, file_type='comprobantes')
