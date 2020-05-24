import argparse
from Crypto.Random import get_random_bytes
from import_key_material.external_key import (
    KMSExternalKey, KMSExternalKeyImporter
)


def generate_aes256_key():
    return get_random_bytes(32)


def parse_arguments(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-id", "--key_id", metavar="", help="KMS key identification"
    )
    parser.add_argument(
        "-alg", "--algorithm", metavar="", help="Encryption algorithm"
    )
    return parser.parse_args()

def main():
    args = parse_arguments("Import key material into KMS")
    key_material = generate_aes256_key()
    external_key = KMSExternalKey(
        args.key_id,
        key_material,
        args.algorithm
    )

    importer = KMSExternalKeyImporter()
    response = importer.import_external_key_to_kms(
        kms_external_key=external_key
    )
    print(f"Imported key material: Key_id => {args.key_id}: {response}")


if __name__ == "__main__":
    main()
