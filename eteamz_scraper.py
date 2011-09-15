from BeautifulSoup import BeautifulSoup
from lxml.html import parse
import urllib2,urllib
import MySQLdb

def get_cursor():
    conn = MySQLdb.connect(host = '50.16.213.18', , db = 'eteamz')
    cursor = conn.cursor()
    return {'cursor': cursor, 'conn' : conn}

def get_links(url):
    doc = parse(url).getroot()
    #main_table = doc.cssselect('div#search_results table')
    result_links = [link.get('href') for link in doc.cssselect("div#search_results table a")] #create a list of urls from the anchor tags in table, then get the 'href' from that list
    return result_links

def make_url(page, search_box = "", city = "", state = "", sport = "", skill = "", age = "", gender = "", organization = ""):
    base_url = "http://search.eteamz.com/search/"
    params = {
        'page': page,
        'search_box' : search_box,
        'city' : city,
        'state' : state,
        'sport' : sport,
        'skill' : skill,
        'age' : age,
        'gender' : gender,
        'organization' : organization,
        }
    params_url = urllib.urlencode(params)
    return base_url + "?" + params_url
        
def insert_links(links, state, gender, age):
    insert_str = ", ".join(["('%s', '%s', '%s', '%s')" % (link, state, gender, age) for link in links])
    query_str = "INSERT INTO teams (url, state, gender, age) VALUES %s" % (insert_str)
    mysql = get_cursor()
    cur = mysql['cursor']
    cur.execute(query_str)
    mysql['conn'].commit()
    return cur.rowcount

def mark_stop(page_num, state, gender, age):
    mysql = get_cursor()
    cur = mysql['cursor']
    cur.execute("INSERT INTO stops (page_number, state, gender, age) VALUES (%s, '%s', '%s', '%s')" % (str(page_num), state, gender, age))
    mysql['conn'].commit()
    return cur.rowcount

def main():
    #states = ['Washington']
    states = ['Alabama', 'Alaska', 'Alberta', 'Arizona', 'Arkansas', 'British Columbia', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'International', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Manitoba', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Brunswick', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'Newfoundland', 'North Carolina', 'North Dakota', 'Northwest Territories', 'Nova Scotia', 'Ohio', 'Oklahoma', 'Ontario', 'Oregon', 'Pennsylvania', 'Prince Edward Island', 'Puerto Rico', 'Quebec', 'Rhode Island', 'Saskatchewan', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'West Virginia', 'Wisconsin', 'Wyoming', 'Yukon'] #already did Washington
    genders = ['Female','Male','Coed']
    ages = ['All Ages', 'Adult', 'Freshman', 'Jr Varsity', 'Senior', 'Sophomore', 'Varsity', 'Youth', 'Youth 10u', 'Youth 11u', 'Youth 12u', 'Youth 13u', 'Youth 14u', 'Youth 15u', 'Youth 16u', 'Youth 17u', 'Youth 18u', 'Youth 6u', 'Youth 7u', 'Youth 8u', 'Youth 9u']
    for state in states:
        #make sure it is done for every state
        for gender in genders:
            #make sure it is done for every gender
            for age in ages:
                page_num =  1 #starting page
                last_link_len = 10
                while  last_link_len >=10:
                    url = make_url(page = page_num, gender = gender, state = state, age = age)
                    links = get_links(url)
                    last_link_len = len(links)
                    page_num += 1
                    if links:
                        insert_links(links, state, gender, age)
                        print 'inserted -- url: %s,   gender: %s,   # of links %s,  age: %s' % (url, gender, str(last_link_len), age)
                mark_stop(page_num - 1, state, gender, age)
                print 'Stopped at page # %s, state: %s, gender: %s, age: %s' %(str(page_num-1), state, gender, age)

