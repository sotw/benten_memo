#[]== Think this two-layered index seems common
#[]== 1. Index page 2. detail page
#[]== Rather than create two python, I should create one only

import os, sys, re, codecs
import argparse
import logging
import urllib
import requests
import sqlite3
#import textwrap
from os.path import expanduser
from subprocess import PIPE
from subprocess import Popen
from lxml import etree
from io import StringIO
from pprint import pprint
from decimal import *

from requests.models import stream_decode_response_unicode
from HMTXCLR import clrTx
from textwrap import TextWrapper
from textwrap import dedent
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

global DB
global tTarget
global args
global ARGUDB
global _wrap
global LINKS
global ctl
global staticStr
global ScreenI
global stockdb
global cursor

staticStr = 'https://tw.stock.yahoo.com/quote/'
LINKS = []
ARGUDB = []
ScreenI = []
_wrap = TextWrapper()

def utf8len(s):
    return len(s.encode('utf-8'))

def prepareMailInfo(mailMsg):
	home = expanduser('~')
	iOut = []
	iOut.append('python')
	iOut.append(home+'/.hmDict/simpleMail.py')
	iOut.append(mailMsg)
	return iOut

def repeatStr(string_to_expand, length):
	return (string_to_expand * ((length/len(string_to_expand))+1))[:length]

def parseInt(sin):
	m = re.search(r'^(\d+)[.,]?\d*?',str(sin))
	return int(m.groups()[-1]) if m and not callable(sin) else None

def getReleaseNoteDetail(tDetail):
	thisScreen = []
	resp = requests.get(tTarget)
	data = resp.text
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(data), parser)

	comments = tree.xpath('//comment()')
	for c in comments:
		p = c.getparent()
		p.remove(c)

	etree.strip_tags(tree,'p')
	etree.strip_tags(tree,'i')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')

	#mTitle = ''
	#titles = tree.xpath("//h1[@class='title']")

'''For programming'''
def paintRED(string,target):
	string = string.replace(target, clrTx(target,'RED'))
	return string

def doStuff(tTarget,id,comment_id):
	#print("enter doStuff")
	global ScreenI
	global stockdb
	global cursor
	updownSymbol = u'\u2197'
	num = id
	#cursor.execute(f"SELECT COMMENTID FROM SOI WHERE ID={num}")
	#my_rets = cursor.fetchone()
	#comment_id = my_rets[0]
	#print(f"comment id = {comment_id}")
	resp = requests.get(tTarget+str(num))
	data = resp.text
	#
	# print(data)
	parser = etree.HTMLParser(recover=True)
	tree = etree.parse(StringIO(data), parser)
	#etree.strip_tags(tree,'span')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')

	#print(repr(result))
	#print(paintRED(repr(result),'function(win)'))
    #print paintRED(result,'stkname')

	# current value
	#headLines = re.findall('<div class=".+?">(.+?)</div>',repr(result),re.DOTALL)
	#headLines = re.findall('<div class=".+?">(.+?)</div>',repr(result),re.DOTALL)
	titles = tree.xpath('//h1[@class="C($c-link-text) Fw(b) Fz(24px) Mend(8px)"]')
	contents = tree.xpath('//span[@class="Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"]')
	if len(contents) == 0:
		contents = tree.xpath('//span[@class="Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)"]')
		updownSymbol = u'\u2198'
	if len(contents) == 0:
		contents = tree.xpath('//span[@class="Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)"]')
		updownSymbol = u'\u2192'

	price = 0
	mytitle = 'NA'
	for content in contents:
		if content.text is not None:
			#print(content.get("value"))
			#print(content.text)
			price = content.text
			break
			
	for title in titles:
		if title.text is not None:
			mytitle = title.text
			break
                                       
	tread_nums = tree.xpath('//div[@class="D(f) Ai(fe) Mb(4px)"]/span')
	my_tread_num = "0"
	for tread_num in tread_nums:
		if tread_num.text is None:
			#print("text is none")
			for child in tread_num:
				#print(child.text)
				#print(child.tail)
				my_tread_num = child.tail
			#print(tread_num.tag)
			#print(tread_num.attrib)
			#print(tread_num.tail)
			#tread_nums.remove(tread_num)

	#diff = Decimal(price) - Decimal(my_price)
	#target_price = Decimal(Decimal(my_price)*Decimal('1.3'))
	ai_comment = " No comment"
	#print(f"my title={mytitle}")
	#ScreenI.append({'serial':num, 'title':mytitle, 'last':my_price, 'current':price, 'updownsymbol':updownSymbol,'diff':diff, 'updownvalue':my_tread_num})
	#print(f"INSERT OR REPLACE INTO SOI(ID, TITLE, COST, PRICE, UPDOWNSYMBOL, DIFF, TARGET_PRICE, AI, UPDOWNVALUE) values({str(num)},\
	#	'{str(mytitle)}','{str(my_price)}','{str(price)}','{str(updownSymbol)}','{str(diff)}','{str(target_price)}','{ai_comment}','{str(my_tread_num)}')")

	cursor.execute(f"UPDATE SOI SET TITLE='{str(mytitle)}', PRICE='{str(price)}', AI='{ai_comment}' WHERE COMMENTID='{str(comment_id)}';")
	stockdb.commit()
 
