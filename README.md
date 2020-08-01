# === Parking-lot tool ==

# OCR-API:
In order to use the ocr_api - please make sure you have valid 'API_KEY'

Sample usage:

# The following command adds record to the DB 
#(in case the image contains valid plate-number)

python parking_lot.py -i <IMAGE-FILE-URL-PATH>

# In order to get the db-records run as following:
python parking_lot.py -i <IMAGE-FILE-URL-PATH> --show
python parking_lot.py --show


# In order to use test-db run as following
python parking_lot.py -i <IMAGE-FILE-URL-PATH> --test 
python parking_lot.py --test --show
