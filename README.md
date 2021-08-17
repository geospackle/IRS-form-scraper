# IRS-form-scraper

### About

The utilities in the repo provide information on IRS forms and enable downloading of the forms.

This has been tested on Python 3.8.10, but should run on Python 3.4+.

### Installation

Clone the repo and in the main directory run

```
pip3 install -r requirements.txt
```

### Usage

To find general information about IRS forms, run 'app/show_form_info.py' with a comma-separated list of form number(s) as argument. The result is shown in JSON format in the terminal window.

```
python3 show_form_info.py 'form w-2, form 1095-c'
```

To download form(s) for a range of year(s), run 'app/download_forms.py' with form number and range of years as arguments.

```
python3 download_forms.py 'form w-2' 2001-2006
```

Arguments are case-insensitive.

