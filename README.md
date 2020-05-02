# cis-700-proj
## Attribute-Based Encryption for Secure Medical Image Management

### Repository Details
setup.sh - bash script to generate public key and master key  
keygen.sh - bash script to generate user private keys   
store.sh - bash script for imaging modalities to send DCM images to the database  
image_store_protocol.py - supplementary code for store.sh
query.sh - bash script for medical personnel to query the database for images  
query_protocol.py - supplementary code for query.sh

### Prerequisites
This implementation depends on the following toolkits, libraries, and modules:
* cpabe toolkit (http://acsc.cs.utexas.edu/cpabe/)
* libbswabe (http://acsc.cs.utexas.edu/cpabe/)
* PBC library (https://crypto.stanford.edu/pbc/)
* openssl (https://www.openssl.org)
* glib (https://www.gtk.org)
* Yubico Python module (https://developers.yubico.com/python-yubico/)
* MySQL Connector Python module
* Pydicom Python modul
