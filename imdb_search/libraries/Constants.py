import os

COMPLETED = "Completed"
ERROR = "Error"


CURRENT_WORKING_DIR = os.getcwd()
INV_IMG_DIR = 'invoices'  # folder to invoice images
OUTPUT_DIR = 'output'  # folder to save excel file

FULL_INV_DIR = os.path.join(CURRENT_WORKING_DIR, INV_IMG_DIR, '')
FULL_OUTPUR_DIR = os.path.join(CURRENT_WORKING_DIR, OUTPUT_DIR, '')
