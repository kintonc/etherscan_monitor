import os, requests, json, pickle, time, datetime, playsound, multiprocessing, logging, yaml

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s: %(message)s', 
    handlers=[logging.StreamHandler()],
    datefmt='%H:%M' 
)

def load_config(filepath):
    with open(filepath, 'r') as f:
        conf = yaml.safe_load(f)
    return conf

def play_notification():
    playsound.playsound('notification-positive.wav')

def pull_api(address, api_key):

    r = requests.get('https://api.etherscan.io/api?module=account&action=txlist&address=' + address + '&startblock=0&endblock=99999999&page=1&offset=10&sort=desc&apikey=' + api_key)

    response = json.loads(r.text)
    return response

def save_latest_txn(txn, filename):
    folder_path = os.path.dirname(os.path.abspath(filename))

    if os.path.exists(folder_path) == False:
        os.mkdir(folder_path)

    f = open(filename, 'wb')
    txn['confirmations'] = 0 # set number of confirmations to 0, to enable easy comparison
    pickle.dump(txn, f)
    f.close()

def load_latest_txn(filename):
    if os.path.isfile(filename):
        f = open(filename, 'rb')
        return pickle.load(f)
    else:
        return False

def compare_txns(old, new):
    # Return True if txns are different, else return False 
    if old != new:
        return True
    return False

def check_new_txn(user, api_key):
    readable_name = user['name']
    address = user['address']

    filename = 'txn/' + address

    # Pull latest txn from file
    file_latest_txn = load_latest_txn(filename)

    # Pull latest TXN  from API
    response = pull_api(address, api_key)
    
    if 'result' in response:
        if len(response['result']) >= 1:
            response_latest_txn = response['result'][0]

    # If the API response doesn't have a response['result'][0], then response_latest_txn = False
    if 'response_latest_txn' not in locals():
        response_latest_txn = False

    if response_latest_txn != False:
        # If the response latest txn is different from file latest txn, then sound notification
        response_latest_txn['confirmations'] = 0 # Set confirmations to 0 for easy comparison
        if response_latest_txn != file_latest_txn:
            #play_notification()
            logging.info(f'{readable_name} - new txn - https://etherscan.io/tx/{response_latest_txn["hash"]}')
            save_latest_txn(response_latest_txn, filename)

if __name__ == '__main__':
    # conf means config
    conf = load_config('config.yaml')
    etherscan_api_key = conf['etherscan_api_key']
    users = conf['users']

    while True:
        for key, user in users.items():
            check_new_txn(user, etherscan_api_key)
        print('Last checked: ' + datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S') + ', ' + str(len(users)) + ' users',end = '\r')
        time.sleep(60)

    pool = multiprocessing.Pool(2)
    pool.map(check_new_txn, users) 
    pool.close()   
