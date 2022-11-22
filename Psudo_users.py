import pandas as pd
import rsa


names = ['Martha', 'Tim', 'Rob', 'Georgia', 'Sid', 'Johny', 'William', 'Ema', 'Bob', 'Jimmy']
users_data = pd.DataFrame()

# creates dictionary of the users with name as key then publickey and private key as value.
# Creates 10 users and save it in users.csv file
def create_users():
    global users_data
    users = {
        "name":[],
        "publicKey":[],
        "privateKey":[]
    }
    for i in range(len(names)):
        publicKey, privateKey = rsa.newkeys(512)
        users["name"].append(names[i])
        users["publicKey"].append(publicKey)
        users["privateKey"].append(privateKey)

    users_data = pd.DataFrame(users)
    #return users_data
    #print(users_data['publicKey'].iloc[0])

def getPublicKey(name : str):
    for i in range(len(names)):
        if users_data['name'].iloc[i] ==  name:
            return users_data['publicKey'].iloc[i]

def getUserPrivateKey(name : str):
    for i in range(len(names)):
        if users_data['name'].iloc[i] ==  name:
            return users_data['privateKey'].iloc[i]
