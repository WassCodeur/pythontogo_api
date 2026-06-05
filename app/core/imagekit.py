import base64

from imagekitio import ImageKit
from app.core.settings import settings

_client: ImageKit | None = None


def _get_client() -> ImageKit:
    global _client
    if _client is None:
        if not settings.imagekit_private_key:
            raise RuntimeError(
                "IMAGEKIT_PRIVATE_KEY is not set. Configure it to use ImageKit."
            )
        _client = ImageKit(private_key=settings.imagekit_private_key)
    return _client


def upload_image_base64_url(image_name: str, base64_string: str, folder: str = ""):
    try:
        client = _get_client()
        upload_response = client.files.upload(
            file=base64.b64decode(base64_string),
            file_name=image_name,
            folder="/pythontogo/" + folder.lstrip("/"),
        )
        return upload_response
    except Exception as e:
        raise Exception(f"Error uploading image: {str(e)}")
