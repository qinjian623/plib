
import urllib
import httplib
import json

class RequestCore(object):
    
    def __init__(self, host = "pcs.baidu.com"):
        self._host = host

    def GET(self, url, params):
        conn     = httplib.HTTPSConnection(self._host)
        conn.request("GET", url+ "?"+  urllib.urlencode(params))
        response = conn.getresponse()
        response_string = response.read()
        return json.loads(response_string)

    def POST(self, url, params):
        headers  = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn     = httplib.HTTPSConnection(self._host)
        conn.request("POST", url, urllib.urlencode(params), headers)
        response = conn.getresponse()
        response_string =  response.read()
        return json.loads(response_string);

def main():
    params   = {'method':'info',
          'access_token':'3.811a254908d094012df764a38882a179.2592000.1348661720.2233553628-238347'}
    url      = "/rest/2.0/pcs/quota"
    r        = RequestCore()
    json_var = r.POST(url, params)
    
    print json.dumps(json_var,
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': '))

    
if __name__ == '__main__':
    main()

