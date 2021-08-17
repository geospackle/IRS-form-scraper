import sys
import json
from utils.process_forms import processForms

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

def showFormInfo(formNames):
    formInfos = []
    formNames = formNames.split(",")
    for name in formNames:
        name = name.strip()
        allForms = processForms(name)
        formInfo = getFormInfo(allForms)
        formInfos.append(formInfo)
    return json.dumps(formInfos, indent=2)

if __name__ == "__main__":
    print(showFormInfo(sys.argv[1]))
