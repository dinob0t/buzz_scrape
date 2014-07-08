import json
import urllib2
import time
from datetime import date
from dateutil.rrule import rrule, DAILY

class NYTimesScraper():
    def __init__(self, apikey):
        # Creates a new NYTimesScraper Object using the apikey that was included.
        self.key = apikey
        # Base URI
        self.url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?'

    def _build_params(self, params):
        # if no parameters passed, raise error
        if not params:
            raise Exception('no search parameters!')
        # otherwise iterate through key and value pairs of params and join them
        # separated by &
        else:
            return '&'.join([k + '=' + v for k,v in params.iteritems()])

    def search(self, params={}):
        # generate a URL from the base URI + search params
        url = self.url + self._build_params(params)
        # append the API key
        url = url + '&api-key=%s' % self.key
        # generate request from URL
        req = urllib2.Request(url)
        # read the request result into data
        data = urllib2.urlopen(req).read()
        # load the JSON data and return it
        return json.loads(data)





# Own method for counting unique items in csv file
def count_items(col_num, csv_file):
    col_num = col_num -1
    with  open(csv_file,'r') as f:
        author_dict = {}
        for line in f:
            line = line.split('\n')
            line =  (line[0].split(','))
            if len(line)>1:
                if line[col_num] not in author_dict.keys():
                    author_dict[line[col_num]] = 1
                else:
                    author_dict[line[col_num]] += 1
    return author_dict

# set API key
nytimes = NYTimesScraper(apikey='3af7a458fcd2dfdafbac6e909b589681:10:69478982')
# Set number of pages to return
pages = 0

# Set up CSV to write to
filename = 'nytimesdata.csv'
writer = open(filename, 'w')
# Write the header
# writer.write('"LASTNAME","PUB_"DATE","SECTION_NAME","WORD_COUNT","SOURCE","URL"\n')
# writer.write('HEADLINE \n')

count = 0
a = date(2014, 1, 1)
b = date(2014, 7, 7)
print a, b
date_list = []
for dt in rrule(DAILY, dtstart=a, until=b):
    date_list.append(dt.strftime("%Y%m%d"))

# iterate over the pages
for page in range(pages+1):


    for date_str in date_list:


        time.sleep(0.5)

        # perform search and get article results
        articles = nytimes.search({'begin_date': date_str, 
            'end_date': date_str,
            'fl': 'headline,type_of_material',
            'page': str(page)})

        #Show how many results
        if page==0:
            total_hits = articles['response']['meta']['hits']  
            print total_hits, ' results found'

        #break out when have seen all responses to save on requests    
        if (page)*10 > total_hits:
            break
        # iterate over articles from response/docs
        for article in articles['response']['docs']:
            if article['type_of_material']:
                if article['type_of_material'] == 'News':
                    if article['headline']:
                
                        results_str = str(article['headline']['main'].encode('utf-8')) + ' \n'
                        writer.write(results_str)
                        count += 1
                        print str(article['headline']['main'].encode('utf-8')), 'count number: ', count

