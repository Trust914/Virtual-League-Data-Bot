import json
import smtplib
import os

import requests
import pprint as pp

"this is just a test"
SHEET_AUTH = (os.environ.get("LEAGUE_SHEETY_USER_NAME"), os.environ.get("LEAGUE_SHEETY_PASSWORD"))
LEAGUE_SHEET_ENDPOINT = os.environ.get("LEAGUE_SHEETY_ENDPOINT")
SHEET_LINK = os.environ.get("LEAGUE_SHEET_LINK")
FROM_EMAIL = os.environ.get("LEAGUE_FROM_EMAIL")
FROM_EMAIL_PASS = os.environ.get("LEAGUE_FROM_EMAIL_PASS")

print(SHEET_LINK)
print(FROM_EMAIL)
print(FROM_EMAIL_PASS)


def check_score_pattern(results_dict: dict):
    teams = []

    for key, value in results_dict.items():
        if key not in ["leagueId", "timeStamp"]:
            club_score = value.split("-")

            def add_team():
                print(f'Pattern found in {key}')
                teams.append(key)

            if len(club_score) >= 15:
                if "D" in club_score:
                    draw_pos = club_score.index("D")
                    print(draw_pos)

                    def find_diff():
                        next_draw_index = club_score.index("D", draw_pos + 1)
                        print(next_draw_index)
                        diff = next_draw_index - draw_pos
                        print(f"Diff btw {next_draw_index} and {draw_pos} is {diff}")
                        return diff, next_draw_index

                    no_draw, next_draw_pos = find_diff()
                    while True:
                        if no_draw < 15 and "D" in club_score[next_draw_pos + 1:]:
                            draw_pos = next_draw_pos
                        elif no_draw >= 15:
                            add_team()
                            break
                        else:
                            break
                        no_draw, next_draw_pos = find_diff()
                else:
                    add_team()
    print(teams)
    teams_string = ",".join(teams).upper()
    print(teams_string)

    message = f"Hey CJ,\n\nHurry up a NO DRAW pattern has been found in the scores of the following team(s):\n{teams_string}.\n\n" \
              f"Click the l google sheet link to check {SHEET_LINK}."

    if teams_string != "":
        send_email(msg=message, to_email="trustezzy@gmail.com")


def send_email(msg, to_email):
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=FROM_EMAIL, password=FROM_EMAIL_PASS)
        connection.sendmail(from_addr=FROM_EMAIL, to_addrs=to_email,

                            msg=f"Subject:Pattern Found!\n\n{msg}".encode("utf-8"))


