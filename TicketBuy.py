#!/usr/bin/env python
#The MIT License (MIT)
#
#Copyright (c) 2016 Vincent Ruijter
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#

import re
import sys
import optparse
import requests
import subprocess
import BeautifulSoup

def get_counter(soup):
	available = soup.findAll('div', attrs={'class': 'counter counter-available'})
	content = []
	counter = 0

	for i in available:
		content.append(str(i))

	for i in content:
		a =  re.findall("<div class=\"counter-value\">(.*?)</div>", i)
		c = map(int, a)

		counter =  int(c[0])

	if not counter:
		counter = 0
	
	return counter	

def get_sold(soup):
	sold = soup.findAll('div', attrs={'class':'counter-value'})
	x = re.findall('.*>(.*)<.*', str(sold[1]))[0]

	return int(x)
	
def get_available(data, counter, sold, url):
	links = re.findall('/tickets/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data.text)
	tickets = []
	for x in links:
		if x not in tickets:
			tickets.append(x)
	atickets = tickets[:-sold]

	ticketlinks = []
	for ticket in atickets:
		ticketlink = "https://www.ticketswap.nl"+ticket+"/reserveren/aanmelden/1"
		ticketlinks.append(ticketlink)

	return ticketlinks

def main():
	parser = optparse.OptionParser(usage="%prog [options]", version="%prog 0.1")
        mandatory = optparse.OptionGroup(parser, "Mandatory")
	optional = optparse.OptionGroup(parser, "Optional")	

        mandatory.add_option("-u", "--url", type="string", help="target url", dest="url")
	optional.add_option("-r", "--reserve", action="store_true", help="reserve ticket", dest="reserve")

        parser.add_option_group(mandatory)
	parser.add_option_group(optional)

        options, arugments = parser.parse_args()
        url = options.url
	reserve = options.reserve

	headers = {
		'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) Gecko/20100101 Firefox/29.0'	
	}

	banner = """
            ___
               `-._\ /     `~~"--.,_
              ------>|              `~~"--.,_
               _.-'/ '.____,,,,----"""~~```'

    				TicketBuy 
     					evict"""

	print banner
	
        if url == None:
                parser.error("Please specify a URL!")

	loop = True

	try:
		while loop == True:
			data = requests.get((url), headers=headers)

			soup = BeautifulSoup.BeautifulSoup(data.text)
			counter = get_counter(soup)

			sold = get_sold(soup)
			tickets = get_available(data, counter, sold, url)
		
			for ticket in tickets:
				if reserve == True:
					subprocess.Popen(['open', ticket])
					subprocess.Popen(['say', 'ticket found!'])
					loop = False
					print ("\nTrying to reserve %s\n" % ticket)
					break
					sys.exit(0)
				else:
					print ticket
				
			sys.stdout.write("\r%i tickets available!" % counter)
			sys.stdout.flush()		

	except KeyboardInterrupt:
		print "\n^C pressed!\n"
		sys.exit()
		
if __name__ == "__main__":
	main()
