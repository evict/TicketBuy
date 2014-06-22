#!/usr/bin/env python
import re
import sys
import optparse
import requests
import subprocess
from bs4 import BeautifulSoup

def get_counter(soup):
	available = soup.findAll('div', attrs={'class': 'counter counter-available'})
	content = []
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
	sold = soup.findAll('span', attrs={'class': 'type sold'})	
	x=0
	for i in sold:
		x=x+1
	return x
	
def get_available(data, counter, sold, url):
	links = re.findall('/tickets/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data.text)
	tickets = []
	for x in links:
		if x not in tickets:
			tickets.append(x)

	atickets = tickets[:-sold]
	tickets = []
	for ticket in atickets:
		ticketlink = "https://www.ticketswap.nl"+ticket+"/reserveren/aanmelden/1"
		tickets.append(ticketlink)
	
	return tickets

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

        if url == None:
                parser.error("Please specify a URL!")

	loop = True

	try:
		while loop == True:
			data = requests.get((url), headers=headers)

			soup = BeautifulSoup(data.text)
			counter = get_counter(soup)

			if counter >= 1:
				loop = False
			sold = get_sold(soup)
			tickets = get_available(data, counter, sold, url)

			for ticket in tickets:
				if reserve == True:
					subprocess.Popen(['open', ticket])
					loop = False
					print ("\nTrying to reserve %s" % ticket)
					break
					sys.exit(0)
				else:
					print ticket
				
			sold = get_sold(soup)
		
			sys.stdout.write("\r%i tickets available!" % counter)
			sys.stdout.flush()		

	except KeyboardInterrupt:
		print "\n^C pressed!"
		sys.exit()
		
if __name__ == "__main__":
	main()