dict_e = {'ars': 'D-W-L-D-D-L-W-W-L-L-W-W-W-L-W-L-W-W-D-W-L-W-W-W-D-W-W-D-L-L-L-L-W-W-D-W-D-L',
          'asv': 'W-D-W-W-L-L-L-D-L-D-D-D-L-W-D-L-L-W-L-L-L-W-D-W-D-L-W-D-W-W-L-W-W-D-W-W-L-W',
          'bou': 'W-W-D-L-L-L-L-L-L-L-W-L-W-L-W-L-L-W-W-L-W-L-D-D-D-L-L-L-W-L-L-L-D-L-L-L-D-L',
          'bri': 'L-L-L-W-L-W-L-W-D-W-D-L-L-D-D-W-W-W-W-L-W-W-W-W-D-L-W-W-D-D-L-D-L-L-L-L-W-W',
          'brn': 'W-L-W-L-L-D-L-D-D-L-L-L-W-W-D-D-D-L-D-L-W-L-D-W-D-L-L-L-D-L-W-D-L-L-D-L-D-W',
          'che': 'L-D-W-W-L-W-L-L-L-L-D-W-D-W-D-W-D-W-D-W-D-W-W-W-D-L-D-W-D-W-D-D-L-D-W-W-L-W',
          'cry': 'L-W-L-L-W-L-W-L-L-D-L-L-W-W-D-W-L-D-W-W-W-L-W-L-L-W-W-L-L-D-D-D-L-W-L-D-L-W',
          'eve': 'D-D-D-L-L-W-W-L-W-L-L-L-L-L-W-L-W-L-L-D-D-L-L-L-D-L-D-D-W-L-D-W-W-D-W-W-W-W',
          'for': 'D-L-D-D-W-W-W-D-D-D-W-D-W-L-D-L-L-L-D-D-L-D-W-D-D-W-W-L-L-L-L-L-L-L-W-L-D-L',
          'ful': 'D-L-L-L-W-W-L-L-D-W-W-D-D-W-D-L-D-L-W-L-L-L-D-D-L-L-L-W-L-D-L-L-D-W-L-L-L-D',
          'lee': 'L-L-L-W-L-L-L-W-L-D-L-W-L-W-L-W-W-D-D-L-L-L-D-D-D-L-D-L-D-W-W-D-L-D-L-D-L-W',
          'lei': 'D-L-W-W-W-W-D-D-W-D-D-W-W-L-D-L-D-L-L-L-W-L-D-W-W-W-W-W-W-L-L-D-W-L-W-W-W-D',
          'liv': 'W-D-W-D-D-W-W-W-W-W-L-W-L-L-D-L-D-D-L-W-W-W-L-W-D-W-D-W-W-W-W-W-W-D-W-L-W-L',
          'mnc': 'W-W-W-W-D-W-W-L-W-W-W-W-L-W-W-W-W-L-W-W-L-D-D-L-D-W-W-W-W-W-D-D-W-W-W-W-W-W',
          'mnu': 'D-L-L-D-W-L-W-W-W-W-W-W-D-D-L-W-D-D-L-W-D-D-W-L-W-W-L-D-D-W-D-W-L-W-L-L-L-L',
          'nwc': 'W-W-D-D-W-W-W-D-W-W-W-D-D-D-L-W-D-W-L-W-W-W-L-L-D-W-L-W-W-L-W-W-W-L-D-W-L-L',
          'sou': 'L-L-D-L-L-L-D-W-D-L-D-D-D-L-L-D-L-D-D-L-L-D-L-L-D-L-W-D-L-L-W-L-L-L-D-L-W-L',
          'tot': 'L-W-W-L-D-D-L-W-D-L-L-D-D-W-D-W-L-D-W-W-W-D-D-L-D-W-L-D-L-W-W-D-D-W-L-D-W-W',
          'whu': 'D-W-D-W-W-L-W-D-W-D-D-L-D-L-D-W-D-D-L-L-L-W-L-W-D-W-L-L-D-D-W-W-D-D-L-W-W-L',
          'wol': 'D-W-L-D-W-L-L-L-L-W-L-L-D-D-D-L-W-D-W-W-D-D-L-L-D-L-L-L-L-W-D-L-W-W-W-D-L-L',
          'leagueId': 'League 5687', 'timeStamp': '2023-05-09 00:19:49'}
print(dict_e)


# check_score_pattern(results_dict=dict_e)


def get_worksheet_data():
    response = requests.get(url=LEAGUE_SHEET_ENDPOINT, auth=SHEET_AUTH)
    response.raise_for_status()
    data = response.json()
    league_table = data["leagueTable"]
    # pp.pprint(league_table)
    # print(len(league_table))
    #
    # for leagues in league_table:
    #     if "League 5513" in leagues["leagueId"]:
    #         index = leagues["id"]
    #         print(index)
    return league_table


def update_league(league_id, league_table, final_data):
    put = False
    index = None

    json_raw_data = json.dumps(final_data, indent=4)
    print(json_raw_data)
    body = {
        "leagueTable": dict_e

    }
    for leagues in league_table:
        if league_id in leagues["leagueId"]:
            index = leagues["id"]
            print(index)
            put = True
            break
    if put:
        make_put_request(json_data=body, row_index=index)
    else:
        make_post_request(json_data=body)


def make_put_request(json_data, row_index):
    response = requests.put(url=f"{LEAGUE_SHEET_ENDPOINT}/{row_index}", json=json_data, auth=SHEET_AUTH)
    data_to_put = response.json()

    if 'errors' in json_data:
        error_detail = json_data['errors'][0]['detail']
        print(f"Error: {error_detail}\n")
    else:
        print({"statusCode": 200, "body": data_to_put})


def make_post_request(json_data):
    """
    This function makes a post-request to the Sheety api in order to push the final data to the Google sheets
    """
    req = requests.post(url=LEAGUE_SHEET_ENDPOINT,
                        json=json_data, auth=SHEET_AUTH)
    data_to_push = req.json()

    if 'errors' in json_data:
        error_detail = json_data['errors'][0]['detail']
        print(f"Error: {error_detail}\n")
    else:
        print({"statusCode": 200, "body": data_to_push})


check_score_pattern(dict_e)
table = get_worksheet_data()
update_league(league_id="League 5687", league_table=table, final_data=None)
