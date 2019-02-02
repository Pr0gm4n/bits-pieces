#!/bin/bash

find . -name ".git" -type d -exec echo "" \; -execdir pwd \; -execdir git pull \;
