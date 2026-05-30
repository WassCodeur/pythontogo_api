import base64

from imagekitio import ImageKit
from app.core.settings import settings


imagekit = ImageKit(
    private_key=settings.imagekit_private_key
)

URL_ENDPOINT = settings.imagekit_url_endpoint


async def upload_image_base64_url(image_name, base64_string, folder=""):
    try:
        upload_response = imagekit.files.upload(
            file=base64.b64decode(base64_string),
            file_name=image_name,
            folder="/pythontogo/" + folder.lstrip("/"),

        )
        return upload_response
    except Exception as e:
        raise Exception(f"Error uploading image: {str(e)}")
