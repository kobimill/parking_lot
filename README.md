# Parking-lot-tool
# Author: Kobi Millshtein
# Date: 2020-07-30

# OCR-API:
Please make sure you have valid key
Go to ocr_api.py and update 'API_KEY' variable.

Sample usage:

# The following command adds record to the DB (in case the image contains valid plate-number)
python parking_lot.py -i <IMAGE-FILE-URL-PATH>

# In order to get the db-records run as following:
python parking_lot.py -i <IMAGE-FILE-URL-PATH> --show
python parking_lot.py --show


# In order to use test-db run as following
python parking_lot.py -i <IMAGE-FILE-URL-PATH> --test 
python parking_lot.py --test --show
