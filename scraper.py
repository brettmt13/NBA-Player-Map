import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
import json
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

# options = Options()
# options.add_argument('--headless=new')

# driver = webdriver.Chrome(options=options)

# driver.get("https://www.scoresandodds.com/nba/props")
# driver.implicitly_wait(10)

# elements = driver.find_elements(By.CLASS_NAME, "props-name")

# playerSlate = []
# for element in elements:
#     name = element.find_element(By.TAG_NAME, 'a')
#     playerSlate.append(name.text)

# driver.quit()

# res = requests.get("https://www.scoresandodds.com/nba/props")
# soup = BeautifulSoup(res.text, 'lxml')
# print(res.text)
# elements = soup.find_all("div", class_="props-name")

# for element in elements:
#     print(element)



import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
import json
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
playerIndex = {}
# options.add_argument('--headless=new')

'''
Draftkings version but it is a very dynamic site and doesn't always work
'''
# driver.get("https://sportsbook.draftkings.com/leagues/basketball/nba")
# driver.implicitly_wait(10)
# driver.find_element(By.ID, 'game_category_Player Points').click()

# playerNameElements = driver.find_elements(By.CLASS_NAME, "sportsbook-row-name")
# ----------------------------------------

# get the elements that have the player names
driver = webdriver.Chrome(options=options)
driver.get("https://www.scoresandodds.com/nba/props")
driver.implicitly_wait(10)

playerNameElements = driver.find_elements(By.CLASS_NAME, "props-name")

# get the text from the element and append the player name to the list
playerSlate = []
for nameElement in playerNameElements:
    name = nameElement.find_element(By.CSS_SELECTOR, 'a').text # the player name is in the <a> element
    playerSlate.append(name)

print(playerSlate)
time.sleep(2)

# for each player, get the game log information
for player in playerSlate[:1]:
    
    playerTable = pd.DataFrame()
    # get the link to the game log
    time.sleep(3)
    nameQuery = player.replace(' ', '+')
    url = f'https://www.google.com/search?q={nameQuery}+nba+espn+game+log'
    res = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})
    driver.get(url)
    searchResults = driver.find_elements(By.CLASS_NAME, "yuRUbf")
    gameLogLink = searchResults[0].find_element(By.CSS_SELECTOR, 'a').get_attribute("href")
    print("Link to game log:", gameLogLink)
    
    time.sleep(3)
    
    # open the game log
    html_res = pd.read_html(gameLogLink)
    print("game log:")
    
    # go through every month's table and get points, assists, rebounds, turnovers
    for table in range(len(html_res)):
        if len(html_res[table].columns) == 17:
            currentTable = html_res[table]
            currentTable = currentTable[['PTS', 'AST', 'REB', 'STL', 'BLK', 'TO', 'MIN']] # only keep these stats
            for col in currentTable.columns:            
                currentTable[col] = pd.to_numeric(currentTable[col], errors='coerce')
            currentTable = currentTable.dropna()
            currentTable = currentTable.astype(int)
            playerTable = pd.concat([playerTable, currentTable], ignore_index=True)
    
    # now with the current full season table, take the df and put it into dictionary
    playerIndex[player] = playerTable
    
driver.quit()

for player in playerIndex:
    print(player)
    print(playerIndex[player])
    


# # res = requests.get("https://www.scoresandodds.com/nba/props")
# # soup = BeautifulSoup(res.text, 'lxml')
# # print(res.text)
# # elements = soup.find_all("div", class_="props-name")

# # for element in elements:
# #     print(element)



            # print(currentTable['PTS'])

            # for row in table['PTS']:
            #     try: # if a number, then it is a stat and add to player's stats
            #         int(row)
            #         playerIndex[player] = {'PTS': table['PTS'].to_list}
            #         print(playerIndex)
                    
                    
                # except: # ignore string rows
                #     print(table.columns)
    