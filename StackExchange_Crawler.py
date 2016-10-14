#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

'''
StackExchange Crawler v0.3

Current version supports:
	- Crawling any StackExchange Website
	- Crawling only on highest vote questions
	- Crawls all answers for any every question
	
Bug Fixes to be done isA in the next version(s):
	- All websites in one dictionary
	- Colorful terminal prompts
	- Interactivity at listing StackExchange websites
	- Multithreading
'''
__version__ = 0.3

try:
	import requests,json,os,sys,threading
except ImportError:
	print "[!] Error importing one or more Library(ies)!\n[~] Leaving...\n\n"
	exit(-1)

'''
	=> Defining core data structures and functions 
	
	HTTP_Link(URI)
	-Description: Retrieves JSON data from a URI
	-Parameters:
		URI = URI that returns JSON data
	----------------------------------------------
	List_StackExchange_Websites()
	-Description: Lists all Stackexchange websites and returns a list
	----------------------------------------------
	WebSites dictionary:
	-Description: API link that lists all stackexchange websites
	----------------------------------------------
	GetHighVotesQA variable:
	-Description: API link that gets the highest voted questions and answers with specific tags and size
	----------------------------------------------
	
'''

WebSites = {'StackExchangeSites'	: 'https://api.stackexchange.com/2.2/sites?pagesize=319'}

AU = {
		'GetHighVotesQuestions' 		: 'https://api.stackexchange.com/2.2/questions?pagesize=%s&order=desc&sort=votes&tagged=%s&site=askubuntu',
		'GetHighVotesAnswers'			: 'https://api.stackexchange.com/2.2/questions/%s/answers?pagesize=%s&order=desc&sort=votes&site=askubuntu&filter=!-*f(6t*Zcw6a',
		'GetHighVotesQuestionsAndAllAnswers' : 'https://api.stackexchange.com/2.2/questions?pagesize=%s&order=desc&sort=votes&tagged=%s&site=askubuntu&filter=!3yXvh452cPbrm6i3H'
	 }


SOF = {		
		'GetHighVotesQuestions' 		: 'https://api.stackexchange.com/2.2/questions?pagesize=%s&order=desc&sort=votes&tagged=%s&site=stackoverflow',
		'GetHighVotesAnswers'			: 'https://api.stackexchange.com/2.2/questions/%s/answers?pagesize=%s&order=desc&sort=votes&site=stackoverflow&filter=!-*f(6t*Zcw6a',
		'GetHighVotesQuestionsAndAllAnswers' : 'https://api.stackexchange.com/2.2/questions?pagesize=%s&order=desc&sort=votes&tagged=%s&site=stackoverflow&filter=!3yXvh452cPbrm6i3H'
	  }

GetHighVotesQA = "https://api.stackexchange.com/2.2/questions?pagesize=%s&order=desc&sort=votes&tagged=%s&site=%s&filter=!3yXvh452cPbrm6i3H"

def HTTP_Link(URI):
	req = requests.get(URI)
	if req.status_code == 200:
		json_data = json.loads(req.text)
	else:
		print "[!] Error fetching URI contents!\n[~] Leaving...\n\n"
		exit(-1)
	return json_data

def List_StackExchange_Websites():
	
	req = requests.get(WebSites['StackExchangeSites'])
	
	if req.status_code == 200:
			json_data = json.loads(req.text)
	else:
		print "[!] Error Listing StackExchange sites\n[~] Leaving...\n\n"
		exit(-1)
	
	sites_list = []
	
	for i in json_data['items']:
		if i['name'].find('Meta') == -1:
			sites_list.append(i['api_site_parameter'])
	
	return sites_list

def Crawler(Questions_tags, Questions_Size, Input_Website):
	
	# Preparing directory name
	tags_list = ""
	for i in Questions_tags.split(';'):
		tags_list = tags_list + '.' + i.upper()
	tags_list = tags_list[1:]
	
	# Create directory for the tag
	new_dir = './Result/' + tags_list
	os.makedirs(new_dir)
	
	# Create questions file
	file_dir = new_dir + '/Questions'
	fp = open(file_dir, 'w')
	
	# Crawl data
	if str(type(Questions_Size))[7:-2] == 'int' and str(type(Questions_tags))[7:-2] == 'str':
		mydata = HTTP_Link(( GetHighVotesQA % (Questions_Size, Questions_tags, Input_Website) ))
	
	# Write JSON data into file
	json.dump(mydata['items'],fp)
	
	print "[~] Done" 

if __name__ == '__main__':
	
	SE_Sites = List_StackExchange_Websites()

	while True:
		
		# Getting a website to crawl
		print "\n[?] Which Website do you want to crawl?\n[~] Please write the Site API name not the website name or the URL\n[~] Example inputs: stackoverflow or askubuntu\n[~] Answer:",
		which_site = raw_input()
		which_site = which_site.lower()
		
		# Sanitizing user input
		while which_site not in SE_Sites:
			print "[!] Invalid website name, please specify website name again\n[~] Answer:"
			which_site = raw_input().lower()
		
		# Getting tags to search
		print "\n\n[?] Which tags do you want to look for?\n[~] Please write your tags delimited by a semi-colon ';', and maximum of 5 tags only\n[~] Example input: css;php;asm\n[~] Answer:",
		input_tags = raw_input()
		
		# Sanitizing user input
		while len(input_tags.split(';')) > 5:
			print "[!] You are only allowed to pass 5 tags, please specify your tags again\n[~] Answer:"
			input_tags = raw_input()
		
		# Getting Questions size
		print "\n\n[?] How many questions you want to crawl?\n[~] Please only specify a number\n[~] Example inputs: 50 or 15\n[~] Answer:", 
		Qsize = input()
		
		# Sanitizing user input
		if str(type(Qsize))[7:-2] == 'str':
			Qsize = int(Qsize,10)
		
		# Start a new thread
		try:
			t = threading.Thread(target = Crawler, args = (input_tags, Qsize, which_site,) )
		except:
			print "[!] Error creating new thread\n[~] Leaving...\n\n"
			exit(-1)
		
		t.start()
		
		# More?
		print "\n\n[?] Do you want to make any concurrent crawling?\n[~] Please answer with yes or no\n[~] Example input: yes\n[~] Answer:",
		concurrent_crawl = raw_input().lower()
		
		if concurrent_crawl == "no":
			break
		

