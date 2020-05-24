variable "tags" {
    type    = map
    default = {}
}

variable "region" {
    type    = string
    default = "us-east-1"
}

variable "key_alias" {
    type    = string
    default = "alias/external_key3"
}

variable "policy_name" {
    type    = string
    default = "external_key_policy"
}

variable "algorithm" {
    type    = string
    default = "RSAES_OAEP_SHA_256"
}

variable "python_module" {
    type    = string
    default = "import_key_material"
}