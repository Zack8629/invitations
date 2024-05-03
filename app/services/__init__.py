from cryptography.fernet import Fernet

from app.services.crypto import Crypto
from app.services.qr import GenerateQR
from app.services.short_link import LinkShortener
from config import BASE_URL, SHORT_BASE_URL

crypto = Crypto(Fernet)
link_shortener = LinkShortener(BASE_URL, SHORT_BASE_URL)

generate_qr = GenerateQR()
