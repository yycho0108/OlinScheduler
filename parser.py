import re
# parser.py : reformat information

def parseTime(time): #convert to numeric min, 24 hr scale
    time = time.strip();
    reg = r"([0]?[0-9]|1[0-2]):([0-5][0-9])(?:\s)?(?i)(am|pm)"; #regex for time
    
    p = re.compile(reg);
    m = p.search(time);
    
    hr = int(m.group(1));
    mn = int(m.group(2));
    xm = m.group(3);
    
    if hr != 12 and xm.startswith(('p','P')):
        hr += 12;
    elif hr == 12 and xm.startswith(('a','A')):
        hr = 0;
    return hr*60 + mn;

def parseDay(d):
    return 'MTWRF'.find(d);

def parseMeet(inList):
    """
    parseMeet(inList) --> list of {day:String,time[start,end]:list[int,int],loc:String}
    """
    outList = []
    for meet in inList:
        try:
            time,loc = meet.split(';');
            days,time = time.split(' ',1);
            start,end = time.split(' - ',1);
            if start.find('AM') == -1 and start.find('PM') == -1:
                if end.find('AM') != -1:
                    start += ' AM';
                else:
                    start += ' PM';
            for d in days:
                outList.append({
                    'day':d,
                    'time':[parseTime(start),parseTime(end)],
                    'loc':loc
                    });
        except ValueError: #Invalid/Undetermined Meeting Pattern
            pass;
    return outList;
