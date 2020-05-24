import os
import boto3
import pytest
from unittest import mock
from moto import mock_kms
from dataclasses import FrozenInstanceError
from import_key_material.external_key import (
    KMSExternalKey, KMSExternalKeyImporter
)


@pytest.fixture()
def key_material():
    yield os.urandom(32)


@pytest.fixture()
def kms_client():
    with mock_kms():
        yield boto3.client(
            "kms",
            region_name="us-east-1"
        )


@mock_kms
def test_get_parameters_for_import(key_material):

    with mock.patch("import_key_material.external_key.KMSExternalKey") \
            as external_key:

        external_key.get_parameters_for_import()
        external_key.get_parameters_for_import.assert_called()


@mock_kms
def test_adding_attributes_to_external_key(key_material):

    with pytest.raises(FrozenInstanceError):

        external_key = KMSExternalKey(
            key_id="123456789",
            key_material=key_material
        )
        external_key.test_attribute = "Test"


@mock_kms
def test_import_key_material_to_kms_with_wrong_argument():

    wrong_agrument = "Test_string"

    kms_key_importer = KMSExternalKeyImporter()

    with pytest.raises(TypeError):
        kms_key_importer.import_external_key_to_kms(
            wrong_agrument
        )


@mock_kms
def test_import_external_key_to_kms(key_material):

    with mock.patch("import_key_material.external_key.KMSExternalKeyImporter") \
            as importer:

        external_key = KMSExternalKey(
            key_id="123456789",
            key_material=key_material
        )
        importer.import_external_key_to_kms(external_key)

        importer.import_external_key_to_kms.assert_called_once_with(
            external_key
        )
