import tkinter
import webbrowser
from zeep import Client, Settings, xsd
from zeep.plugins import HistoryPlugin

# showing error messages


def errormsg(text):
    ferror.place(x=0, y=0)
    terror.place(x=0, y=0)
    terror.config(state='normal', height=10, width=50, bg='red')
    terror.delete('1.0', tkinter.END)
    terror.insert(tkinter.END, 'error!\n')
    terror.insert(tkinter.END, text+'\n')
    terror.config(state='disabled')
    okbutton = tkinter.Button(ferror, text='  ok  ',
                              command=ferror.place_forget)
    okbutton.place(x=200, y=200, anchor='center')

# outputing full data


def fullout(full):
    #new window and settings
    fullout = tkinter.Toplevel(root)
    fullout.title('full output')
    fullout.geometry('500x500')
    #scroll bars
    fullscroll_v = tkinter.Scrollbar(fullout)
    fullscroll_v.pack(side='right', fill="y")
    fullscroll_h = tkinter.Scrollbar(fullout, orient='horizontal')
    fullscroll_h.pack(side='bottom', fill="x")
    #output text widget
    outputbox = tkinter.Text(fullout, wrap='none', height=500, width=500,
                             yscrollcommand=fullscroll_v.set, xscrollcommand=fullscroll_h.set)
    outputbox.pack(fill='both')
    outputbox.insert(tkinter.END, full)
    fullscroll_h.config(command=outputbox.xview)
    fullscroll_v.config(command=outputbox.yview)
    fullout.geometry('500x500')

# sending the SOAP request


def send(LDB_TOKEN, choosecrs, WSDL):
    settings = Settings(strict=False)
    history = HistoryPlugin()
    WSDL = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=' + WSDL
    client = Client(wsdl=WSDL, settings=settings, plugins=[history])

    header = xsd.Element(
        '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken',
        xsd.ComplexType([
            xsd.Element(
                '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}TokenValue',
                xsd.String()),
        ]))
    header_value = header(TokenValue=LDB_TOKEN)

    res = client.service.GetDepBoardWithDetails(numRows=10,
                                                crs=choosecrs,
                                                _soapheaders=[header_value])
    simpleoutput = tkinter.Toplevel(root)
    simpleoutput.title("Trains at Station")
    simpleoutput.geometry('400x300')
    f1 = tkinter.Frame(root, height=300, width=400)
    f1.place(x=0, y=0)

    # scroll bars
    scroll_v = tkinter.Scrollbar(simpleoutput)
    scroll_v.pack(side='right', fill="y")

    simpledata = tkinter.Text(
        simpleoutput, wrap='word', yscrollcommand=scroll_v.set)
    simpledata.pack(fill='both', expand=0)
    root.geometry('400x300')
    simpleoutput.title("Trains at " + res.locationName + '\n')
    scroll_v.config(command=simpledata.yview)
    services = res.trainServices.service

    for i in range(0, len(services)):
        simpledata.insert(tkinter.END, str(i + 1) + '\n')
        t = services[i]

        l = t.destination.location
        l = tuple(l)

        simpledata.insert(tkinter.END, t.std + " to " +
                          t.destination.location[0].locationName + ",expected: " + t.etd + '\noperated by ' + t.operator + '\n')

        if t.delayReason != None:
            simpledata.insert(
                tkinter.END, 'delay reason: ' + t.delayReason + '\n')
        if t.cancelReason != None:
            simpledata.insert(
                tkinter.END, 'cancel reason: ' + t.cancelReason + '\n')

        if t.adhocAlerts != None:
            simpledata.insert(tkinter.END, 'alerts: ' +
                              str(t.adhocAlerts) + '\n')

        cp = t.subsequentCallingPoints
        cpl = cp.callingPointList
        cpl = cpl[0]
        namearr = []

        cpl = cpl['callingPoint']
        for q in range(0, len(cpl)):
            thiss = cpl[q]

            namearr += [thiss.locationName]
            et = thiss.et
            st = thiss.st
            if et == "On time":
                choice = st
            else:
                choice = et
            choice = "(" + choice + "), "
            namearr += [choice]
        callingstring = ''
        for c in range(0, len(namearr)):
            callingstring = callingstring + namearr[c]
        callingstring = callingstring[:-2]
        simpledata.insert(tkinter.END, 'calling at: ' + callingstring + '\n')
        simpledata.insert(tkinter.END, '--------------------\n')

    lout = tkinter.Label(f1, text='the train times are in the new window')
    lout.place(x=20, y=20)
    lt = tkinter.Label(f1, text='thank you for using pyLDBWS')
    lt.place(x=20, y=50)
    bfull = tkinter.Button(f1, text='output full data')
    bfull.place(x=20, y=80)
    bfull['command'] = lambda arg1=services: fullout(arg1)
    bmain = tkinter.Button(f1, text='main menu', command=f1.place_forget)
    bmain.place(x=20, y=170)

