from urllib.request import urlopen, HTTPError
from dataclasses import dataclass
import re
from bs4 import BeautifulSoup
 
@dataclass
class formData:
    form_number: int
    form_title: str
    form_year: int
    form_url: str

def getFormData(formName, startIdx=0):
    formName = re.sub('\s+', '+', formName)
    url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow={startIdx}&criteria=formNumber&value={formName}&isDescending=false"
    try:
        with urlopen(url) as response:
            html = response.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            entries = soup.find("table", {"class": "picklist-dataTable"}).findAll("tr")[1:]
            if len(entries) == 0: raise Exception("Search term not found")

    except HTTPError as e:
        print('error fetching resource', e)

    return entries

def processForms(formName):
    out = []
    forms = getFormData(formName)
    allForms = forms
    startIdx = 200
    while len(forms) == 200:
        forms = getFormData(formName, startIdx)
        startIdx += 200
        allForms += forms
    for form in allForms:
        productNumber = form.find('a').get_text(strip=True) 
        r = re.compile(formName, re.IGNORECASE)
        if bool(r.fullmatch(productNumber)):
            link = form.find('a')['href'] 
            title = form.find("td", {"class": "MiddleCellSpacer"}).get_text(strip=True)  
            year = form.find("td", {"class": "EndCellSpacer"}).get_text(strip=True)  
            form = formData(productNumber, title, year, link)
            out.append(form)

    return out
            

print(processForms('form w-2'))
