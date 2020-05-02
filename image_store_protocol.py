# image_store_protocol.py
#   Script for storing DICOM images in the database encrypted under specific attributes.
#
# Author: Sydney Pugh
# Date: 26 April 2020

import mysql.connector
import subprocess
import pydicom
import sys

POLICY_FMT = ("{hosp} and "
              "(sysadmin or "
              "( (imaging_technician and {im_spec}) or "
              "( {dept} and "
              "( attending_physician or "
              "( nurse and {n_lvl} ) ) ) ) )"
             )


## Enforce modality to provide DICOM file
if len(sys.argv) != 2:
    print('USAGE:  python image_store_protocol.py <dicom_file>')
    exit(-1)


## Request policy parameters from modality
hospital = raw_input('Enter hospital: ')
hospital = hospital.strip('\n')

image_spec = raw_input('Enter imaging specialty: ')
image_spec = image_spec.strip('\n')

department = raw_input('Enter department: ')
department = department.strip('\n')

nurse_lvl = raw_input('Enter nurse level: ')
nurse_lvl = nurse_lvl.strip('\n')


## Encrypt DICOM file under ABE
# encryption cmmd format: cpabe-enc <args> <pub_key> <file_to_encrypt> <policy> 
policy = POLICY_FMT.format(hosp=hospital, im_spec=image_spec, dept=department, n_lvl=nurse_lvl)
cmmd = ['cpabe-enc', '-k', '-o', '.temp-enc.cpabe', './cpabe-keys/pub_key', sys.argv[1], policy]

ret = subprocess.call(cmmd)
if ret != 0:
    print('cpabe-enc returned ' + str(ret) + ' ...')
    exit(-1)

fp = open('.temp-enc.cpabe', 'r')
encrypted_data = fp.read()
fp.close()


## Extract parameters from DICOM file
dr = pydicom.dcmread(sys.argv[1])


## Store encrypted DICOM file in database
cnx = mysql.connector.connect(
  host='localhost',
  user='<insert userID>',
  passwd='<insert pwd>',
  database='mydb',
  auth_plugin='mysql_native_password'
)
cursor = cnx.cursor()

query = ("INSERT INTO imaging_db "
        "(PATIENT_ID,STUDY_ID,STUDY_DATE,STUDY_TIME,IMAGE_TYPE,DICOM_FILE) "
        "VALUES (%s,%s,%s,%s,%s,%s)")

data = (dr.PatientID, dr.StudyID, dr.StudyDate, dr.StudyTime, dr.Modality, encrypted_data)

cursor.execute(query, data)
cnx.commit()

cursor.close()
cnx.close()


## Remove encryption file
subprocess.call(['rm','.temp-enc.cpabe'])