def setup_logging(level):
	global DB
	DB = logging.getLogger('benten') #replace
	DB.setLevel(level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tTarget
	global args

	parser = argparse.ArgumentParser(description='This benten_memo ( Benzaiten ) is a personal memo system for Taiwan stock market') #replace
	parser.add_argument('-v', '--verbose', dest='verbose', action = 'store_true', default=False, help='Verbose mode')
	parser.add_argument('query', nargs='*', default=None)
	parser.add_argument('-d', '--database', dest='database', action = 'store', default='/.benten_memo/benten_memo.db') #replace
	parser.add_argument('-q', '--sqlite3', dest='sql3db', action = 'store', default='/.benten_memo/benten_memo.db3') #replace
	parser.add_argument('-a', '--add', dest='add', action = 'store_true', default=False, help='add stock number you intent to say something')
	parser.add_argument('-r', '--read', dest='read', action = 'store_true', default=False, help='dump records')
	parser.add_argument('-k', '--kill', dest='kill', action = 'store_true', default=False, help='remove a stock from monitor list')
	parser.add_argument('-l', '--list', dest='listme', action = 'store_true', default=False, help='old interface, reserved')
	parser.add_argument('-u', '--update', dest='updateme', action = 'store_true', default=False, help='update')
	args = parser.parse_args()
	tTarget = ' '.join(args.query)
	log_level = logging.INFO
	if args.verbose:
		log_level = logging.DEBUG
	#if not tTarget:
	#	parser.print_help()
	#	exit()
	if args.read and args.kill:
		print("Flag conflict, some flag are exclusive")
		parser.print_help()
		exit()
	if not args.read and not args.kill and not args.add and not args.listme and not args.updateme:
		parser.print_help()
		exit()
	setup_logging(log_level)

def refreshDb():
	global ARGUDB
	global DB
	global stockdb
	global cursor
	ARGUDB = []
	home = expanduser('~')
	if os.path.isfile(home+args.database) is True:
		f = open(home+args.database,'r')
		if f is not None:
			for line in f :
				if line != '\n' and line[0] != '#':
					line = line.rstrip('\n')
					ARGUDB.append(line)
		f.close()
	else:
		DB.debug('override file is not exist')
	stockdb = sqlite3.connect(home+args.sql3db)
	cursor = stockdb.cursor()
	DB.info("sqlite3 databse connected")
	cursor.execute('''CREATE TABLE IF NOT EXISTS SOI
	(COMMENTID INTEGER PRIMARY KEY AUTOINCREMENT,
	ID INTEGER NOT NULL,
	TITLE TEXT,
	TIME TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')), 
	PRICE TEXT,
	COMMENT TEXT,
	AI TEXT
	);''')
	DB.info("table created or existed")
	stockdb.commit()

def	doDump():
	#for entry in ARGUDB:
	#	print(entry)
	global stockdb
	global cursor	
	global ScreenI
	ScreenI.clear()
	print("|"+clrTx("      TIME","CYAN")+"|"+clrTx("Serial","CYAN")+"|"+clrTx("    Name","CYAN")+"|"+clrTx("     Price","CYAN"))

	cursor.execute(f"SELECT * FROM SOI")
	for record in cursor.fetchall():
		#print(record)		
		ScreenI.append({'Time':record[3], 'Serial':record[1], 'Title':record[2], 'Price':record[4], 'Comment':record[5]})

	for item in ScreenI:
		target_str = f"|{item['Time']:>10}|{item['Serial']:>6}|{item['Title']:>8}|{Decimal(item['Price']):>8.2f}|{item['Comment']}"

def doDumpEx(num=0):
	global ScreenI
	global stockdb
	global cursor
	#for entry in ARGUDB:
	#	curr_idx+=1
	#	print(f"Handling {curr_idx}/{max_entrys}", end='\r')
	#	doStuff(staticStr,entry)
	cursor.execute(f"SELECT COMMENTID,ID FROM SOI")
	for rets in cursor.fetchall():
		doStuff(staticStr,rets[1],rets[0])
		
	#print("|"+clrTx("               TIME","CYAN")+"|"+clrTx("Serial","CYAN")+"|"+clrTx("    Name","CYAN")+"|"+clrTx(" Price","CYAN")+"|"+clrTx("MEMO","CYAN"))

	if num == 0:
		cursor.execute(f"SELECT * FROM SOI")
	else:
		cursor.execute(f"SELECT * FROM SOI WHERE ID = {num}")

	for record in cursor.fetchall():
		#print(record)		
		ScreenI.append("------------------------------------------------------------------")
		ScreenI.append(f"{record[3]}|{record[1]}|{record[2]}")
		ScreenI.append(f"{record[4]}|{record[5]}")
	
	for item in ScreenI:
		print(item)

def doWriteLn(msg):
	global DB
	global stockdb
	global cursor
	msgs = msg.split(":")
	if(len(msgs) !=2):
		print(clrTx("you need to input [stock_num]:[comment]",'YELLOW'))
	home = expanduser('~')
	cursor.execute(f"INSERT OR REPLACE INTO SOI(ID,COMMENT) values({msgs[0]},'{msgs[1]}')")
	stockdb.commit()

def doKillALn(number):
    index = ARGUDB.index(number)
    ARGUDB.pop(index)
    home = expanduser('~')
    f = open(home+args.database,'w')
    for entry in ARGUDB:
        f.write(entry+'\n')
    f.close()

def main():
	#doStuff(tTarget)
	global stockdb
	global cursor
	if args.read :
		if len(tTarget) == 0:
			id = 0
		else:
			id  = int(tTarget)
		doDumpEx(id)
	elif args.kill:
		doKillALn(tTarget)
	elif args.add:
		doWriteLn(tTarget)
	elif args.updateme:
		doDumpEx()
	stockdb.close()

if __name__ == '__main__':
	verify()
	refreshDb()
	main()
