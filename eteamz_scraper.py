from BeautifulSoup import BeautifulSoup
from lxml.html import parse
import urllib2,urllib
import MySQLdb

states = ['Alaska', 'Alberta', 'Arizona', 'Arkansas', 'British Columbia', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'International', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Manitoba', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Brunswick', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'Newfoundland', 'North Carolina', 'North Dakota', 'Northwest Territories', 'Nova Scotia', 'Ohio', 'Oklahoma', 'Ontario', 'Oregon', 'Pennsylvania', 'Prince Edward Island', 'Puerto Rico', 'Quebec', 'Rhode Island', 'Saskatchewan', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'West Virginia', 'Wisconsin', 'Wyoming', 'Yukon'] #already did Washington,Alabama
genders = ['Female','Male','Coed']
ages = ['All Ages', 'Adult', 'Freshman', 'Jr Varsity', 'Senior', 'Sophomore', 'Varsity', 'Youth', 'Youth 10u', 'Youth 11u', 'Youth 12u', 'Youth 13u', 'Youth 14u', 'Youth 15u', 'Youth 16u', 'Youth 17u', 'Youth 18u', 'Youth 6u', 'Youth 7u', 'Youth 8u', 'Youth 9u']
sports = ['Action Sports', 'Adventure Racing', 'Aerobics', 'Archery', 'Badminton', 'Band', 'Bandy', 'Baseball', 'Baseball - Little League', 'Baseball FED Rules', 'Baseball Rules', 'Basketball', 'Baton Twirling', 'Biathlon', 'Billiards', 'Bobsleigh', 'Bocce', 'Body Building', 'Bowling', 'Boxing', 'Broomball', 'Canoeing', 'Cheerleading', 'Chess', 'Climbing', 'Company', 'Cricket', 'Croquet', 'Cross Country', 'Curling', 'Cycling', 'Dance', 'Darts', 'Disc Golf', 'Disc Sports', 'Diving', 'Dodgeball', 'Duathlon', 'Enduro and RAID Rally', 'Equestrian', 'Fencing', 'Field Hockey', 'Figure Skating', 'Fire', 'Fishing', 'Fitness', 'Flying-R/C', 'Foosball', 'Football', 'Football-AU', 'Football-Austrailian Rules', 'Football-Flag', 'Golf', 'Gymnastics', 'Handball', 'Handball-Team', 'Hockey-Ball', 'Hockey-Ice', 'Hockey-Inline', 'Hockey-Street', 'Horseshoes', 'Hunting', 'Ice Skating', 'Inline Skating', 'Judo', 'Jump Rope', 'Karate', 'Kayak', 'Kickball', 'Kite Club', 'Lacrosse', 'Luge', 'Lumberjacking', 'Marching Drill Team/Drum Lines', 'Martial Arts', 'Motocross', 'Motorsport', 'Mountain Biking', 'Multi-Sport', 'Myteam', 'Netball', 'Orienteering', 'Other', 'Other Sports', 'Outdoors', 'Outrigging', 'Paddleball', 'Paintball', 'Police', 'Polo', 'Poms', 'Quoit', 'Racewalking', 'Racing', 'Racing-Dragon Boat', 'Racing-Horse', 'Racing-Kart', 'Racquetball', 'Rafting', 'Ringette', 'Rodeo', 'Rowing', 'Rugby', 'Running', 'Sailing', 'Scouting', 'Scuba Diving', 'Sheriff', 'Shooting', 'Skateboarding', 'Skating', 'Skating-Speed', 'Skating-Synchro', 'Skiing', 'Skydiving', 'Skysurfing', 'Snorkeling', 'Snow Boarding', 'Soccer', 'Softball', 'Softball-Fastpitch', 'Softball-Slowpitch', 'Spinning', 'Squash', 'Step Teams', 'Stickball', 'Strength & Conditioning', 'Support', 'Surfing', 'Swimming', 'Swimming-Synchro', 'Tae Kwon Do', 'Tee Ball', 'Tennis', 'Tennis-Platform', 'Tennis-Table', 'Track & Field', 'Tractor Pulling', 'Triathlon', 'Ultimate Frisbee', 'Volleyball', 'Wakeboarding', 'Walking', 'Wally Ball', 'Water Polo', 'Water Skiing', 'Weight Lifting', 'Whiffle Ball', 'Windsurfing', 'Winter Sports', 'Wrestling', 'Yoga']
skills = ['Church', 'Club', 'College', 'Competitive', 'Corporate', 'Elementary', 'High School', 'Jr College', 'Middle School', 'National', 'Other', 'Professional', 'Recreational', 'Semi-Pro', 'Tournament']
organizations = ['AA Youth Basketball', 'American Amateur Baseball Congress', 'American Association of Cheerleading Coaches and Advisors', 'Amateur Athletic Union Boys Basketball', 'Amateur Athletic Union Girls Basketball', 'Amateur Athletic Union Jr. Golf', 'American Amateur Youth Baseball Alliance', 'All American Youth Football & Cheer', 'AFA Flag Football', 'AFA Semi-Pro', 'American Legion Baseball', 'American Running Association', 'American Roundball Corporation', 'Amateur Softball Association', 'American Youth Soccer Organization', 'Babe Ruth League Baseball', 'Basketball Congress International', 'British Youth American Football Association', 'Continental Amateur Baseball Association', 'Cal Ripken League', 'Connie Mack World Series', 'Central Texas Fastbreak Basketball', 'Dixie Youth Baseball', 'Dixie Softball', 'Dizzy Dean Baseball', 'Babe Ruth League Softball', 'Georgia Youth Football Conference', 'Indian Nations Youth Football', 'International Senior Softball Association', 'Little League Baseball and Softball', 'Mickey Mantle Baseball', 'Mid-American Youth Basketball', 'Mens Senior/Adult Baseball League', 'National Adult Baseball Association', 'National Amateur Baseball Federation', 'National Baseball Congress', 'National Field Hockey Coaches Association', 'National Softball Association', 'Pony Baseball', 'Pony', 'Pop Warner Little Scholars', 'Sandy Koufax Baseball', 'Soccer Association for Youth', 'Slow Pitch Softball Team', 'T-Ball USA', 'USA Hockey Inc.', 'USA Volleyball', 'USA Water Polo', 'United States Baseball Congress', 'USSSA Baseball', 'USSSA Fast Pitch Softball', 'USSSA Slow Pitch Softball', 'US Youth Soccer Association', 'Youth Football', 'Independent Softball Association - Canada', 'Senior Softball Canada', 'USA Track & Field ', 'Boy Scouts of America', 'Girl Scouts', 'World Organization of the Scout Movement', 'Scouts Canada']

