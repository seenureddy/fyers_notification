#!/bin/bash

# curl -H "Content-Type: application/json" -X POST 'http://localhost:5000/qk/email' -d "@data.json"
# curl -X POST http://localhost:5000/qk/email -H 'content-type: application/json' -d "@data.json"

curl -s "http://localhost:5000" -F file=@./myfile.csv -X POST -H 'enctype:multipart/form-data ; Content-Type:multipart/form-data'