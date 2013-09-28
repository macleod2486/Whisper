Whisper
=======

Secure chat program based in Python that uses the RSA public-key/private-key
encryption for sending and recieving messages.  With a decentralized model 
of server-client relations.

This currently is still very alpha but will mature over time.  I will not recommend it for production use, yet.

### Instructions

- Configure your username within the file in the etc/ directory and the port you want your server to listen off of
- Start the file named client.py within the src/ directory
- Then generate your keys, then give the public key file with a .pub extension to your friend/relative/someone you're going to chat with and vice versa.  
- Once complete start the server with the server button then connect to your friends server.

### Current near future goals

- ~~Encrypt the private keys and require a password to unlock~~
- ~~Fingerprint public keys~~
- Make more efficient
- Allow multiple users to connect
- Send files
- Cover more platforms
- Python 3 support

### FAQ


- What does Whisper protect against?

  * When you send messages over the network they are at risk of being captured and read by a third party.  Whisper encrypts these messages using the RSA public key/private key scheme.

- Why RSA?

  * RSA has been proven to be a fairly solid scheme for encryption since the only easy way to decrypt or see the messages is by having the private key.

- Why decentralized?

  * Choke points for web services have been shown to be large targets for adversaries.  When successfully attacked the collateral damagecan be large.  When decentralized it becomes much harder for an adversary to affect large amounts of users.

- What platforms will Whisper work on?

  * Currently Whisper has been tested to work on Linux with Python 2.7.5 but as it develops it will cover more platforms.
