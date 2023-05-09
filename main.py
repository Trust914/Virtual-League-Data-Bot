import time
import json
import requests
import os
import selenium.common
import smtplib
# from email.message import EmailMessage
from tempfile import mkdtemp
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

SHEET_AUTH = (os.environ.get("LEAGUE_SHEETY_USER_NAME"), os.environ.get("LEAGUE_SHEETY_PASSWORD"))
LEAGUE_SHEET_ENDPOINT = os.environ.get("LEAGUE_SHEETY_ENDPOINT")
PATTERN_TEAMS_ENDPOINT = os.environ.get("PATTERN_TEAMS_ENDPOINT")
SHEET_LINK = os.environ.get("LEAGUE_SHEET_LINK")
FROM_EMAIL = os.environ.get("LEAGUE_FROM_EMAIL")
FROM_EMAIL_PASS = os.environ.get("LEAGUE_FROM_EMAIL_PASS")


def get_web():
    """
    This function opens the webpage
    """
    # Required dependencies to use selenium
    serv = service.Service("/opt/chromedriver")

    # Set chrome options for working with headless mode (no screen)
    driver_options = webdriver.ChromeOptions()
    driver_options.binary_location = '/opt/chrome/chrome'
    driver_options.add_argument("headless")
    driver_options.add_argument("no-sandbox")
    driver_options.add_argument("--single-process")  # Lambda only gives us only one CPU
    driver_options.add_argument("--no-zygote")  # Don't create zygote processes because Lambda gives us only one CPU
    driver_options.add_argument("--disable-dev-shm-usage")  # Create a temporary folder for shared memory files
    driver_options.add_argument("--disable-dev-tools")  # Disable Chrome dev tools
    driver_options.add_argument(f"--user-data-dir={mkdtemp()}")  # Create a temporary folder to user data
    driver_options.add_argument(f"--data-path={mkdtemp()}")  # Create a temporary folder to browser data
    driver_options.add_argument(f"--disk-cache-dir={mkdtemp()}")  # Create temporary folder to cache
    driver = webdriver.Chrome(service=serv, options=driver_options)

    driver.get("https://vsmobile.bet9ja.com/mobile/themes/?sk=bet9ja&t=b61c29e6-9348-4c58-af90-378760a74693&game"
               "=league_premier&pid=14001,14003,14011,14012,14014,14015,14016,"
               "14017&v=0&text=Premier&lang=en_GB#resutls&ui_state=dialog")
    driver.maximize_window()
    time.sleep(10)
    return driver


def click_menu_icon(web_driver):
    """
    This function clicks the menu icon in the top left corner of the webpage
    """
    while True:
        try:
            web_driver.find_element(by=By.CSS_SELECTOR,
                                    value="div.ui-panel-wrapper div.ui-header span.left a.ui-link").click()
            break
        except (
                selenium.common.exceptions.ElementNotInteractableException,
                selenium.common.exceptions.ElementClickInterceptedException
        ):
            web_driver.refresh()  # keep refreshing the page until the error disappears
            time.sleep(5)


def get_current_league(web_driver):
    """
    Extract the current running league ID from the webpage
    """

    def refresh():
        click_menu_icon(web_driver)
        time.sleep(5)
        web_driver.find_element(by=By.LINK_TEXT,
                                value="Results").click()  # click the "results" link to open the page for all leagues
        # data

    try:
        refresh()
    except (
            selenium.common.exceptions.NoSuchElementException,
            selenium.common.exceptions.ElementClickInterceptedException):
        refresh()
        click_menu_icon(web_driver)

    time.sleep(10)
    # get current league
    league_value = web_driver.find_element(by=By.XPATH,
                                           value="//*[@id='results-div-header']/table/tbody/tr/td[1]/span").text

    return league_value


def get_results_body(current_league_id, web_driver):
    """
    This function extracts the raw league data from the result page
    """
    vals = []  # List to store all match fixations in the entire league
    total_weeks = 38  # total weeks in a league
    min_week = 15
    while True:
        updated_league_value = get_current_league(web_driver)
        print(f"Current league is {updated_league_value}\n")

        time.sleep(5)
        wait = WebDriverWait(web_driver, 10)
        # locate the entire results table
        temp = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#results-div-header-mainTable tbody")))
        time.sleep(5)
        results_body = temp.find_elements(by=By.TAG_NAME, value="tbody")  # results-div-header-mainTable > tbody
        total_week_result = len(results_body)
        print(f"Total number of weeks completed: {total_week_result}\n")

        if total_week_result < min_week:
            # Since the total week per league is 38, we want to maximize the use of time and resources. After opening
            # the result page, if the current week in the current league is less than the minimum week that the bot
            # can wait for until the maximum is reached, we exit without extracting any data and wait for the next
            # run time
            print(
                f"Number of completed weeks in {updated_league_value} is not up to the minimum requirement.\nExiting "
                f"the program...........")
            results_body = None
            break
        elif total_week_result in range(min_week, total_weeks + 1) or updated_league_value != current_league_id:
            # The current league is complete, extract the data and perform other actions required
            break
        # else:
        #     # We are in a minimum acceptable week. The bot will now wait for the current league to elapse,
        #     # extract data and perform other actions required
        #     print(f"Current league week is {total_week_result} and is close to the final week: {total_weeks}.\n"
        #           f"Refreshing and Waiting for {current_league_id} to end.....\n")
        #     web_driver.refresh()  # refresh the webpage and check if the league weeks are up to the maximum = 38
        #     time.sleep(5)
    # driver.close()
    if results_body is not None:
        # extract each row results in the result table.each row contains a match fixation, e.g., ARS 1-3 CHE
        for results in results_body:
            temp = results.find_elements(by=By.TAG_NAME, value="tr")
            temp = temp[1:]
            vals.append(temp)
    return vals


