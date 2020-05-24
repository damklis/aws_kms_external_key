
set -xe

pip install -r import_key_material/requirements.txt

key_id=$1
algorithm=$2

python -m import_key_material \
--key_id $key_id \
--algorithm $algorithm