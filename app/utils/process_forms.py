import re
from urllib.request import urlopen, HTTPError
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class FormData:
    form_number: str
    form_title: str
    form_year: int
    form_url: str

def getFormData(formName, startIdx=0):
    urlFormName = re.sub(r"\s+", "+", formName)
    url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow={startIdx}&criteria=formNumber&value={urlFormName}&isDescending=false"
    try:
        with urlopen(url) as response:
            html = response.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            entries = soup.find("table", {"class": "picklist-dataTable"}).findAll("tr")[1:]
            if len(entries) == 0: raise Exception(f"Search term '{formName}' not found")

    except HTTPError as e:
        print("error fetching resource", e)

    return entries

def processForms(formName):
    forms = []
    allForms = []
    formData = []
    startIdx = 0
    while startIdx == 0 or len(forms) == 200:
        forms = getFormData(formName, startIdx)
        startIdx += 200
        allForms += forms
    for form in allForms:
        productNumber = form.find("a").get_text(strip=True) 
        r = re.compile(formName, re.IGNORECASE)
        if r.fullmatch(productNumber):
            link = form.find("a")["href"] 
            title = form.find("td", {"class": "MiddleCellSpacer"}).get_text(strip=True)  
            year = int(form.find("td", {"class": "EndCellSpacer"}).get_text(strip=True))  
            form = FormData(productNumber, title, year, link)
            formData.append(form)

    if len(formData) == 0: raise Exception(f"Exact search term '{formName}' not found")

    return formData
 
