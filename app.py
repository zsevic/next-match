import gi,signal,os,notify2,json,urllib
from htmldom import htmldom
from urllib.request import urlopen, Request
gi.require_version('Gtk','3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3','0.1')
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID='nextmatch'
URL='http://int.soccerway.com/teams/serbia/fk-crvena-zvezda-beograd/1942'

def main():
    indicator=appindicator.Indicator.new(APPINDICATOR_ID,os.path.abspath('./images/icon.png'),appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify2.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu=gtk.Menu()
    item_match=gtk.MenuItem('Next match')
    item_match.connect('activate',match)
    item_quit=gtk.MenuItem('Quit')
    item_quit.connect('activate',quit)
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
    dom=htmldom.HtmlDom()
    resp=urlopen(URL)
    html=resp.read().decode('utf-8')
    dom=dom.createDom(html);
    next=dom.find(".matches > tbody .result-win").last().parent().parent().next().html()
    next=parseHtml(next)
    return next

def parseHtml(html):
    res=""
    dom=htmldom.HtmlDom()
    dom=dom.createDom(html)
    time=dom.find(".timestamp").text()
    res+=time
    team_a=dom.find(".team-a").text()
    team_b=dom.find(".team-b").text()
    res+="".join([team_a.strip()," - ",team_b.strip()])
    return res

if __name__=="__main__":
    signal.signal(signal.SIGINT,signal.SIG_DFL)
    main()
