# Base code
'''
# generate public and private keys with
# rsa.newkeys method,this method accepts
# key length as its parameter
# key length should be atleast 16

publicKey, privateKey = rsa.newkeys(512)
 
# this is the string that we will be encrypting
message = "hello there..."
 
# rsa.encrypt method is used to encrypt
# string with public key string should be
# encode to byte string before encryption
# with encode method
encMessage = rsa.encrypt(message.encode(), publicKey)
 
#print("Public key: ",hex( int( ((str(publicKey).split("(")[1]).split(",")[0]) ) ) )
print(type(publicKey))
print("original string: ", message)
print("encrypted string: ", encMessage)
 
# the encrypted message can be decrypted
# with ras.decrypt method and private key
# decrypt method returns encoded byte string,
# use decode method to convert it to string
# public key cannot be used for decryption
decMessage = rsa.decrypt(encMessage, privateKey).decode()
 
print("decrypted string: ", decMessage)
'''


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import rsa
import time
import os
from pprint import pprint
import pandas as pd
import Psudo_users as p_users
p_users.create_users()


names = p_users.names
storage = pd.DataFrame()
currentUser = 'Martha'

contacts = {}
for i in range(len(names)):
    # creates the contact dictionary which will be public with user_name as key and public key as value.
    contacts[names[i]] = p_users.getPublicKey(names[i])


# creates a storage data-base and initialise with no new messages in inbox and in outbox.
def create_data_base():
    global databaseOfAllUsers
    databaseOfAllUsers={}
    data = {
        'Contact' : [],
        'inbox' : [],
        'outbox' : []
    }
    for user in names:
        databaseOfAllUsers[user] = ''
        for name in contacts:
            if user!=name:
                data['Contact'].append(name)
                data['inbox'].append('')
                data['outbox'].append('')
        databaseOfAllUsers[user] = data
        data = {'Contact' : [], 'inbox' : [], 'outbox' : []}

    databaseOfAllUsers

create_data_base()


def send_message(user, recipient, message):
    try:
        # Accesses public key of the recipient from the contacts dictinary using recipient name
        publicKey1 = contacts[recipient]
        publicKey2 = contacts[user]

        # Encrypt the message with the public key of the recipient
        encMessage_sent = rsa.encrypt(message.encode(), publicKey1)
        encMessage_copy = rsa.encrypt(message.encode(), publicKey2)

        # Store the encrypted data in recipinets inbox
        for i in range(len(databaseOfAllUsers[recipient]['Contact'])):
            if databaseOfAllUsers[recipient]['Contact'][i] == user:
                break
        databaseOfAllUsers[recipient]['inbox'][i] = encMessage_sent

        # Store the encrypted data in users outbox
        for i in range(len(databaseOfAllUsers[user]['Contact'])):
            if databaseOfAllUsers[user]['Contact'][i] == recipient:
                break
        databaseOfAllUsers[user]['outbox'][i] = encMessage_copy

        return True
    except Exception as e:
        print(e)
        return False


def read_message(user, userPrivateKey, chatFrom):
    try:
        # Access the inbox chat encrypted message from storage file
        for i in range(len(databaseOfAllUsers[user]['Contact'])):
            if databaseOfAllUsers[user]['Contact'][i] == chatFrom:
                break
        encMessage = databaseOfAllUsers[user]['inbox'][i]

        # Decrypt the message usong my private key
        decMessage = rsa.decrypt(encMessage, userPrivateKey).decode()
    except Exception as e:
        print(e)
        decMessage = ''
    return(decMessage)


def driveMenu():
    global currentUser
    print("Current user: ",currentUser)
    print('''
    +=============================+
    |   1) change user            |
    |   2) send message           |
    |   3) read from inbox        |
    |   4) state of database      |
    +=============================+
    ''')
    option = eval(input("Select an option: "))
    if option == 1:
        print(names)
        prevUser = currentUser
        currentUser = input("Enter a user name from the above list: ")
        print("Current user changed from",prevUser,"to",currentUser)
        time.sleep(2)
        os.system('cls')
    elif option == 2:
        os.system('cls')
        print(databaseOfAllUsers[currentUser]['Contact'])
        recipient = input("Enter a recipient from contacts to sent message to: ")
        message = input("Enter the message to be sent: ")
        send_message(currentUser, recipient, message)
        os.system('cls')
        print("Message sent successfully")
        time.sleep(2)
        os.system('cls')
    elif option == 3:
        os.system('cls')
        print(databaseOfAllUsers[currentUser]['Contact'])
        chatName = input("Enter a inbox chat name from the above contacts: ")
        message = read_message(currentUser, p_users.getUserPrivateKey(currentUser), chatName)
        os.system('cls')
        if message == '':
            print('Inbox is empty!')
        else:
            print("Recent message from",chatName,": ",message)
    elif option == 4:
        os.system('cls')
        pprint(databaseOfAllUsers)
    else:
        os.system('cls')
        print("wrong option")
        time.sleep(2)
        os.system('cls')

while True:
    driveMenu()
