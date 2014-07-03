from optparse import OptionParser, OptionGroup
from lib.utils.FileUtils import File
import os

class ArgumentsParser(object):
    def __init__(self, script_path):
        usage = "Usage: %prog [-u|--url] target [-e|--extensions] extensions [options]"
        parser = OptionParser(usage)
        self.script_path = script_path
        # Mandatory arguments
        mandatory = OptionGroup(parser, 'Mandatory')
        mandatory.add_option("-u", "--url", help="URL target", action="store", type="string", dest="url", default=None)
        mandatory.add_option("-e", "--extensions", help="Extensions list separated by comma (Example: php, asp)", \
            action="store", dest="extensions", default=None)

        # Optional Settings
        settings = OptionGroup(parser, 'Optional Settings')
        settings.add_option("-r", "--recursive", help="Bruteforce recursively", action="store_true", \
            dest="recursive", default=False)
        settings.add_option("-t", "--threads", help="Number of Threads", action="store", type="int", \
            dest="threadsCount", default=10)
        settings.add_option("-x", "--exclude-500", help="Exclude Internal Server Error Status (500)", action="store_true", \
            dest="exclude500", default=False)
        settings.add_option("--cookie", "--cookie", action="store", type="string", dest="cookie", default=None)
        settings.add_option("--user-agent", "--user-agent", action="store", type="string", dest="useragent", \
            default=None)
        settings.add_option("-w", "--wordlist", action="store", dest="wordlist", default=("{1}{0}db{0}dicc.txt".format(os.path.sep, self.script_path)))
        settings.add_option("-l", "--lowercase", action="store_true", dest="lowercase", default="False")
        
        settings.add_option("--timeout", "--timeout", action="store", dest="timeout", type="int", default=30)
        settings.add_option("--ip", "--ip", action="store", dest="ip", default=None)
        settings.add_option("--max-retries", "--max-retries", action="store", dest="maxRetries", type="int", default=5)
        settings.add_option("--no-follow-redirects", "--no-follow-redirects", action="store_true", dest="followRedirects", default=False)
        settings.add_option("--http-proxy", "--http-proxy", action="store", dest="httpProxy", type="string", default=None)

        #settings.add_option("--ignore-response-status", "--ignore-response-status", action="store", type="string", dest="ignoreResponseStatus", default="")

        # Reports Settings
        reports = OptionGroup(parser, 'Reports')
        reports.add_option("-o", "--output", action="store", dest="outputFile", default=None)
        reports.add_option("--json-output", "--json-output", action="store", dest="jsonOutputFile", default=None)
        

        parser.add_option_group(mandatory)
        parser.add_option_group(settings)
        parser.add_option_group(reports)
        (options, arguments) = parser.parse_args()
        if options.url == None:
            print("Url target is missing")
            exit(0)
        if options.extensions == None:
            print("No extension specified. You must specify at least one extension")
            exit(0)
        
        with File(options.wordlist) as wordlist:
            if not wordlist.exists():
                print ("The wordlist file does not exists")
                exit(0)
            if not wordlist.isValid():
                print ("The wordlist is invalid")
                exit(0)
            if not wordlist.canRead():
                print ("The wordlist cannot be read")
                exit(0)
        if options.httpProxy is not None:
            if options.httpProxy.startswith("http://"):
                self.proxy = options.httpProxy
            else:
                self.proxy = "http://{0}".format(options.httpProxy) 
        else:
            self.proxy = None
        self.url = options.url
        self.extensions = [extension.strip() for extension in options.extensions.split(",")]
        self.useragent = options.useragent
        self.cookie = options.cookie
        self.threadsCount = options.threadsCount
        self.exclude500 = options.exclude500
        self.wordlist = options.wordlist
        self.lowercase = options.lowercase
        self.outputFile = options.outputFile
        self.jsonOutputFile = options.jsonOutputFile
        self.timeout = options.timeout
        self.ip = options.ip
        self.maxRetries = options.maxRetries
        self.recursive = options.recursive
        self.redirect = not options.followRedirects