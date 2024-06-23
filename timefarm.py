import requests
import random
import time
import threading

def get_new_token(query_id):
    headers_token = {
        'accept': '*/*',
        'accept-language': 'id-ID,id;q=0.9,en-ID;q=0.8,en;q=0.7',
        'content-type': 'text/plain;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://tg-tap-miniapp.laborx.io',
        'priority': 'u=1, i',
        'referer': 'https://tg-tap-miniapp.laborx.io/',
        'sec-ch-ua': '""',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '""',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; Redmi Note 8 Build/TQ3A.230901.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.123 Mobile Safari/537.36'
    }

    data = query_id
    
    response = requests.post('https://tg-bot-tap.laborx.io/api/v1/auth/validate-init', headers=headers_token, data=data)
    response_data = response.json()
    return response_data['token']

def worker(query_id, account_number):
    auth_token = get_new_token(query_id)

    while True:
        headers = {
            'accept': '*/*',
            'accept-language': 'id-ID,id;q=0.9,en-ID;q=0.8,en;q=0.7,en-US;q=0.6',
            'authorization': 'Bearer '+auth_token,
            'dnt': '1',
            'origin': 'https://tg-tap-miniapp.laborx.io',
            'priority': 'u=1, i',
            'referer': 'https://tg-tap-miniapp.laborx.io/',
            'sec-ch-ua': '""',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '""',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 13; Redmi Note 8 Build/TQ3A.230901.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.123 Mobile Safari/537.36',
        }
        
        json_data = {}
        
        try:
            response = requests.post('https://tg-bot-tap.laborx.io/api/v1/farming/finish', headers=headers, json=json_data)
            response_data = response.json()
            try:
                restart_mining = requests.post('https://tg-bot-tap.laborx.io/api/v1/farming/start', headers=headers, json=json_data)
                coins = response_data['balance']
                print(f'Account {account_number}: Your Coins {coins}')
                time.sleep(5)
                rand_delay = random.randint(180, 200)
                delay = rand_delay * 60
                for i in range(delay, 0, -1):
                    minutes, seconds = divmod(i, 60)
                    hours, minutes = divmod(minutes, 60)
                    print(f"Account {account_number}: Time remaining: {hours:02d}:{minutes:02d}:{seconds:02d}", end='\r')
                    time.sleep(1)
                print()  # New line for each account's delay countdown
            except:
                message = response_data['error']['message']
                if 'Too early to finish farming' in message:
                    print(f'Account {account_number}: {message}')
                    rand_delay = random.randint(180, 200)
                    delay = rand_delay * 60
                    for i in range(delay, 0, -1):
                        minutes, seconds = divmod(i, 60)
                        hours, minutes = divmod(minutes, 60)
                        print(f"Account {account_number}: Time remaining: {hours:02d}:{minutes:02d}:{seconds:02d}", end='\r')
                        time.sleep(1)
                    print()  # New line for each account's delay countdown
        
        except Exception as e:
            print(f'Account {account_number}: An error occurred:', e)
            try:
                message = response_data['error']['message']
                if 'Forbidden' in message:
                    print(f'Account {account_number}: {message} Regenerate Token')
                    auth_token = get_new_token(query_id)
            except Exception as e:
                print(f'Account {account_number}: Retrying due to error:', e)
                time.sleep(2)

def main():
    query_id_file = input('Masukan File Query Id (queryid.txt): ')
    with open(query_id_file, "r") as file:
        query_ids = [line.strip() for line in file if line.strip()]
    
    threads = []

    for index, query_id in enumerate(query_ids, start=1):
        thread = threading.Thread(target=worker, args=(query_id, index))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
