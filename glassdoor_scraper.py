from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
import csv

def get_jobs(driver_path,keyword,location, num_jobs, verbose,filename):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    options.add_argument('headless') #-- note that this mode is slower
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(driver_path, options=options)
    driver.set_window_size(1120, 1000)

#    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=United%20States&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    
    url = 'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=%22' + keyword + '%22&sc.keyword=%22' + keyword + '%22&locT=&locId=&jobType='

    driver.get(url)
    
    element = driver.find_element_by_xpath('//*[@id="sc.location"]')
    element.send_keys(location)
    time.sleep(.1)
    element = driver.find_element_by_xpath('//*[@id="HeroSearchButton"]')
    element.click()
    time.sleep(1)
    
    jobs = []
    
    cols = '''Job Title
    URL
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
    Revenue'''.split('\n') 
    
    jcomps = {}
    pgress=[]
    pgn = 1
    
    num_jj = driver.find_element_by_xpath('//*[@id="MainColSummary"]/div/div/div[2]').text
    print(num_jj)
    
    num_j = int(num_jj.split('"')[0])
    if num_j< num_jobs:
        nn = num_j
    else:
        nn = num_jobs
    
    with open(filename, 'w') as f:
        csv.writer(f,delimiter='|').writerow(cols)


    while len(jobs) < nn and pgn<=30:  #If true, should be still looking for new jobs.
        try:

            #Let the page load. Change this number based on your internet speed.
            #Or, wait until the webpage is loaded, instead of hardcoding it.
            time.sleep(2)

            #Test for the "Sign Up" prompt and get rid of it.
            try:
                driver.find_element_by_class_name("selected").click()
            except ElementClickInterceptedException:
                pass

            time.sleep(.1)

            try:
                driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  #clicking to the X.
            except NoSuchElementException:
                pass


            #Going through each job in this page
            job_buttons = driver.find_elements_by_class_name("jl")  #jl for Job Listing. These are the buttons we're going to click.
           # print(len(job_buttons))
            print(pgn,',',len(job_buttons))
            i=1
            for job_button in job_buttons:  
                
    #            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(nn)))
                print("Progress: {}".format("" + str(i) + "/" + str(len(job_buttons))))
                pr = str(len(jobs)) + "/" + str(nn)
                pgress.append(pr)
#                if pgress.count(pr)>5:
#                    continue
                    
#                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                    try:
#                        driver.find_element_by_xpath('.//li[@class="next"]//a').click()
#                    except NoSuchElementException:
#                        print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
#                        break

                
                if len(jobs) >= nn:
                    break
                try:    
                    element = driver.find_element_by_xpath('//*[@id="prefix__icon-close-1"]')
                    element.click()
                except:
                    pass

                job_button.click()  #You might
#                print('clicked')
                time.sleep(1)
                collected_successfully = False
                trials = 0
                while not collected_successfully:
                    if trials<5:
                        try:
                            company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text.split()[0]
                            location = driver.find_element_by_xpath('.//div[@class="location"]').text
                            job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                            job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                            collected_successfully = True

                        except:
                            time.sleep(5)
                            trials +=1
                    else:
                        company_name=-1
                        location =-1
                        job_title =-1
                        job_description =-1
                        collected_successfully = True
                        
                url = job_button.find_element_by_css_selector('a.jobInfoItem').get_attribute('href')
                try:
                    salary_estimate = driver.find_element_by_xpath('.//div[@class="salary"]').text
                except NoSuchElementException:
                    salary_estimate = -1 #You need to set a "not found value. It's important."

                try:
                    rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
                except NoSuchElementException:
                    rating = -1 #You need to set a "not found value. It's important."

                #Printing for debugging
                if verbose:
                    print("Job Title: {}".format(job_title))
                    print("Salary Estimate: {}".format(salary_estimate))
                    print("Job Description: {}".format(job_description[:500]))
                    print("Rating: {}".format(rating))
                    print("Company Name: {}".format(company_name))
                    print("Location: {}".format(location))

                #Going to the Company tab...
                #clicking on this:
                #<div class="tab" data-tab-type="overview"><span>Company</span></div>
                try:
                    driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()

                    try:
                        size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                    except NoSuchElementException:
                        size = -1

                    try:
                        founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                    except NoSuchElementException:
                        founded = -1

                    try:
                        type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                    except NoSuchElementException:
                        type_of_ownership = -1

                    try:
                        industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                    except NoSuchElementException:
                        industry = -1

                    try:
                        sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                    except NoSuchElementException:
                        sector = -1

                    try:
                        revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                    except NoSuchElementException:
                        revenue = -1


                except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                    size = -1
                    founded = -1
                    type_of_ownership = -1
                    industry = -1
                    sector = -1
                    revenue = -1



                if verbose:
                    print("Size: {}".format(size))
                    print("Founded: {}".format(founded))
                    print("Type of Ownership: {}".format(type_of_ownership))
                    print("Industry: {}".format(industry))
                    print("Sector: {}".format(sector))
                    print("Revenue: {}".format(revenue))

                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                
                
                if company_name not in jcomps.keys():   
                    jcomps[company_name] = [job_title]
                    jobs.append({"Job Title" : job_title,
                    "URL" : url,            
                    "Salary Estimate" : salary_estimate,
                    "Job Description" : job_description,
                    "Rating" : rating,
                    "Company Name" : company_name,
                    "Location" : location,
                    "Size" : size,
                    "Founded" : founded,
                    "Type of ownership" : type_of_ownership,
                    "Industry" : industry,
                    "Sector" : sector,
                    "Revenue" : revenue})                    
                    pst = [job_title,salary_estimate,job_description,rating,company_name,location,size,founded,type_of_ownership,industry,sector,revenue]
                    with open(filename, 'a') as f:
                        csv.writer(f, delimiter='|').writerow(pst)     
                else:
                    if job_title not in jcomps[company_name]:
                        jcomps[company_name].append(job_title)
                        jobs.append({"Job Title" : job_title,
                        "URL" : url,               
                        "Salary Estimate" : salary_estimate,
                        "Job Description" : job_description,
                        "Rating" : rating,
                        "Company Name" : company_name,
                        "Location" : location,
                        "Size" : size,
                        "Founded" : founded,
                        "Type of ownership" : type_of_ownership,
                        "Industry" : industry,
                        "Sector" : sector,
                        "Revenue" : revenue})                    
                        pst = [job_title,salary_estimate,job_description,rating,company_name,location,size,founded,type_of_ownership,industry,sector,revenue]
                        with open(filename, 'a') as f:
                            csv.writer(f, delimiter='|').writerow(pst)
                    else:
#                        print('doubled!!')
                        continue
                
                i+=1    
 #               else:
 #                   continue
                #add job to jobs
            #Clicking on the "next page" button
            try:
                driver.find_element_by_xpath('.//li[@class="next"]//a').click()
                pgn += 1
            except NoSuchElementException:
                print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(nn, len(jobs)))
                break
        except:
            continue
    driver.quit()

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
