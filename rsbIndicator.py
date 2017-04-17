import gi,signal,os,notify2,json,urllib
from htmldom import htmldom
from pyquery import PyQuery as pq
from urllib.request import urlopen, Request
gi.require_version('Gtk','3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3','0.1')
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID='myappindicator'

def main():
    indicator=appindicator.Indicator.new(APPINDICATOR_ID,os.path.abspath('rsb.svg'),appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify2.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu=gtk.Menu()
    item_quit=gtk.MenuItem('Quit')
    item_quit.connect('activate',quit)
    item_match=gtk.MenuItem('Next match')
    item_match.connect('activate',match)
    menu.append(item_match)
    menu.append(item_quit)
    menu.show_all()
    return menu

def match(_):
    n=notify2.Notification("<b>Next match</b>",next_match())
    n.show()

def quit(_):
    notify2.uninit()
    gtk.main_quit()

def next_match():
    url='http://int.soccerway.com/teams/serbia/fk-crvena-zvezda-beograd/1942'
    resp=urlopen(url)
    html=resp.read()
    d=pq(html)
    d=d(".matches > tbody tr .result-win:last")
    return str(d)

if __name__=="__main__":
    signal.signal(signal.SIGINT,signal.SIG_DFL)
    main()