def get_scores(league_table_raw):
    """
    This function extracts the real text from each match fixation, sorting the teams alphabetically
    """
    dic = {}  # This dictionary stores the real match fixation text.

    for val in league_table_raw:
        match_results_list = []  # temporary list to store a match result like so: [ARS 1-3 CHE]
        current_week = league_table_raw.index(val)
        for td in range(len(val)):
            match_results_list.append(val[td].text)
        dic[current_week + 1] = sorted(match_results_list)
    return dic  # For example, { 1: [ARS 1-3 CHE], 2: [FOR 0-0 MNC]}


def find_win_lose_draw(scores_dict):
    """
    This function gets the final result of a particular club in a match fixation for all the weeks
    """
    for keys in scores_dict:
        team_dict = {}  # Dictionary to store a team's score -
        # either Lose(L), Win(W) or Draw(D) per match fixation in a week
        for vals in scores_dict[keys]:  # e.g., [ARS 1-3 CHE]
            vals = vals.split()
            # print(vals)
            real_score = vals[1]  # e.g., 1-3
            # print(real_score)
            left_team = vals[0]  # e.g., ARS
            right_team = vals[2]  # e.g., CHE
            left_team_score = real_score.split("-")[0]
            right_team_score = real_score.split("-")[1]
            if left_team_score > right_team_score:
                team_dict[left_team] = "W"
                team_dict[right_team] = "L"
            elif left_team_score < right_team_score:
                team_dict[left_team] = "L"
                team_dict[right_team] = "W"
            else:
                team_dict[left_team] = "D"
                team_dict[right_team] = "D"

            scores_dict[keys] = {key: team_dict[key] for key in sorted(team_dict)}  # Update the original dictionary
    return scores_dict


def clean_scores(uncleaned_scores, current_league):
    """
    This function cleans the data and gets all the scores of each club per week
    """
    scores = []
    teams = [team for key in uncleaned_scores for team in uncleaned_scores[key]]  # all the teams in the league
    teams = sorted(set(teams))
    print(teams)

    for team in teams:
        score_result = ""
        # e.g., if  uncleaned_scores = {1: # {'ARS': 'W', 'ASV': 'W', },2: {'ARS': 'L', 'ASV': 'W',}},  then:
        for key in uncleaned_scores:
            for club_name in uncleaned_scores[key]:
                if team == club_name:
                    score_result += f"{uncleaned_scores[key][club_name]}-"
                    # print(score_result)
        score_result = score_result[:len(score_result) - 1]  # remove the extra dash(-) at the end of the string
        scores.append(score_result)
    # print(scores)
    cleaned_results = {team_name.lower(): team_score for team_name, team_score in zip(teams, scores)}
    cleaned_results["leagueId"] = current_league
    cleaned_results["timeStamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return cleaned_results


def check_score_pattern(results_dict: dict):
    teams = []  # to store teams with no draw pattern
    pattern = {}  # to store the pattern dictionary
    min_week = 15
    # iterate through each key-value pair in the dictionary
    for key, value in results_dict.items():
        # if key is "leagueId" or "timeStamp", store its value in pattern dictionary and move to the next iteration
        if key in ["leagueId", "timeStamp"]:
            pattern[key] = value
            continue

        # split the score string and check if it meets the criteria for a no-draw pattern
        club_score = value.split("-")
        if len(club_score) < min_week or "D" not in club_score:
            continue

        # get the positions of all "D" in the score string
        draw_positions = [i for i, score in enumerate(club_score) if score == "D"]
        if len(draw_positions) < 2:  # the team has only one draw or no draw...
            continue

        # iterate through each pair of adjacent draw positions and check if the distance between them is >= 10
        for i in range(len(draw_positions) - 1):
            start, end = draw_positions[i], draw_positions[i + 1]
            if end - start >= min_week:
                # if the distance is >= 10, add the team to the teams list and break out of the loop
                teams.append(key.upper())
                break

    # create a string of teams with no draw pattern and store it in the pattern dictionary
    if teams:
        teams_string = ",".join(teams)
        pattern["noDrawPatternTeams"] = teams_string
        print(f"Pattern found in {teams_string}")
    else:
        teams_string = "No teams without draw"
        pattern["noDrawPatternTeams"] = teams_string
        print(teams_string)

    return teams_string, pattern


def send_email(to_email, user, new_pattern_teams, old_pattern_teams, id_league):
    print(f"old_pattern_teams: {old_pattern_teams}")

    # Check if the league is in old_pattern_teams and if the pattern is new
    for league in old_pattern_teams:
        if id_league == league.get("leagueId"):
            old_pattern = league.get("noDrawPatternTeams")
            if new_pattern_teams == old_pattern or new_pattern_teams == "No teams without draw":
                # The Pattern is not new, so don't send the email
                return
            break

    # If the league was not found in old_pattern_teams or the pattern is new, send the email
    if new_pattern_teams != "No teams without draw":
        message = f"Hey {user},\n\nA NO DRAW pattern has been found in the scores of the following team(s):\n{new_pattern_teams}.\n\n" \
                  f"Click the Google sheet link to check {SHEET_LINK}."

        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=FROM_EMAIL, password=FROM_EMAIL_PASS)
            connection.sendmail(from_addr=FROM_EMAIL, to_addrs=to_email,
                                msg=f"Subject:Pattern Found!\n\n{message}".encode("utf-8"))


