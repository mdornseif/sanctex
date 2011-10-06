# encoding: utf-8
"""
DSL zur beschreibung von REST-interfaces, angelehnt an https://gist.github.com/805540

Copyright (c) 2011 HUDORA. All rights reserved.
File created by Philipp Benjamin Koeppchen on 2011-02-23
"""

import urlparse
from pprint import pprint
import xml.dom.minidom
import optparse

from huTools.http import fetch
from huTools import hujson


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
FOREGROUND = 30
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"


def colored(text, color):
    """Färbt den Text mit Terminalsequenzen ein.

    >>> colored('whatever', RED)
    '\033[1;32mwhatever\033[0m' # wuerde dann in rot erscheinen, wenn man es ausgibt
    """
    start = COLOR_SEQ % (FOREGROUND + color)
    return start + text + RESET_SEQ


class Response(object):
    """Repräsentiert das Ergebnis einer REST-Anfrage.
    Mittels responds_* koennen zusicherungen geprueft werden:

    r.responds_http_status(200)
    r.responds_html()
    """

    def __init__(self, method, url, status, headers, content):  # pylint: disable=R0913
        self.method = method
        self.url = url
        self.status = status
        self.headers = headers
        self.content = content
        self.errors = 0

    def fail(self, message):
        """Negatives ergebnis einer Zusicherung."""
        self.errors += 1
        print '%s %s -> %s: %s' % (self.method, self.url, colored("FAIL", RED), message)
        print '=' * 50
        print "<<<",
        pprint(self.headers)
        print "<<<",
        print self.content
        print '=' * 50
        print

    def succeed(self, message):
        """Positives ergebnis einer Zusicherung."""
        print '%s %s -> %s: %s' % (self.method, self.url, colored("SUCCESS", GREEN), message)

    def expect_condition(self, condition, message):
        """sichert eine boolsche bedingung zu. sollte nicht direkt aufgerufen werden"""
        if not condition:
            self.fail(message)
        else:
            self.succeed(message)

    # low-level-beschreibungen der erwartungen
    def responds_http_status(self, expected_status):
        """sichert zu, dass mit dem gegebenen HTTP-status geantwortet wurde."""
        self.expect_condition(self.status == expected_status,
                        'expected status %s, got %s' % (expected_status, self.status))

    def responds_content_type(self, expected_type):
        """sichert zu, dass mit dem gegebenen Content-Type geantwortet wurde."""
        actual_type = self.headers.get('content-type')
        # evtl wird dem contenttype ein encoding nachgestellt, dies soll abgetrennt werden
        actual_type = actual_type.split(';')[0]
        self.expect_condition(actual_type == expected_type,
                        'expected content type %r, got %r' % (expected_type, actual_type))

    def converter_succeeds(self, converter, message):
        """sichert zu, dass content mittels converter(self.content) ohne exception konvertiert werden kann"""
        try:
            converter(self.content)
        except Exception:
            self.fail(message)
        else:
            self.succeed(message)

    # high-level-beschreibungen
    def responds_json(self):
        """sichert zu, dass die Antwort ein well-formed JSON-Dokument war."""
        self.responds_http_status(200)
        self.responds_content_type('application/json')
        self.converter_succeeds(hujson.loads, 'expected valid json')

    def responds_xml(self):
        """sichert zu, dass die Antwort ein well-formed XML-Dokument war."""
        self.responds_http_status(200)
        self.responds_content_type('application/xml')
        self.converter_succeeds(xml.dom.minidom.parseString, 'expected valid xml')

    def responds_plaintext(self):
        """sichert zu, dass die Antwort ein Plaintext-Dokument war."""
        self.responds_http_status(200)
        self.responds_content_type('text/plain')

    def responds_html(self):
        """sichert zu, dass die Antwort ein HTML-Dokument war."""
        self.responds_http_status(200)
        self.responds_content_type('text/html')

    def responds_not_found(self):
        """sichert zu, dass kein Dokument gefunden wurde."""
        self.responds_http_status(404)

    def responds_access_denied(self):
        """sichert zu, dass der Zugriff verweigert wurde."""
        self.responds_http_status(401)


class TestClient(object):
    """Hilfsklasse zum Ausfuehren von HTTP-Requests im Rahmen von Tests."""
    def __init__(self, host):
        self.host = host
        self.authdict = {}
        self.responses = []

    def add_credentials(self, auth, creds):
        """Stellt dem Client credentials zur Verfügung, die in GET genutzt werden können.

        auth: key der Credentials
        creds: HTTP-Credentials in der Form 'username:password'
        """
        self.authdict[auth] = creds

    def GET(self, path, auth=None, accept=None):  # pylint: disable=C0103
        """Führt einen HTTP-GET auf den gegebenen [path] aus.
        Nutzt dabei ggf. die credentials zu [auth] und [accept]."""
        if auth and auth not in self.authdict:
            raise ValueError("Unknown auth '%s'" % auth)

        headers = {}
        if accept:
            headers['Accept'] = accept

        url = urlparse.urlunparse(('http', self.host, path, '', '', ''))
        status, headers, content = fetch(url, content='', method='GET',
                                         credentials=self.authdict.get(auth),
                                         headers=headers, multipart=False, ua='', timeout=15)

        response = Response('GET', url, status, headers, content)
        self.responses.append(response)
        return response

    @property
    def errors(self):
        """Anzahl der fehlgeschlagenen Zusicherungen, die für Anfragen dieses Clients gefroffen wurden."""
        return sum(r.errors for r in self.responses)


def get_app_version():
    """Ermittelt die Aktuell zu deployende Version."""
    # Der dümmste YAML parser der Welt.
    for line in open('app.yaml'):
        if line.startswith('version: '):
            version = line.split()[1]
            return version.strip()
    raise RuntimeError("Can't detect version")


def create_testclient_from_cli(default_hostname, default_credentials_user, default_credentials_admin):
    """ Creates a Testclient with it's arguments from the Commandline.

    the CLI understands the options, --hostname, --credentials-user, --credentials-admin, their default
    values are taken from this functions args

    default_hostname: hostname, on wich to run tests, if none is provided via CLI
    default_credentials_user: HTTP-credetials for the user, if none are provided via CLI
    default_credentials_admin: HTTP-credetials for the admin, if none are provided via CLI

    returns a `TestClient`
    """
    parser = optparse.OptionParser()
    parser.add_option('-H', '--hostname', dest='hostname',
                                          help='Hostname, on which the tests should be run',
                                          default=default_hostname)
    parser.add_option('-u', '--credentials-user', dest='credentials_user',
                                                  help='HTTP-credentials for the non-admin-user',
                                                  default=default_credentials_user)
    parser.add_option('-a', '--credentials-admin', dest='credentials_admin',
                                                   help='HTTP-credentials for the admin-user',
                                                   default=default_credentials_admin)

    opts, args = parser.parse_args()
    if args:
        parser.error('positional arguments are not accepted')

    # Die or sorgen dafür, dass --option='' als 'nicht angegeben' gewertet wird, siehe aufruf im Makefile
    client = TestClient(opts.hostname or default_hostname)
    client.add_credentials('user', opts.credentials_user or default_credentials_user)
    client.add_credentials('admin', opts.credentials_admin or default_credentials_admin)

    return client
