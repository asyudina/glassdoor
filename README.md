# glassdoor parser
Glassdoor jobs parsing by keyword and location

Requires chrome driver chromedriver to be installed https://sites.google.com/a/chromium.org/chromedriver/downloads

```
Parameters
----------
driver_path - str 
    path to chromedriver file downloaded by link above
keyword - str
    keyword for job search
location - str
    location for job search
verbose - bool
    True if need to print detailed results while parsing

Returns
-------
df    
    dataframe with jobs
```


Information available:
```
Job Title
Salary Estimate
Job Description
Rating
Company Name
Location
Size
Founded
Type of ownership
Industry
Sector
Revenue
```
