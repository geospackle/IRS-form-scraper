from urllib.request import urlopen, HTTPError
from dataclasses import dataclass
import os
import sys
import re
import json
from bs4 import BeautifulSoup


@dataclass
class formData:
    form_number: str
    form_title: str
    form_year: int
    form_url: str

def getFormData(formName, startIdx=0):
    formName = re.sub(r'\s+', '+', formName)
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
            year = int(form.find("td", {"class": "EndCellSpacer"}).get_text(strip=True))  
            form = formData(productNumber, title, year, link)
            out.append(form)

    return out
            

def getFormInfo(forms):
    maxYear = max(form.form_year for form in forms)
    minYear = min(form.form_year for form in forms)
    out = {
        "form_number": forms[0].form_number,
        "form_title": forms[0].form_title,
        "min_year": minYear,
        "max_year": maxYear
        }
    return out

def showFormInfo(inValues):
    out = []
    for value in inValues:
        value = value.strip()
        print(value)
        allForms = processForms(value)
        formInfo = getFormInfo(allForms)
        out.append(formInfo)
    return json.dumps(out, indent=2)

def downloadForms(formName, years):
    lo = int(years.split("-")[0].strip())
    hi = int(years.split("-")[1].strip())
    allForms = processForms(formName)
    formNumber = allForms[0].form_number

    if not os.path.exists(f'downloads/{formNumber}'):
        os.makedirs(f'downloads/{formNumber}')

    for year in range(lo, hi+1):
        url = [form.form_url for form in allForms if form.form_year == year][0]
        response = urlopen(url)
        with open(f'downloads/{formNumber}/{year}.pdf', 'wb') as f:
            f.write(response.read())

    print('Files written')

downloadForms('form w-2', '2018-2020')
