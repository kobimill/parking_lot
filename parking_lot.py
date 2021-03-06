"""
This is a service which gets an image of an Israeli license plate and returns a
decision whether the vehicle may enter a parking lot or not.
"""
import re
import argparse
import ocr_api
import parking_lot_db

PRIVATE_VEHICLE_TYPE = 'private'
GAS_OPERATOR_VEHICLE_TYPE = 'gas_operator'
MILITARY_LAW_VEHICLE_TYPE = 'military_law_enforcement'
PUBLIC_TRANSPORTATION_VEHICLE_TYPE = 'public_transportation'

PUBLIC_TRANSPORTATION_LAST_2_DIGITS = ['25', '26']
PROHIBITED_LAST_2_DIGITS = ['85', '86', '87', '88', '89', '00']


def get_sum_digits(str_num):
    num = 0
    for i in str_num:
        num += int(i)
    return num


def prohibited_vehicle(plate_number, last_2_digits):
    '''
    7 digits numbers which their two last digits are 85/86/87/88/89/00, are
    also prohibited.
    '''
    num_digits = len(plate_number)
    return num_digits == 7 and last_2_digits in PROHIBITED_LAST_2_DIGITS


def check_plate_number(plate_number, test_mode=False):
    car_type = PRIVATE_VEHICLE_TYPE
    prohibited = True

    last_two_chars = plate_number[-2:]

    if not plate_number.isdigit():  # Contains alphabet letters
        '''
        Military and law enforcement vehicles are also prohibited (these can be
        identified by an inclusion of an English alphabet letter within the plate number)
        '''
        car_type = MILITARY_LAW_VEHICLE_TYPE

    elif last_two_chars in PUBLIC_TRANSPORTATION_LAST_2_DIGITS:
        '''
        Public transportation vehicles cannot enter the parking lot (their license
        plates always end with 25 or 26).
        '''
        car_type = PUBLIC_TRANSPORTATION_VEHICLE_TYPE

    elif len(plate_number) in [7, 8] and get_sum_digits(plate_number) % 7 == 0:
        '''
        Seven or eight digits license plate numbers which their digits sum divided
        by 7, are suspected as operated by gas, and therefore also prohibited.
        '''
        car_type = GAS_OPERATOR_VEHICLE_TYPE

    elif not prohibited_vehicle(plate_number, last_two_chars):
        prohibited = False

    cars_db = parking_lot_db.DB(test=test_mode)
    cars_db.add_row(plate_number, car_type, int(prohibited))

    return prohibited, car_type


def remove_non_alphanum_from_text(text):
    return re.sub(r'\W+', '', text)


def process_licence_plate(car_license_plate_image, test_mode=False):
    image_results = ocr_api.ocr_space(car_license_plate_image)
    if not image_results:
        raise Exception("Invalid file/URL given!")

    is_error_processing = image_results['IsErroredOnProcessing']
    if is_error_processing:
        error = image_results['ErrorMessage'][0]
        raise Exception(error)

    parsed_results = image_results['ParsedResults'][0]
    parsed_text = parsed_results['ParsedText']
    parsed_exit_code = parsed_results['FileParseExitCode']
    parsed_error = parsed_results['ErrorMessage']

    if parsed_exit_code > 1:
        raise Exception("Failed parsing image! Error: '{}'".format(parsed_error))

    # Converting parsed text to list
    parsed_text_lines_list = [remove_non_alphanum_from_text(text_line) for text_line
                              in map(str.strip, parsed_text.split('\n')) if text_line]

    if not parsed_text_lines_list:
        raise Exception("Warning! not found text in given image!")

    # Extract plate-number from text:
    plate_number = None
    for i in parsed_text_lines_list:
        if i.isalpha():  # Contains letters chars only
            continue

        # Valid israeli license-plate
        if len(i) < 5 or len(i) > 8:
            continue

        if i.isalnum() or i.isdigit():
            plate_number = i
            break

    if not plate_number:
        raise Exception("Not found valid plate-number!")

    return check_plate_number(plate_number, test_mode)


def show_db_records_info(test_mode=False):
    cars_db = parking_lot_db.DB(test_mode)
    records = cars_db.get_records()
    for i in records:
        print(i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", action='store', help="Image file/url")
    parser.add_argument("--show", action='store_true', help="Show records info")
    parser.add_argument("--test", action='store_true', help=argparse.SUPPRESS)

    args = parser.parse_args()
    if args.image:
        try:
            prohibited, car_type = process_licence_plate(args.image, args.test)
            print(f"Car-Type: {car_type}, Prohibited: {prohibited}")
        except Exception as e:
            print(f"Failed processing image '{args.image}', Exception: {e}")
            exit(1)

    if args.show:
        show_db_records_info(args.test)
