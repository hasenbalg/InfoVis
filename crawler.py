import urllib2
import re
import datetime
import sys

filename = str(datetime.datetime.now()) + '.txt'
print( "arguments: filename url")
if len(sys.argv)>=2:
    filename = sys.argv[1]
target_file = open(filename, 'w')

if len(sys.argv)>=3:
    base_url = sys.argv[2]

    url = base_url
    print(url)
    response = urllib2.urlopen(url).read()
    # print(response)
    text = re.sub(r"<HTML>[\s\S]+?<!-- BEGIN CHAPTERTITLE -->", "", response)#remove start of page
    text = re.sub(r"<!-- END CHAPTERTITLE -->[\s\S]+?</HTML>", "", text)#remove end of page

    text1 = re.sub(r"<HTML>[\s\S]+?<!-- BEGIN CHAPTER -->", "", response)#remove start of page
    text1 = re.sub(r"<!-- END CHAPTER -->[\s\S]+?</HTML>", "", text1)#remove end of page
    #text = re.sub(r"<[\s\S]+?>", "", text)#remove tags
    #text = re.sub(r"&.+?;", "", text)#remove &nbsp;
    # print(text)
    target_file.write(text + text1)
    target_file.close()
else:
    base_url = 'http://www.bartleby.com/107/'

    for i in range(17,68):
        url = base_url + str(i) + '.html'
        print(url)
        response = urllib2.urlopen(url).read()
        # print(response)
        text = re.sub(r"<HTML>[\s\S]+?<!-- BEGIN CHAPTERTITLE -->", "", response)#remove start of page
        text = re.sub(r"<!-- END CHAPTERTITLE -->[\s\S]+?</HTML>", "", text)#remove end of page

        text1 = re.sub(r"<HTML>[\s\S]+?<!-- BEGIN CHAPTER -->", "", response)#remove start of page
        text1 = re.sub(r"<!-- END CHAPTER -->[\s\S]+?</HTML>", "", text1)#remove end of page
        #text = re.sub(r"<[\s\S]+?>", "", text)#remove tags
        #text = re.sub(r"&.+?;", "", text)#remove &nbsp;
        # print(text)
        target_file.write(text + text1)
    target_file.close()
