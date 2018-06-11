import gi, signal, os, notify2, urllib
from urllib.request import urlopen
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

from bs4 import BeautifulSoup

APPINDICATOR_ID = 'nextmatch'
URL_FOOTBALL = 'http://int.soccerway.com/teams/serbia/fk-crvena-zvezda-beograd/1942'
URL_BASKETBALL = 'http://www.scoresway.com/?sport=basketball&page=team&id=150'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('./images/icon.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify2.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_football = gtk.MenuItem('Next football match')
    item_football.connect('activate', football)
    item_basketball = gtk.MenuItem('Next basketball match')
    item_basketball.connect('activate', basketball)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_football)
    menu.append(item_basketball)
    menu.append(item_quit)
    menu.show_all()
    return menu

def football(_):
    fb = notify2.Notification("<b>Next football match</b>", next_match(URL_FOOTBALL))
    fb.show()

def basketball(_):
    bb = notify2.Notification("<b>Next basketball match</b>", next_match(URL_BASKETBALL))
    bb.show()

def quit(_):
    notify2.uninit()
    gtk.main_quit()

def next_match(url):
    page = urlopen(url).read()
    soup = BeautifulSoup(page,'html.parser')
    past_matches = soup.findAll('a', {
        'class':[
            'result-win',
            'result-loss',
            'result-draw'
        ]}
    )
    cancelled_matches = soup.findAll('a', {
        'title': 'Cancelled' 
    })
    next_round = len(past_matches) + len(cancelled_matches)
    table = soup.find('table', {'class': 'matches'})
    table_body = table.find('tbody')
    matches = table_body.findAll('tr')
    try:
        next_one = matches[next_round]
        return parseHtml(str(next_one))
    except:
        return "There is no match in the schedule"

def parseHtml(html):
    res = ''
    match_html = BeautifulSoup(html, 'html.parser')    
    day = match_html.find('td', {'class': 'day'}).text
    date = match_html.find('td', {'class': 'full-date'}).text
    res += '\n'.join([day,date])
    if(match_html.find('td', {'class': 'score-time'})):
        time = match_html.find('td', {'class': 'score-time'}).text
        res += time
    
    team_a = match_html.find('td', {'class': 'team-a'})
    team_a = team_a.find('a').get('title')
    team_b = match_html.find('td', {'class': 'team-b'})
    team_b = team_b.find('a').get('title')
    res += ' '.join([team_a.strip(), '-', team_b.strip()])
    return res

if __name__ == "__main__":
    signal.signal(signal.SIGINT,signal.SIG_DFL)
    main()
