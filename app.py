import gi,signal,os,notify2,urllib
from htmldom import htmldom
from urllib.request import urlopen, Request
gi.require_version('Gtk','3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3','0.1')
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID='nextmatch'
URL_FOOTBALL='http://int.soccerway.com/teams/serbia/fk-crvena-zvezda-beograd/1942'
URL_BASKETBALL='http://www.scoresway.com/?sport=basketball&page=team&id=150'

def main():
    indicator=appindicator.Indicator.new(APPINDICATOR_ID,os.path.abspath('./images/icon.png'),appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify2.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu=gtk.Menu()
    item_football=gtk.MenuItem('Next football match')
    item_football.connect('activate',football)
    item_basketball=gtk.MenuItem('Next basketball match')
    item_basketball.connect('activate',basketball)
    item_quit=gtk.MenuItem('Quit')
    item_quit.connect('activate',quit)
    menu.append(item_football)
    menu.append(item_basketball)
    menu.append(item_quit)
    menu.show_all()
    return menu

def football(_):
    fb=notify2.Notification("<b>Next football match</b>",next_match(URL_FOOTBALL))
    fb.show()

def basketball(_):
    bb=notify2.Notification("<b>Next basketball match</b>",next_match(URL_BASKETBALL))
    bb.show()

def quit(_):
    notify2.uninit()
    gtk.main_quit()

def next_match(url):
    dom=htmldom.HtmlDom()
    resp=urlopen(url)
    html=resp.read().decode('utf-8')
    dom=dom.createDom(html)
    win_length=dom.find(".result-win").length()
    draw_length=dom.find(".result-draw").length()
    loss_length=dom.find(".result-loss").length()
    length=win_length+draw_length+loss_length
    next=dom.find(".matches > tbody").children().eq(length).html()
    next=parseHtml(next)
    return next

def parseHtml(html):
    res=""
    dom=htmldom.HtmlDom()
    dom=dom.createDom(html)
    time=dom.find(".timestamp").text()
    if(len(time)==0):
        res+="N/A\n"
    else:
        res+=time
    team_a=dom.find(".team-a").text()
    team_b=dom.find(".team-b").text()
    res+="".join([team_a.strip()," - ",team_b.strip()])
    return res

if __name__=="__main__":
    signal.signal(signal.SIGINT,signal.SIG_DFL)
    main()
