#import libraries
#import logging
import re
import time
from robobrowser import RoboBrowser

def RemoveTags(originalText):
	newText = re.search(r'M">(.+)</a>', originalText)
	return newText.group(1)

def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext







def GetPostDate(spanTag):
	tagPattern = re.compile('<.+>')
	cleanedSpanTag = str(re.sub(tagPattern, '', spanTag))

	regexGroup = re.search('(\w\w\w\s\d+\s\d\d\d\d),\s(\d\d:\d\d\s\w\w)',cleanedSpanTag)
	postdatetime = str(regexGroup.group())
	postdate = str(regexGroup.group(1))
	posttime = str(regexGroup.group(2))

	return postdatetime

def CleanPost(p):
	print(p)
	


def ParseThread(threadID):
	#Will need to put in a control here to ensure the threadID is valid
	threadURL = 'http://thedark.jcink.net/index.php?showtopic=' + str(threadID)
	print("URL is: " + threadURL)

	f = open("post.txt", "a")

	br = RoboBrowser()
	br.open(threadURL)

	#Fill out age form
	forms = br.get_forms()
	form = forms[0]
	form['day'] = '12'
	form['month'] = 'January'
	form['year'] = '1988'
	br.submit_form(form)

	#Click on the redirection link after verifying age
	link = br.find('a')
	br.follow_link(link)


	soup = br.parsed

	#Topic Title
	topic_title = soup.find('span', attrs={'class': 'topic-title'}).string
	print(topic_title)
	f.write(topic_title + "\n\n")

	posts = soup.find_all('span', attrs={'class': re.compile('post-normal.*')})

	count = 1

	for p in posts:
		#Post Number
		f.write("Post Number: " + str(count) + "\n")
		print("Post Number: " + str(count))

		#Post Date
		span_tag = p.find('span', attrs={'class': 'postdetails'})
		postdatetime = GetPostDate(str(span_tag.contents))
		f.write(postdatetime)
		print(postdatetime)

		#Post Author
		span_normal_tag = p.find('span', attrs={'class': 'normalname'})
		f.write(" by " + span_normal_tag.a.span.string + "\n\n")
		print(span_normal_tag.a.span.string)


		#Write the post
		postDiv = p.find('div', attrs={'class': 'postcolor'})
		print(postDiv.contents)
		print("\n")
		f.write(postDiv.contents)
		f.write("\n\n")


		count = count+1






def GatherCharacters(character_page):
	br = RoboBrowser()
	br.open(character_page)

	#Fill out age form
	forms = br.get_forms()
	form = forms[0]
	form['day'] = '12'
	form['month'] = 'January'
	form['year'] = '1988'
	br.submit_form(form)

	#Click on the redirection link after verifying age
	link = br.find('a')
	br.follow_link(link)


	soup = br.parsed

	#Get the name of the page
	species = re.search(r'\s(\w+)$', soup.title.string).group(1)
	print("------------")
	print("  " + species)
	print("------------")

	#Add character names to a list after cleaning up the lines
	characterNames = []

	for charName in soup.find_all('div', attrs={'class': 'tname'}):
		tempCharName = RemoveTags(str(charName))
		characterNames.append(tempCharName)
		print(tempCharName)




def PrintMenu(menuType):
	if menuType=="mainmenu":
		print("****************************")
		print("*       Menu Options       *")
		print("****************************")
		print("1 - Characters")
		print("2 - Post")
		print("100 - Exit")
	
	elif menuType=="charactermenu":
		print("****************************")
		print("*     Character Options    *")
		print("****************************")
		print("1 - Human")
		print("2 - Lamia")
		print("100 - Exit")
	else:
		print("Error: Requested menu type doesn't exist in PrintMenu function.")


def CharacterMenu():
	lamia_page = 'http://thedark.jcink.net/index.php?showforum=96'
	human_page = 'http://thedark.jcink.net/index.php?showforum=92'

	PrintMenu("charactermenu")
	characterChoice = int(input('Selection: '))

	while characterChoice > 0:
		if characterChoice==1:
			print("Chose Human")
			GatherCharacters(human_page)
			characterChoice = -1
		elif characterChoice==2:
			print("Chose Lamia")
			GatherCharacters(lamia_page)
			characterChoice = -1
		elif characterChoice==100:
			print("Exiting.")
			characterChoice=-1
		else:
			print('Try again.')
			characterChoice = int(input('Selection: '))


def main():
	#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

	PrintMenu("mainmenu")
	userChoice = int(input('Selection: '))

	while userChoice>0:
		if userChoice==1:
			CharacterMenu()
			userChoice=-1
		elif userChoice==2:
			threadID = int(input('Input thread ID:'))
			ParseThread(threadID)
			userChoice=-1
		elif userChoice==100:
			print("Exiting...")
			userChoice=-1
		else:
			print("Try again.")
			userChoice = input('Selection: ')



if __name__ == "__main__":
	main()