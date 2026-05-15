## check my blog - https://medium.com/@sharmarajat1984/salesforce-pub-sub-api-grpc-via-postman-and-decode-the-payload-823063be6cd7

### Install the Python on your machine if you don't have


Step 1 — Install Python and Avro

bash
python3 --version
If not installed, install using Homebrew:

brew install python

pip3 install avro-python3

### Create Avro file to Decode the gRPC schema
In this repo decode_avro.py is the schema payload for my PE WOM_Workorder__e.avsc

On Terminal 
python3 decode_avro.py "Replace with your Payload"

#### your payload should be looked like - gMrQ6vxlJDAwNWJtMDAwMDBFcE1zckFBRgJCV2VsY29tZSB0byBSYWphdCBCbG9nIG9uIE1lZGl1bSAx 

### Decode the payload Replay_id
In this repo the file is decode_replay_id.py

On Terminal 
python3 decode_replay_id.py AAAAAArvySIAAA==
