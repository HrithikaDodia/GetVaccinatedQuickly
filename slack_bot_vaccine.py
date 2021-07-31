import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from covid_vaccine_info import get_vaccine_details 


def show_message_slack(result):
    blk = []

    star_emoji = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":star: :star: :star: :star: :star: :star: :star: :star: :star: :star: :star: :star: :star: :star:"
            }
    }

    blk.append(star_emoji)

    for r in result:
        # print(r)
        text_message = ''
        for key in r:
            val = key.replace('_', ' ')
            text_message += f'*{val.upper()}:* '
            if key == 'slots':
                l = r[key]
                for i in range(len(l) - 1):
                    text_message += f'{l[i]} | '
                text_message += f'{l[-1]}\n'
            
            elif key == 'vaccine':
                d = r[key]
                text_message += '\n'
                for key in d:
                    text_message += f'{key}: {d[key]}\n'
            else:
                text_message += f'{r[key]}\n'

        text_message += '-------------------------------------------------\n'
        start_text = {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text':(
                    text_message
                )
            }
        }
        blk.append(start_text)
    
    blk.append(star_emoji)

    client.chat_postMessage(channel='#get-vaccine-quickly', blocks=blk)

if __name__ == '__main__':
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
    district = os.environ['DISTRICT_CODE']
    area = os.environ['AREA']
    min_age_limit = os.environ['MIN_AGE_LIMIT']

    result = get_vaccine_details(district, area, min_age_limit)
    show_message_slack(result)