def get_cursor():
    conn = MySQLdb.connect(host = '50.16.213.18', user = 'root', passwd = 'AwsOmPass123', db = 'eteamz')
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
        
def insert_links(links, state, gender, age, sport = "", skill = "", organization = ""):
    insert_str = ", ".join(["('%s', '%s', '%s', '%s', '%s')" % (link, state, gender, age, sport) for link in links])
    query_str = "INSERT INTO teams_sports (url, state, gender, age, sport) VALUES %s" % (insert_str)
    mysql = get_cursor()
    cur = mysql['cursor']
    cur.execute(query_str)
    mysql['conn'].commit()
    #return cur.rowcount

def mark_stop(page_num, state, gender, age, sport = "", skill = "", organization = ""):
    mysql = get_cursor()
    cur = mysql['cursor']
    cur.execute("INSERT INTO stops_sports (page_number, state, gender, age, sport) VALUES (%s, '%s', '%s', '%s', '%s')" % (str(page_num), state, gender, age, sport))
    mysql['conn'].commit()
    #return cur.rowcount

def main():
    #states = ['Washington']
    for state in states:
        #make sure it is done for every state
        for gender in genders:
            #make sure it is done for every gender
            for age in ages:
                for sport in sports:
                    page_num =  1 #starting page
                    last_link_len = 10
                    while  last_link_len >=10:
                        url = make_url(page = page_num, gender = gender, state = state, age = age, sport = sport)
                        links = get_links(url)
                        last_link_len = len(links)
                        page_num += 1
                        if links:
                            insert_links(links, state, gender, age, sport)
                            print 'inserted -- url: %s,   gender: %s,   # of links %s,  age: %s, sport: %s' % (url, gender, str(last_link_len), age, sport)
                    mark_stop(page_num - 1, state, gender, age, sport)
                    print 'Stopped at page # %s, state: %s, gender: %s, age: %s, sport: %s' %(str(page_num-1), state, gender, age, sport)

