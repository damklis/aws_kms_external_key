import os
from base64 import b64encode, b64decode
import pytest
from Crypto.PublicKey import RSA
from cryptography.hazmat.backends.openssl.rsa import _RSAPublicKey
from import_key_material.public_key_encryptor import (
    PublicKeyEncryptor, _DERPublicKeyConverter
)


@pytest.fixture
def pk_encryptor():
    yield PublicKeyEncryptor()


@pytest.fixture()
def pub_key_der():
    pub_key = RSA.generate(2048).publickey()
    pub_key_der = pub_key.export_key(format='DER')
    yield pub_key_der


@pytest.fixture()
def key_plain():
    yield os.urandom(32)


def test_deserialize_public_key(pk_encryptor, pub_key_der):

    converter = _DERPublicKeyConverter()

    result = converter.deserialize_public_key(
        der_public_key=pub_key_der
    )

    assert isinstance(result, _RSAPublicKey)


def test_encrypt_key_material_with_wrong_argument(
    pk_encryptor, pub_key_der
):

    test_key_plain = "Test_plain_key_as_string"

    with pytest.raises(TypeError):
        pk_encryptor.encrypt_key_material(
            test_key_plain, pub_key_der
        )


def test_encrypt_key_material(pk_encryptor, key_plain, pub_key_der):

    result = pk_encryptor.encrypt_key_material(
        key_plain, pub_key_der
    )

    assert len(result) == 256
