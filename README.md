# json-2-bq

This is meant to be a utility that takes a new-line json file, and generate the bigquery schemas as well as the json file/function needed to use the gcs text to bq template (https://cloud.google.com/dataflow/docs/templates/provided-templates#cloud-storage-text-to-bigquery).

## How to do this - Steps:
* For now, use genson as below, to write out to a schema file (instructions found on genson webpage -- update here?).
`genson $FILENAME(newlinejson) > schemafile.json`

Use  `generate_js_file.py` and `generate_bq_schema_file.py` files with that schemafile by running `python generate_[...].py schemafile.json]`.

### Open issues:
* Data types (does this identify anything other than object and string/text)?
* Turn into a single script -- rather than running schema generator separately.  

### Imports/Dependencies:
* Genson (https://pypi.org/project/genson/)

