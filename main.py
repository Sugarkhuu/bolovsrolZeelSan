import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# ikon news page
url_ikon = "https://ikon.mn/n/2tgu?fbclid=IwAR0fbYzhEzUJL9VWVDvllLvEFypzooHUwZyVrTSKUdQbxBGPsBPI7ZnkIZQ"

# setup and start the chrome driver 
chrome_options = Options() # Initialize options for Chrome browser
driver = webdriver.Chrome(options=chrome_options) # New webdriver instance
driver.get(url_ikon)

# switch to table as iframe
table_frame =driver.find_element(By.CSS_SELECTOR, '#wrapper > div.icontainer > div.icolumn > div > div.inews > div.icontent > div.flourish-embed > iframe')
driver.switch_to.frame(table_frame) # driver.switch_to.default_content()


# header of table 
hdrs = driver.find_elements(By.XPATH,"//*[@id='header-row']/div/div/p")
cols = ["Page"]
for hdr in hdrs:
    cols.append(hdr.text)

# table contents
table = []

i = 1
while i <= 10:
    print(f"Page {i} ... ")
    rows = driver.find_elements(By.XPATH,"//*[@id='table-inner']/div")
    for row in rows[1:]:
        row_val = [i]

        # collect each fields in a row
        for col in range(6):

            try:
                if col != 5:
                    val = row.find_element(By.XPATH, f"div[{col+1}]/div/p").text
                else:
                    val = row.find_element(By.XPATH, f"div[{col+1}]/div").text
            except:
                val = None # field empty
                
            row_val.append(val)

        # add row 
        table.append(row_val) 


    # next page
    driver.find_element(By.XPATH, "//*[@id='pagination']/button[2]").click()
    i += 1 


# make dataframe
df = pd.DataFrame(columns=cols, data=table)

# split name
df[['Овог', 'Нэр']] = df['Эцэг /эх/-ийн нэр Өөрийн нэр'].str.split(' ', 1, expand=True)

# save
df.to_csv('Боловсролын зээлийн сан түүх_1997_2023.csv', encoding="utf-8-sig")