#!/bin/bash

# Check args
if [ $# -ne 1 ]; then
    echo "Usage: $0 <absolute_path_to_file>"
    exit 1
fi

# Key's variables
first_key="S1.cpp"
second_key="S2.cpp"
found_first_key=false

# path to check file
absolute_path_to_file=$1

# checking file
return_flag=0
while IFS= read -r line; do
    if [[ "$line" == *"$first_key"* ]]; then
        found_first_key=true
    elif [[ "$line" == *"$second_key"* && "$found_first_key" == true ]]; then
        return_flag=1
        break
    fi
done < "$absolute_path_to_file"

# delete temporary file
cleanup=true
if [ "$cleanup" = true ]; then
    rm -f "$absolute_path_to_file"
fi

# return code
exit $return_flag
