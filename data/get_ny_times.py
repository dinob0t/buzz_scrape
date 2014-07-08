import json
import urllib2
import time

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
pages = 500

# Set up CSV to write to
filename = 'nytimesdata.csv'
writer = open(filename, 'a')
# Write the header
# writer.write('"LASTNAME","PUB_"DATE","SECTION_NAME","WORD_COUNT","SOURCE","URL"\n')
# writer.write('HEADLINE \n')

count = 0

# iterate over the pages
for page in range(pages):
    time.sleep(0.5)

    # perform search and get article results
    articles = nytimes.search({'begin_date': '20140101', 
        'end_date': '20140601',
        'fl': 'headline,source',
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
        if article['source']:
            if article['source'] == 'The New York Times':
                if article['headline']:
                    
                    results_str = str(article['headline']['main'].encode('utf-8')) + ' \n'
                    writer.write(results_str)
                    count += 1
                    print str(article['headline']['main'].encode('utf-8')), 'count number: ', count

                     
        # store each field in results string
        # results_str = ""
        # add each field after checking that it exists
        # if article ['byline'] and article['byline']['person'] and 'lastname' in article['byline']['person'][0].keys():
        #     results_str += '"' + article['byline']['person'][0]['lastname'] + '",'
        # else:
        #     results_str += '"UNKNOWN AUTHOR",'

        # if article['pub_date']:
        #     results_str += '"' + article['pub_date'] + '",'
        # else:
        #     results_str += '"UNKNOWN PUB DATE",'

        # if article['section_name']:
        #     results_str += '"' + article['section_name'] + '",'
        # else:
        #     results_str += '"UNKNOWN SECTION NAME",'

        # if article['word_count']:
        #     results_str += '"' + article['word_count'] + '",'
        # else:
        #     results_str += '"UNKNOWN WORD COUNT",'

        # if article['source']:
        #     results_str += '"' + article['source']  + '",'
        # else:
        #     results_str += '"UNKNOWN SOURCE",' 
        # # final part of string writes new line
        # if article['web_url']:
        #     results_str += '"' + article['web_url'] + '"\n"'
        # else:
        #     results_str += '"UNKNOWN URL"\n'

        
        # write out this result
        


# print count_items(5, 'nytimesdata.csv')

#1. Most recent article on missing plane 
#2014-06-09 - yes still in the media
#First article
#2014-03-07

#2. Using 'print count_items(5, 'nytimesdata.csv')'
# shows that 'AP' gave the most source material
# {'"SOURCE"': 1, '"AP"': 135, '"The New York Times"': 110, '"Reuters"': 14}

# Since I'm new here in New York, I would like to use
# the yelp API to find good coffee. Looks like there
# are plenty of python wrappers out there already 
