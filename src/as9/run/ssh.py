import paramiko
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the SSH client
client = paramiko.SSHClient()

# Add the public key required for authentication
client.load_system_host_keys()

# Automatically add the server's host key (not previously known)
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the server
try:
    #private_key_path = "C:/programs/keys/myriad/id_rsa"
    #mykey = paramiko.RSAKey.from_private_key_file("C:/programs/keys/myriad/id_rsa")
    mykey = paramiko.RSAKey.from_private_key_file("C:/Users/lukel/.ssh/id_rsa")

    client.connect('testv-phi-07.aws.counsyl.com', username='llast', disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']}, pkey=mykey)
    print("Connected successfully!")
except Exception as e:
    print("Failed to connect, reason:", e)

# Close the connection when you're done with it.
client.close()
