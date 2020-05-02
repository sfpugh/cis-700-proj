# query_protocol.py
#   Script for querying database for images, obeying the policies set in ABE 
#   (i.e., only query results/images for which the requestor has sufficient 
#   attributes for will be returned).
#
# Author: Sydney Pugh
# Date: 26 April 2020

from datetime import datetime
import mysql.connector
import subprocess
import pydicom
import sys


## Enforce user to provide key and results directory
if len(sys.argv) != 3:
    print('USAGE:  python query_protocol.py <priv_key> <results_dir>')
    exit(-1)


## Prompt query information from requestor
print('Enter query information...')

try:
    patient_id = input('Patient ID: ')
    patient_id = int( patient_id )
except SyntaxError:
    patient_id = None

try:
    study_id = input('Study ID: ')
    study_id = int( study_id )
except SyntaxError:
    study_id = None

try:
    study_date = input('Study Date (format MM-DD-YYYY): ')
    study_date = datetime.strptime(study_date, '%m-%d-%Y').date()
except SyntaxError:
    study_date = None

try:
    study_time = input('Study Time (format HH:MM:SS): ')
    study_time = datetime.strptime(study_time, '%H:%M:%S').time()
except SyntaxError:
    study_time = None

try:
    image_type = input('Image Type: ')
    image_type = image_type.lower()
except SyntaxError:
    image_type = None


## Build query
query = ("SELECT DICOM_FILE "
        "FROM imaging_db "
        "WHERE (PATIENT_ID = @patient_id OR @patient_id IS NULL) "
        "AND (STUDY_ID = @study_id OR @study_id IS NULL) "
        "AND (STUDY_DATE = @study_date OR @study_date IS NULL) "
        "AND (STUDY_TIME = @study_time OR @study_time IS NULL) "
        "AND (LOWER(IMAGE_TYPE) LIKE @image_type OR @image_type IS NULL)")

data = {
    'patient_id': patient_id,
    'study_id':   study_id,
    'study_date': study_date,
    'study_time': study_time,
    'image_type': image_type
}


## Establish connection to database
cnx = mysql.connector.connect(
  host='localhost',
  user='<insert userID>',
  passwd='<insert pwd>',
  database='mydb',
  auth_plugin='mysql_native_password'
) 
cursor = cnx.cursor()


## Process query results
cursor.execute(query, data)

i = 1
for (dicom_encryption,) in cursor:
    # save all encrypted query results to dir (insecure, but working way)
    fp = open(sys.argv[2] + '/.result' + str(i) + '.cpabe', 'w')
    #fp = open(sys.argv[2] + '/.result.cpabe', 'w')
    fp.write(dicom_encryption)
    fp.close

    # this code section returns 11 (unknown error from cpabe-dec) 
#    cmmd = ['cpabe-dec', './cpabe-keys/pub_key', sys.argv[1], sys.argv[2] + '/.result.cpabe']
#    ret = subprocess.call(cmmd)
#    if ret == 1:    # if cannot be decrypted under given key
#        ret = subprocess.call(['rm', sys.argv[2] + '/.result.cpabe'])
#        if ret != 0:
#            print('rm returned ' + str(ret) + '...')
#        continue
#    elif ret != 0:  # if some other non-zero or non-one return value
#        print('cpabe-dec returned ' + str(ret) + '...')
#        exit(-1)

    i = i + 1


cursor.close()
cnx.close()
