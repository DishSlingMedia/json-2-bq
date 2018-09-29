import os
import sys
import json

filename = sys.argv[1]

list_of_jsonlines = []

def lowerandunderscore(columnname):
	return columnname.replace(' ', '_').lower() #if type(columnname) == string() else "oh"

#read file
with open(filename, 'r') as f:
    genson_schema = json.load(f)

# Assumes max nested of 1
for column in genson_schema['properties']:
    nested = False
    json_builder = json_builder = "obj.{} = values['{}']".format(lowerandunderscore(column),column)
    col_type =  genson_schema['properties'][column]['type']
    if col_type == 'object':
        nested = True
        if 'properties' in genson_schema['properties'][column].keys():
            for nested_col in genson_schema['properties'][column]['properties']:
            	json_builder = "obj.{} = values['{}']['{}']".format(lowerandunderscore("{}_{}".format(column,nested_col)),column,nested_col)
                list_of_jsonlines.append(json_builder)
    else:
    	json_builder = "obj.{} = values['{}']".format(lowerandunderscore(column),column)

    if nested == False:
        list_of_jsonlines.append(json_builder)

for line in list_of_jsonlines:
	print line
    