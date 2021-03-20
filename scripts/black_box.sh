#!/bin/bash

# curl -H "Content-Type: application/json" -X POST 'http://localhost:5000/fys/email' -d @data.json
# curl -X POST http://localhost:5000/fys/email -H 'content-type: application/json' -d "@data.json"

# curl -s "http://0.0.0.0:5000/fys/email" -d @./data.json -X POST -H 'Content-Type: application/json'

curl -s "http://0.0.0.0:5000/fys/csv_upload" -F csv_file=@./csv_file_data.csv -X POST -H 'enctype:multipart/form-data ; Content-Type:multipart/form-data'
