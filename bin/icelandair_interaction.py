from splinter import Browser
import datetime, time, re
import csv

departlist = ['JFK','BOS','ORD','EWR','WAS']
arrivelist = ['LGW','CDG','MUC']

sites  = ['us','ca','fr','co.uk','is','no']

browser = Browser('firefox')
data = []
for date_inc in range(3,20):
    date = datetime.datetime.today() + datetime.timedelta(days=date_inc)

    if len(str(date.month)) == 1:
        mon = '0' + str(date.month)
    else:
        mon = str(date.month)

    if len(str(date.day)) == 1:
        day = '0' + str(date.day)
    else:
        day = str(date.day)
    yr = str(date.year)

    input_date1 = mon + day + yr
    input_date2 = day + mon + yr

    for site in sites:
        url = 'http://www.icelandair.' + site + '/'
        for depart in departlist:
            for arrive in arrivelist:
                try:
                    browser.visit(url)
                    browser.find_by_id('dep_1').fill(depart)
                    time.sleep(2)
                    browser.find_by_id('arr_1').fill(arrive)
                    time.sleep(2)
                    browser.find_by_id('oneway').first.click()
                    mask = browser.find_by_id('departDate-1').first.outer_html
                    if re.search('(?<=placeholder=")\w+',mask).group(0) == 'mm':
                        browser.find_by_id('departDate-1').fill(input_date1)
                    else:
                        browser.find_by_id('departDate-1').fill(input_date2)
                    time.sleep(2)
                    browser.find_by_id('search_now').first.click()
                    time.sleep(20)
                except:
                    pass

                for x in range(0,6):
                    try:
                        price             = browser.find_by_xpath('//*[@id="table-bound0-cell0' + str(x) + '-available-content"]/div/div/span').first.value
                        currency_element  = browser.find_by_xpath('//*[@id="table-bound0-cell0' + str(x) + '-available-content"]/div/div/abbr').first.outer_html
                        currency          = re.search('(?<=title=")(.*)(?=" class)',currency_element).group(0)
                        #currency          = browser.find_by_xpath('//*[@id="owd-pricing-description"]/div/div[2]/div/div/span[2]').first.value
                        flightdate        = browser.find_by_xpath('//*[@id="availability-bound-0"]/header/h2/div[2]/div/div').first.value
                        flightdate2       = mon + '/' + day + '/' + yr
                        airline1          = browser.find_by_xpath('//*[@id="table-bound0-row'+ str(x) + '"]/div/div[2]/span[1]').first.value
                        flightid1         = browser.find_by_xpath('//*[@id="table-bound0-row' + str(x) + '"]/div/div[2]/span[2]').first.value
                        flighttime        = browser.find_by_xpath('//*[@id="table-bound0-row' + str(x) + '"]/div/div[1]/div/span[1]/strong').first.value
                        airportfrom       = browser.find_by_xpath('//*[@id="table-bound0-rowheader' + str(x) + '"]/div/div[1]/div/span').first.value
                        airportfrom_abbr  = browser.find_by_xpath('//*[@id="table-bound0-rowheader' + str(x) + '"]/div/div[1]/div/abbr').first.value
                        airportto         = browser.find_by_xpath('//*[@id="table-bound0-rowheader' + str(x) + '"]/div/div[2]/div/span').first.value
                        airportto_abbr    = browser.find_by_xpath('//*[@id="table-bound0-rowheader' + str(x) + '"]/div/div[2]/div/abbr').first.value
                        departtime        = browser.find_by_xpath('//*[@id="table-bound0-rowheader' + str(x) + '"]/div/div[1]/time').first.value
                        arrivetime        = browser.find_by_xpath('//*[@id="table-bound0-rowheader' + str(x) + '"]/div/div[2]/time').first.value
                        timestamp         = datetime.datetime.now().timestamp()

                        obs = [price,
                                currency,
                                flightdate,
                                flightdate2,
                                airline1,
                                flightid1,
                                flighttime,
                                airportfrom,
                                airportfrom_abbr,
                                airportto,
                                airportto_abbr,
                                departtime,
                                arrivetime,
                                timestamp]

                        data.append(obs)
                    except:
                        pass

now = datetime.datetime.now()
suffix = str(now.month) + '_' + str(now.day) + '_' + str(now.year) + '_' + str(now.hour) + '_' + str(now.minute)
outcsv = 'icelandair' + '_' + suffix + '.csv'
with open(outcsv, 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    varnames = ['Price',
                'Currency',
                'Flight_date',
                'Flight_date2',
                'Airline1',
                'Flightid1',
                'Flight_time',
                'Airport_dep',
                'Airport_dep_abbr',
                'Airport_arr',
                'Airport_arr_abbr',
                'Depart_time',
                'Arrive_time',
                'timestamp']
    writer.writerow(varnames)
    writer.writerows(data)

#with open(outfile, 'w') as f:
        #f.write(browser.html.encode('utf-8'))
    
    
