import os
import sys
import json

## NOT NULLABLE -- WHAT IS THIS IN BQ???
filename = sys.argv[1]

bq_schema_json = {}

## HOW TO HANDLE escape characters and/or does single-vs-double quotes matter??

bq_schema = []
required = set()
data_types_map = {
    'string': "STRING"
    ## Int, etc?
    ## DOESN'T INCLUDE OBJECT!
}

def lowerandunderscore(columnname):
	return columnname.replace(' ', '_').lower().replace('/','_') #if type(columnname) == string() else "oh"

#read file
with open(filename, 'r') as f:
    genson_schema = json.load(f)

## ASSUMES REQUIRED ARE ONLY TOP LEVEL
for column in genson_schema['required']:
    required.add(column)

# Assumes max nested of 1
for column in genson_schema['properties']:
    nested = False
    bq_col = {}
    col_type =  genson_schema['properties'][column]['type']
    if col_type in data_types_map.keys():
        bq_col['name'] = lowerandunderscore(column)
        bq_col['type'] = data_types_map[col_type]
        ## FIGURE OUT WHAT TO DO ABOUT NOT NULLABLE!
        bq_col['mode'] = "NULLABLE" if column in required else "NULLABLE" 
    elif col_type == 'object':
        nested = True
        if 'properties' in genson_schema['properties'][column].keys():
            for nested_col in genson_schema['properties'][column]['properties']:
                bq_col = {}
                bq_col['name'] = lowerandunderscore("{}_{}".format(column,nested_col))
                bq_col['type'] = data_types_map[genson_schema['properties'][column]['properties'][nested_col]['type']]
                bq_col['mode'] = "NULLABLE"
                bq_schema.append(bq_col)
    else:
        print("not string or record type")
        print("column is: {}".format(column))
        exit(1)

    if nested == False:
        bq_schema.append(bq_col)

no_dup_elements = set()
for element in bq_schema:
    if lowerandunderscore(element['name']) not in no_dup_elements:
        no_dup_elements.add(lowerandunderscore(element['name']))
    else:
        bq_schema.remove(element)


with open('bq_schema.json', 'w') as f:
    bq_schema_json["BigQuery Schema"] = bq_schema
    f.write(json.dumps(bq_schema_json))




