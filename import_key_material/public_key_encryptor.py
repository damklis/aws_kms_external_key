from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_der_public_key
from OpenSSL.crypto import (
    load_publickey, dump_publickey, FILETYPE_ASN1
)


class _DERPublicKeyConverter:

    def to_public_key(self, buffer):
        der_public_key = load_publickey(
            type=FILETYPE_ASN1,
            buffer=buffer
        )

        return self.deserialize_public_key(
            dump_publickey(
                type=FILETYPE_ASN1,
                pkey=der_public_key
            )
        )

    @staticmethod
    def deserialize_public_key(der_public_key):
        return load_der_public_key(
            der_public_key,
            backend=default_backend()
        )


class PublicKeyEncryptor:
    def __init__(self):
        self.algorithm = SHA256()
        self.converter = _DERPublicKeyConverter()

    def encrypt_key_material(self, key_material, wrapping_key):
        public_key = self.converter.to_public_key(
            wrapping_key
        )
        return public_key.encrypt(
            key_material,
            padding.OAEP(
                mgf=padding.MGF1(
                    algorithm=self.algorithm
                ),
                algorithm=self.algorithm,
                label=None
            )
        )
