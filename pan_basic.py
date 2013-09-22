
import urllib
import httplib
import json

class RequestCore(object):
    """
    """
    
    def __init__(self, ):
        """
        """
        pass



def main():
    """
    """
    # import httplib
    # conn = httplib.HTTPConnection("www.baidu.com")
    # conn.request("GET","/index.html")
    # r1 = conn.getresponse()
    # print r1.status, r1.reason
    # data1 = r1.read();
    # print data1

    print json.dumps(GET(), sort_keys=True,
                     indent=4, separators=(',', ': '))

######################################################################################################
# >>> import httplib, urllib                                                                         #
# >>> params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})             #
# >>>                                                                                                #
# >>> conn = httplib.HTTPConnection("bugs.python.org")                                               #
# >>> conn.request("POST", "", params, headers)                                                      #
# >>> response = conn.getresponse()                                                                  #
# >>> print response.status, response.reason                                                         #
# 302 Found                                                                                          #
# >>> data = response.read()                                                                         #
# >>> data                                                                                           #
# 'Redirecting to <a href="http://bugs.python.org/issue12524">http://bugs.python.org/issue12524</a>' #
# >>> conn.close()                                                                                   #
######################################################################################################
    
def GET():
    """
    """

    params = urllib.urlencode({
            'method':'info',
            'access_token':'3.811a254908d094012df764a38882a179.2592000.1348661720.2233553628-238347'})

    conn = httplib.HTTPSConnection("pcs.baidu.com")
    conn.request("GET", "/rest/2.0/pcs/quota?%s" % params)
    response = conn.getresponse()
    return json.loads(response.read())
    
    
    
if __name__ == '__main__':
    main()

