import os
import sys
import json

## NOT NULLABLE -- WHAT IS THIS IN BQ???

filename = sys.argv[1]

bq_schema = []
required = set()

def lowerandunderscore(columnname):
	return columnname.replace(' ', '_').lower() #if type(columnname) == string() else "WTF"

#read file
with open(filename, 'r') as f:
    for line in f:
        genson_schema = json.load(line.strip())

## ASSUMES REQUIRED ARE ONLY TOP LEVEL
for column in genson_schema['required']:
    required.add(column)

# Assumes max nested of 1
for column in genson_schema['properties']:
    bq_col = {}
    bq_col['mode'] = "NULLABLE"

    col_type = genson_schema['type']
    if col_type == 'string':
        bq_col['type'] = "STRING"
        bq_col['name'] = lowerandunderscore(column)
    elif col_type == 'object':
        # RECURSION WOULD COME IN HERE
        for nested_col in genson_schema['properties'][column]['properties']
            bq_col_name = lowerandunderscore("{}_{}".format(column,nested_col))
            nested_col_type = genson_schema['properties'][column]['properties'][nested_col]['type']
                if nested_col_type = 'string':
                	bq_col['type'] = "STRING"
                else: 
                    print("not string or record type")
                    print("column is: {}".format(column))
                    exit(1)
    else:
        print("not string or record type")
        print("column is: {}".format(column))
        exit(1)

    bq_schema.append(bq_col)

    
print(bq_schema)



