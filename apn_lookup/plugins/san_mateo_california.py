import lxml.html
import requests

from apn_lookup.plugins import base_plugin

URL_1 = 'http://www.sanmateocountytaxcollector.org/SMCWPS/SearchParcels'
URL_2 = 'http://www.sanmateocountytaxcollector.org/SMCWPS/Parcel'

HEADERS_LINES = '''\
Host: www.sanmateocountytaxcollector.org
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://www.sanmateocountytaxcollector.org/SMCWPS/pages/secureSearch.jsp
Connection: keep-alive
'''


def makeSession():
    session = requests.Session()

    for line in HEADERS_LINES.splitlines():
        k, v = line.split(':', 1)
        session.headers[k.strip()] = v.strip()
    return session


class SanMateoPlugin(base_plugin.PluginBase):
    """

    San Mateo county version of the property tax lookup.

    """

    def setup(self):
        """
        Do nothing.
        """
        pass

    def teardown(self):
        """
        Do nothing.
        """
        pass

    def open(self):
        """
        Do nothing.
        """
        pass

    def close(self):
        """
        Do nothing.
        """
        pass

    def lookup(self, ID):

        params = {'parcelNumber': ID,
                  'searchType': 'parcel',
                  'listFirst': 'S',
                  'bkList': 'SS',
                  'addressTypeDsp': '',
                  'addressType': '',
                  'actionType': 'search',
                  'nextPage': './pages/parcelList.jsp',
                  'thisPage': './pages/secureSearch.jsp?erMsg=',
                  'parcel1': ID[0:3],
                  'parcel2': ID[3:6],
                  'parcel3': ID[6:9]
                  }
        session = makeSession()

        # Get cookie
        session.request('GET', 'http://www.sanmateocountytaxcollector.org/'
                        'SMCWPS/pages/secureSearch.jsp')
        print(session.cookies)
        print('PARAMS: ', params)
        req = session.request('POST', URL_1, params=params)
        print('COOKIE: ', session.cookies)
        html = lxml.html.fromstring(req.text)
        print(req.text)
        print(req.status_code)
        linkDict = {}
        for x in html.xpath('.//a'):
            linkDict = {k:v for k, v in x.items()}
            if linkDict.get('class') == 'nLink'\
               and 'showParcel' in linkDict['href']:
                print(linkDict)
                break

        print('I have a LinkDict')

        # Ugly parsing
        unparsed_args = linkDict['href'].split('showParcel(')[1].split(')')[0]
        parsed_args = unparsed_args.replace("'", '').split(',')
        params_list = ['parcelNumber',
                       'mainParcelNumber',
                       'billNumber',
                       'rollYear',
                       'billType',
                       'billStatus',
                       'newWin']

        new_params = {x: y for x, y in zip(params_list,
                                           parsed_args)}
        new_params['isHistory'] = 'N'
        new_params['bkList'] = 'SS_PR'
        new_params['nextPage'] = './pages/parcelDetail.jsp'

        # Reset the header
        session.headers.update(
            {'Referer': ('http://www.sanmateocountytaxcollector.org/SMCWPS/'
                         'pages/parcelList.jsp?list=SS')
            }
        )

        print('I HAVE NEW PARAMS: ', new_params)
        print('SENDING TO: ', URL_2)
        print('COOKIES: ', session.cookies)
        print('HEADERS: ', session.headers)
        req = session.request('POST', URL_2, params=new_params)
        html = lxml.html.fromstring(req.text)
        print('HTML: ', req.text)


def factory():
    return SanMateoPlugin()
