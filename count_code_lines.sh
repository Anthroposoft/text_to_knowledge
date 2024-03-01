#!/bin/bash

# Initialize sum variable
sum=0

# Find all python files recursively in the directory
while IFS= read -r -d '' file
do
    # Use grep to count non-comment lines of code
    count=$(grep -v '^\s*#' "$file" | wc -l)

    # Add count to sum
    sum=$((sum + count))
done < <(find src testing examples -type f -name "*.py" -print0)

echo "Total lines of python code: $sum"
