
#%%
import pandas as pd
from tqdm import tqdm

import bs4
#%%
from bs4 import BeautifulSoup
import requests
#%%
steelsites = pd.read_excel("Steel Suppliers.xlsx")
steelsites_dict = steel.to_dict("records")
#%%
#urlss = steel["url"]
#%%


def get_category_data(item, category):
    if category in item.text:
        return item.text.lstrip(category)
    else: 
        return None


#%%
def get_steel_site_data(url):
    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    div = soup.findAll("div", attrs={"class":"mw-parser-output"})
    location = None
    product_cat = None
    products = None
    if len(div) >= 1:
        listitems  = div[0].findAll("li")
        for item in listitems:
            location = get_category_data(item, "Location: ") if get_category_data(item, "Location: ") else location
            product_cat = get_category_data(item, "Steel product category: ") if get_category_data(item, "Steel product category: ") else product_cat
            products = get_category_data(item, "Steel products: ") if get_category_data(item, "Steel products: ") else products
    
    return (location, product_cat , products)


#%%
for site in tqdm(steelsites_dict):
    data = get_steel_site_data(site.get("url"))
    site["location"] = data[0]
    site["product_cat"] = data[1]
    site["products"] = data[2]

df_result = pd.DataFrame(steelsites_dict)
df_result.to_excel("resutls.xlsx")
# %%
