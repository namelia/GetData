import sys
import errno
import os
import datetime
import codecs
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

folderDirectory ="/Users/nancyamelia/Desktop/FYP/Data"


bankKeywords= {
              'HSBC' : ' "HSBC" OR "HSBC_UK" OR "HSBCUKBusiness" OR "HSBC_UK_Careers" OR "#hsbc #bank" ',
              'BNPParibas' : ' "BNP Paribas" OR "BNPParibas" OR "BNPPcampus" OR "BNPP_Wealth" OR "BNPPFBelgie" OR "BNPPAM_COM" OR "#bnp #paribas" OR "#bnp #bank" ',
              'DeutscheBank' : ' "Deutsche Bank" OR "DeutscheBank" OR "careersDB" OR "#deutsche #bank" ',
              'Santander' : ' "Santander" OR "Santanderuk" OR "SantanderUKHelp" OR "SantanderAcc" OR "SantanderBank" ',
              'Barclays': ' "Barclays" OR "Barclay" OR "BarclaysUK" OR "BarclaysUKHelp" OR "Barclaysuknews" OR "BarclaysBusiness" OR "Barclays_cship" OR "BarclaysJobsUK"',
              'Lloyds' :  ' "Lloyds" OR "Lloydsbank" OR "Lloydsuk" OR "Lloydsbanks" OR "AskLloydsBank" ',
              'RBS' :  ' "RBS Bank" OR "@RBS" OR "Royal Bank of Scotland" OR "RBSBanks" OR "RBSBank" OR "RBS_UK" OR "RBS_Help" ',
              'UBS' : ' "UBS" OR "UBS banks" OR "UBS bank" OR "Union Bank of Switzerland" OR "UBScareers" OR "UBS_UK" OR "UBSBanks" OR "UBSBank"',
              'CreditSuisse' : ' "creditsuisse" OR "credit suisse" OR "creditsuissebank" OR "credit suisse banks" OR "credit suisse bank" OR "careersatcs"',
              'StandardChartered' : ' "standard chartered" OR "stanChart" OR "standardchartered" OR "standardcharteredbank" OR "standardcharteredbanks" OR "StanChartHelp" OR "StanChartBank" OR "StanChartBanks" '
              }

now = datetime.datetime.now()
creationDate = now.strftime("%Y%m%d")

def createDirFile(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def main():
	sinceDate = "2017-12-11"
	#Remember to writdired=e the until Date + 1 day
	untilDate = "2017-12-18"
	for bankName in bankKeywords:
		try:
			print "Executing bank " + bankName
			fileName = folderDirectory + "/%s-%s/%s.csv" % (sinceDate,untilDate, bankName)
			createDirFile(fileName)
			tweetCriteria = got.manager.TweetCriteria().setSince(sinceDate).setUntil(untilDate).setQuerySearch(bankKeywords[bankName])
			tweet = got.manager.TweetManager.getTweets(tweetCriteria)
			print "Succesfully gathered tweets..."
			outputFile = codecs.open(fileName, "w+", "utf-8")
			for t in tweet:
				outputFile.write(('\n%s,%s,%d,%d,"%s",%s,%s,%s,"%s",%s' % ( t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions,t.hashtags, t.id, t.permalink)))
			outputFile.flush();
			print('More %d saved on file...\n' % len(tweet))
		except Exception :
			print "Unsuccessful, please try again."


if __name__ == '__main__':
	main()
