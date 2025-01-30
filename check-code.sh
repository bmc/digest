#!/usr/bin/env bash
#
# Run Python checkers and formatters.

echo "Checking types ..."
pyright || exit 1

echo "Running pylint ..."
pylint digest || exit 1

echo "Sorting imports in $i"
isort digest

echo "Formatting $i with black"
black digest
