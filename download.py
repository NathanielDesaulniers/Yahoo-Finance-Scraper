#!/usr/local/bin/python2.7
import os

def ReadFile(i):
	with open(i) as f:
	    lines = f.read().splitlines()
	return lines

def AppendFile(path, text):
	with open(path, "a") as f:
		f.write(text)

def ValidateFile(filename):
	if not os.path.isfile(filename):
		return False
	lines = ReadFile(filename)
	for line in lines:
		if "message:unknown error has happened" in line.lower():
			return False
	return True

#wget "url" -O file || rm -f file
#http://superuser.com/questions/166387/wget-o-writes-empty-files-on-failure
#http://chartapi.finance.yahoo.com/instrument/1.0/KO/chartdata;type=quote;range=1d/csv
def DownloadFile(symbol, extension, days):
	filename = symbol + extension
	os.system("wget --tries=10 --user-agent=\"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3\" -O " + filename + " \"" + "http://chartapi.finance.yahoo.com/instrument/1.0/" + symbol + "/chartdata;type=quote;range=" + str(days) + "d/csv" + "\"" + " || rm -f " + filename)

def AttemptDownload(symbol, extension, days, attempts):
	if symbol == "":
		return True
	for x in range(0, attempts):
		DownloadFile(symbol, extension, days)
		if ValidateFile(symbol + extension):
			return True
	return False

def DownloadStockFile(filename):
	LogFile = "Log.dat"
	Attempts = 10
	Days = 1
	AppendFile(LogFile, "Started downloading " + filename + "\n")
	lines = ReadFile(filename)
	for symbol in lines:
		if not AttemptDownload(symbol.strip(), ".csv", Days, Attempts):
			AppendFile("Log.dat", "Input File: " + filename + " Failed to download: " + symbol + "\n")
	AppendFile(LogFile, "Finished downloading " + filename + "\n")

def CleanUp():
	os.system("tar -jcf $(date +%Y%m%d).zip *.csv *.dat")
	os.system("rm *.csv *.dat")
	#tar cfz $(date +%Y-%m-%d).zip *.csv
	#rm *.csv


#DownloadStockFile("TEMP.txt")
DownloadStockFile("TSX.txt")
DownloadStockFile("NYSE.txt")
DownloadStockFile("NASDAQ.txt")


CleanUp()




