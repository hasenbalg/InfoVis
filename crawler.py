import urllib2
import re
filename = 'anatomie_book.txt'
target_file = open(filename, 'w')

base_url = 'http://www.bartleby.com/107/'
for i in range(1,292):
    url = base_url + str(i) + '.html'
    print(url)
    response = urllib2.urlopen(url).read()
    # print(response)
    text = re.sub(r"<HTML>[\s\S]+?<!-- BEGIN CHAPTER -->", "", response)#remove start of page
    text = re.sub(r"<!-- END CHAPTER -->[\s\S]+?</HTML>", "", text)#remove end of page
    text = re.sub(r"<[\s\S]+?>", "", text)#remove tags
    text = re.sub(r"&.+?;", "", text)#remove &nbsp;
    # print(text)
    target_file.write(text)
target_file.close()