def get_worksheet_data(endpoint, sheet):
    response = requests.get(url=endpoint, auth=SHEET_AUTH)  # league table sheet
    response.raise_for_status()
    data = response.json()
    usable_data = data[f"{sheet}"]

    return usable_data


def make_leaguetable_post_request(json_data, endpoint):
    """
    This function makes a post-request to the Sheety api in order to push the final data to the Google sheets
    """
    req = requests.post(url=endpoint,
                        json=json_data, auth=SHEET_AUTH)
    data_to_push = req.json()

    if 'errors' in json_data:
        error_detail = json_data['errors'][0]['detail']
        print(f"Error: {error_detail}\n")
    else:
        print({"statusCode": 200, "body": data_to_push})


def make_leaguetable_put_request(json_data, row_index, endpoint):
    response = requests.put(url=f"{endpoint}/{row_index}", json=json_data, auth=SHEET_AUTH)
    data_to_put = response.json()

    if 'errors' in json_data:
        error_detail = json_data['errors'][0]['detail']
        print(f"Error: {error_detail}\n")
    else:
        print({"statusCode": 200, "body": data_to_put})


def update_league_table(league_id, sheet_table, sheet_name, final_data, url):
    put = False
    index = None

    json_raw_data = json.dumps(final_data, indent=4)
    print(json_raw_data)
    body = {
        f"{sheet_name}": final_data

    }
    for leagues in sheet_table:
        if league_id in leagues["leagueId"]:
            index = leagues["id"]
            print(index)
            put = True
            break
    if put:
        make_leaguetable_put_request(json_data=body, row_index=index, endpoint=url)
    else:
        make_leaguetable_post_request(json_data=body, endpoint=url)


# ---------------------------------------------------- Execute Bot -----------------------------------------------------

def handler(event=None, context=None):
    users = [{"name": "Trust", "email": "trustezzy@gmail.com"}, {"name": "CJ", "email": "okaforc684@gmail.com"}]
    sheet1 = "leagueTable"
    sheet2 = "patternTeams"

    # Get the current league
    driver = get_web()
    current_league_val = get_current_league(driver)

    # Extract league data and club scores
    league_results = get_results_body(current_league_val, driver)
    if league_results :
        raw_scores = get_scores(league_results)

        # Clean the scores and update the league table
        uncleaned_league_scores = find_win_lose_draw(raw_scores)
        final_league_results = clean_scores(uncleaned_league_scores, current_league_val)

        table_from_league_sheet = get_worksheet_data(endpoint=LEAGUE_SHEET_ENDPOINT, sheet=sheet1)
        update_league_table(league_id=current_league_val, sheet_table=table_from_league_sheet,
                            final_data=final_league_results, sheet_name=sheet1, url=LEAGUE_SHEET_ENDPOINT)

        # Check for score patterns and update the pattern table
        table_from_pattern_sheet = get_worksheet_data(endpoint=PATTERN_TEAMS_ENDPOINT, sheet=sheet2)
        pattern_teams, pat_dict = check_score_pattern(results_dict=final_league_results)
        update_league_table(league_id=current_league_val, sheet_table=table_from_pattern_sheet, final_data=pat_dict,
                            url=PATTERN_TEAMS_ENDPOINT, sheet_name=sheet2[:11])

        # Send an email if a new pattern is found
        for receivers in users:
            send_email(to_email=receivers["email"], new_pattern_teams=pattern_teams,
                       old_pattern_teams=table_from_pattern_sheet, id_league=current_league_val, user=receivers["name"])


if __name__ == "__main__":
    handler()
