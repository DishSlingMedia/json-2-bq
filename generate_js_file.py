import os
import sys
import json

## NOT NULLABLE -- WHAT IS THIS IN BQ???
filename = sys.argv[1]

js_start = [
"function transform(line) {",
"var values = JSON.parse(line);",
"var obj = new Object();"
]

js_end = [
"var jsonString = JSON.stringify(obj);",
"return jsonString;",
"}"
]

list_of_jsonlines = []

def lowerandunderscore(columnname):
    return columnname.replace(' ', '_').lower().replace('/',' ') #if type(columnname) == string() else "oh"

#read file
with open(filename, 'r') as f:
    genson_schema = json.load(f)

# Assumes max nested of 1
for column in genson_schema['properties']:
    nested = False
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


full_json_file = js_start + list_of_jsonlines + js_end

with open('output.js', 'w') as f:
    for line in full_json_file:
        f.write("{}\n".format(line.strip()))
