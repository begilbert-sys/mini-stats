import atexit
import datetime
import json 
import requests
import time

from collections import Counter
from nyt_s_token import NYT_S_TOKEN

# arbitrary number of seconds to wait between each request 
# change at your own risk
RATELIMIT = 5
FIRST_MINI_DATE = datetime.date(2014, 8, 21)

today = datetime.datetime.now().date()

with open('data.json') as file:
    data = json.load(file)
    LAST_RUN_DATE = datetime.datetime.strptime(data['last_run'], "%Y-%m-%d").date()
    word_count = Counter(data['word_count'])

def get_mini_words(date: datetime.date) -> list:
    '''
    Given a date, return every word from the mini of that date 
    '''
    if not FIRST_MINI_DATE <= date <= today:
        raise ValueError(f"{date} is not a valid mini date")
    
    headers = {"Cookie": f"NYT-S={NYT_S_TOKEN}"}
    response = requests.get(f"https://www.nytimes.com/svc/crosswords/v6/puzzle/mini/{date}.json", headers=headers)
    if response.status_code != 200:
        raise requests.HTTPError(f"{date} failed with status code {response.status_code}")
    
    response_json = json.loads(response.text)
    board_json = response_json['body'][0]['cells']
    
    clues = {}
    for cell in board_json:
        if not cell: # blacked-out cells are empty
            continue
        letter = cell['answer']
        for clue in cell['clues']:
            if clue in clues:
                clues[clue] += letter
            else:
                clues[clue] = letter
    return list(clues.values())

word_frequency = Counter()
date_range = (today - LAST_RUN_DATE).days
current_date = LAST_RUN_DATE

#ensure data is always saved before closing
@atexit.register
def save_and_close():
    with open('data.json', 'w') as file:
        contents = {'last_run': str(current_date), 'word_count': word_count}
        json.dump(contents, file)
    print("contents saved")

for day in range(1, date_range):
    time.sleep(RATELIMIT)
    current_date = LAST_RUN_DATE + datetime.timedelta(days = day)
    word_list = get_mini_words(current_date)
    print(current_date, word_list)
    for word in word_list:
        word_count[word] += 1