# checking the parameters before sending request


def check():
    ok = True
    key = ekey.get()
    if key == '' or key == 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx':
        errormsg('please provide a key')
        ekey.config(bg='red')
        ok = False

    elif len(key) != 36:
        errormsg('the key should be 36 characters, including dash')
        ok = False
    crs = ecrs.get()
    crs = crs.upper()
    crs = 'RDG'
    if crs == '':
        errormsg('no CRS')
        ecrs.config(bg='red')
        ok = False
    elif len(crs) != 3:
        errormsg('CRS must be 3 digit')
        ok = False
    #wsdl = ewsdl.get()
    wsdl = '2021-11-01'
    if wsdl == '':
        errormsg('no WSDL version')
        ewsdl.config(bg='red')
        ok = False
    elif len(wsdl) != 10:
        errormsg('the format of wsdl version is YYYY-MM-DD')
        ok = False
    if ok == True:
        ekey.config(bg='white')
        ecrs.config(bg='white')
        ewsdl.config(bg='white')
        send(key, crs, wsdl)


# main window and settings
root = tkinter.Tk()
root.geometry('400x300')
root.title('pyLDBWS')

# elements
# title
l1 = tkinter.Label(root, text='pyLDBWS', font=30)
l1.place(x=20, y=10)
l2 = tkinter.Label(
    root, text='Live Departure Boards Web Service request sender', font=('sans-serif', 12))
l2.place(x=20, y=40)
# entry boxes and labels
lkey = tkinter.Label(root, text='API key')
lkey.place(x=20, y=70)
ekey = tkinter.Entry(root, width=36)
ekey.place(x=20, y=90)
ekey.insert(0, "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
lcrs = tkinter.Label(root, text='CRS')
lcrs.place(x=20, y=120)
ecrs = tkinter.Entry(root, width=5)
ecrs.place(x=20, y=140)
ecrs.insert(0, "PAD")
lwsdl = tkinter.Label(root, text='WSDL version')
lwsdl.place(x=20, y=170)
ewsdl = tkinter.Entry(root, width=10)
ewsdl.place(x=20, y=190)
ewsdl.insert(0, "2021-11-01")
# links
llink = tkinter.Label(root, text='useful links(opens in browser)')
llink.place(x=200, y=120)
bdoc = tkinter.Button(root, text='LDBWS documentation')
bdoc['command'] = lambda url='http://lite.realtime.nationalrail.co.uk/openldbws/': webbrowser.open(
    url)
bdoc.place(x=200, y=150)
bcrs = tkinter.Button(root, text='list of CRS codes')
bcrs['command'] = lambda url='https://www.nationalrail.co.uk/stations_destinations/48541.aspx/': webbrowser.open(
    url)
bcrs.place(x=200, y=180)

bgit = tkinter.Button(root, text='GitHub repository')
bgit['command'] = lambda url='https://github.com/ic1149/pyLDBWS': webbrowser.open(
    url)
bgit.place(x=200, y=210)
# send button
bsend = tkinter.Button(root, text='send request!', command=check)
bsend.place(x=20, y=250)
# error frame and text widget
ferror = tkinter.Frame(root, height=300, width=400)
terror = tkinter.Text(ferror, height=200, width=300)

# main loop
root.mainloop()
