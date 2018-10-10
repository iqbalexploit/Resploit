#! /usr/bin/python

try:
        import sys
        import socket
        import requests

        rhost = sys.argv[1]
        wordlist = sys.argv[2]

        print '[*] Checking RHOST... ',
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
                status = s.connect_ex((rhost, 80))
                s.close()
                if status == 0:
                        print '[DONE]'
                        pass
                else:
                        print '[FAIL]'
                        print '[!] Error: Cannot Reach RHOST %s\n' %(rhost)
                        sys.exit(1)
        except socket.error:
                print '[FAIL]'
                print '[!] Error: Cannot Reach RHOST: %s\n' %(rhost)
                sys.exit(1)

        print '[*] Parsing Wordlist... ',
        try:
                with open(wordlist) as file:
                        to_check = file.read().strip().split('\n')
                print '[DONE]'
                print '[*] Total Paths to Check: %s' %(str(len(to_check)))
        except IOError:
                print '[FAIL]'
                print '[!] Error: Failed to Read Specified File\n'
                sys.exit(1)

        def checkpath(path):
                try:
                        response = requests.get('http://' + rhost + '/' + path).text
                except Exception:
                        print '[!] Error: An Unexpected Error Occured'
                        sys.exit(1)
                if "Underconstruction" not in response:
                        print '[*] Valid Path Found: /%s' %(path)

        print '\n[*] Beginning Scan...\n'
        for i in range(len(to_check)):
                checkpath(to_check[i])
        print '\n[*] Scan Complete!'
except KeyboardInterrupt:
        print '\n[!] Error: User Interrupted Scan'
        sys.exit(1)
