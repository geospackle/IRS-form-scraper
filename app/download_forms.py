import os
import sys
from urllib.request import urlopen, HTTPError
from utils.process_forms import processForms

def downloadForms(formName, years):
    if "-" in years:
        lo = int(years.split("-")[0].strip())
        hi = int(years.split("-")[1].strip())
    else:
        lo = int(years)
        hi = int(years)
    if len(str(lo)) != 4 and len(str(hi)) !=4:
        raise TypeError('Wrong year format')

    allForms = processForms(formName)
    formNumber = allForms[0].form_number

    if not os.path.exists(f'downloads/{formNumber}'):
        os.makedirs(f'downloads/{formNumber}')

    for year in range(lo, hi+1):
        url = [form.form_url for form in allForms if form.form_year == year][0]

        try:
            response = urlopen(url)
        except HTTPError as e:
            print('Error fetching resource from external server', e)
            
        with open(f'downloads/{formNumber}/{formNumber} - {year}.pdf', 'wb') as f:
            f.write(response.read())

    print("Files written in './downloads'")

if __name__ == "__main__":
    downloadForms(sys.argv[1], sys.argv[2])
