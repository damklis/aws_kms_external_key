from datetime import date
from dataclasses import dataclass
import boto3
from botocore.exceptions import ClientError
from import_key_material.public_key_encryptor import PublicKeyEncryptor


def kms_client(class_):
    class_.kms_client = boto3.client("kms")
    return class_


@kms_client
@dataclass(frozen=True)
class KMSExternalKey:
    key_id: str
    key_material: bytes
    algorithm: str = "RSAES_OAEP_SHA_256"

    def get_parameters_for_import(self):
        try:
            response = self.kms_client.get_parameters_for_import(
                KeyId=self.key_id,
                WrappingAlgorithm=self.algorithm,
                WrappingKeySpec='RSA_2048',
            )
            token = response.get("ImportToken")
            public_key = response.get("PublicKey")
            return public_key, token
        except ClientError as err:
            print(f"Client error: {err}")
            return None, None


@kms_client
class KMSExternalKeyImporter:
    def __init__(self):
        self.encryptor = PublicKeyEncryptor()

    def import_external_key_to_kms(self, kms_external_key):
        if not isinstance(kms_external_key, KMSExternalKey):
            raise TypeError(f"Must be an instance of KMSExternalKey")

        wrapping_key, token = kms_external_key.get_parameters_for_import()
        encrypted_key_material = self.encryptor.encrypt_key_material(
            key_material=kms_external_key.key_material,
            wrapping_key=wrapping_key,
        )

        return self.kms_client.import_key_material(
            KeyId=kms_external_key.key_id,
            ImportToken=token,
            EncryptedKeyMaterial=encrypted_key_material,
            ExpirationModel='KEY_MATERIAL_DOES_NOT_EXPIRE',
        )
