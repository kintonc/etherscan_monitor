import os, requests, json, pickle, time, datetime, playsound, logging, yaml, threading

#####
# Parameters
CHECK_FREQUENCY_SECONDS = 60

#####

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
    playsound.playsound('notif.mp3')

def pull_api(address, api_key, network):

    if network == 'eth':
        r = requests.get('https://api.etherscan.io/api?module=account&action=txlist&address=' + address + '&startblock=0&endblock=99999999&page=1&offset=10&sort=desc&apikey=' + api_key)
    elif network == 'avax':
        r = requests.get('https://api.snowtrace.io/api?module=account&action=txlist&address=' + address + '&startblock=1&endblock=99999999&page=1&offset=10&sort=desc&apikey=' + api_key)

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

def check_new_txn(user, api_keys_all_networks, notif_played_count):
    readable_name = user['name']
    address = user['address']
    networks = user['network']

    for network in networks:
        filename = 'txn/' + address + '_' + network

        # Pull latest txn from file
        file_latest_txn = load_latest_txn(filename)

        api_key = api_keys_all_networks[network]
        # Pull latest TXN  from API
        response = pull_api(address, api_key, network)
        
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
                if notif_played_count == 0:
                    # start_time_notif = datetime.datetime.now() // FOR PERFORMANCE DEBUGGING
                    thr = threading.Thread(target=play_notification,args=(),kwargs={})
                    thr.start()
                    # we don't want to play notif sound more than once, every time data is pulled from API even for muiltiple accounts
                    # so we set notif_palyed_count = 1
                    notif_played_count = 1 
                    # end_time_notif = datetime.datetime.now() // FOR PERFORMANCE DEBUGGING
                    # print((end_time_notif-start_time_notif).total_seconds()) // FOR PERFORMANCE DEBUGGING
                    
                if network == 'eth':
                    txn_url = f'https://etherscan.io/tx/{response_latest_txn["hash"]}'
                elif network == 'avax':
                    txn_url = f'https://snowtrace.io/tx/{response_latest_txn["hash"]}'

                logging.info(f'{readable_name}_{network} - new txn - {txn_url}')
                save_latest_txn(response_latest_txn, filename)
    
    return notif_played_count

if __name__ == '__main__':
    # conf means config
    conf = load_config('config.yaml')
    api_key = {}
    api_key['eth'] = conf['etherscan_api_key']
    api_key['avax'] = conf['snowtrace_api_key']
    users = conf['users']

    while True:
        start_time = datetime.datetime.now()
        notif_played_count = 0

        for key, user in users.items():
            notif_played_count = check_new_txn(user, api_key, notif_played_count)
        
        end_time = datetime.datetime.now()
        time_elapsed = (end_time - start_time).total_seconds() 

        print('Last checked: ' + datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S') + ', ' + str(len(users)) + ' users, ' + str(time_elapsed) + ' s',end = '\r')
        time.sleep(CHECK_FREQUENCY_SECONDS)

    pool = multiprocessing.Pool(2)
    pool.map(check_new_txn, users) 
    pool.close()   
