import sys
import re

"""
  Function Name:

  	exitMessage

  Description:

  	Prints specified message then exits program with specified exit code

  Parameters:

  	String  message  the message to print out
    int  code  the exit code
"""
def exitMessage(message, code):
  print(message)
  sys.exit(code)

"""
    Function Name:

        htmlNavBar

    Description:

  	    Returns a String contaning the navigation bar portion of the HTML file

    Parameter:

        String  highlighted_link  the link to highlight

    Returns:

        String  htmlString  the html file string
"""
def htmlNavBar(highlighted_link):
    htmlString = ""
    htmlString += "\n<header>"
    htmlString += "\n<nav>"
    htmlString += "<div class=\"topNav\">"
    htmlString += "<a id=\"navbar.top\"></a>"
    htmlString += "\n<ul class=\"navList\" title=\"Navigation\">"

    if highlighted_link != "Home":
        htmlString += "\n<li><a href=\"../home.html\">Home</a></li>"
    else:
        htmlString += "\n<li><a href=\"../home.html\" class=\"navBarCell1Rev\">Home</a></li>"

    if highlighted_link != "Functions":
        htmlString += "\n<li><a href=\"../indexes/functions.html\">Functions</a></li>"
    else:
        htmlString += "\n<li class=\"navBarCell1Rev\">Functions</li>"

    if highlighted_link != "Variables":
        htmlString += "\n<li><a href=\"../indexes/variables.html\">Variables</a></li>"
    else:
        htmlString += "\n<li class=\"navBarCell1Rev\">Variables</li>"

    if highlighted_link != "Constants":
        htmlString += "\n<li><a href=\"../indexes/constants.html\">Constants</a></li>"
    else:
        htmlString += "\n<li class=\"navBarCell1Rev\">Constants</li>"

    if highlighted_link != "Libraries":
        htmlString += "\n<li><a href=\"../indexes/libraries.html\">Libraries</a></li>"
    else:
        htmlString += "\n<li class=\"navBarCell1Rev\">Libraries</li>"

    htmlString += "\n</header>"

    return htmlString

"""
    Function Name:

        htmlHead

    Description:

  	    Returns a String contaning the start of a HTML file

    Parameter:

        String  title  title to put in the header
        String  path  the path to relate the stylesheet to

    Returns:

        String  htmlString  the html file string
"""
def htmlHead(title, path):
    htmlString = ""
    htmlString += "<!DOCTYPE HTML>"
    htmlString += "\n<html lang=\"en\">"
    htmlString += "\n<head>"
    htmlString += "\n<title>" + title + "</title>"
    htmlString += "\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">"
    htmlString += "\n<link rel=\"stylesheet\" type=\"text/css\" href=\"" + path + "\\stylesheets\stylesheet.css\" title=\"Style\">"
    htmlString += "\n<head>"
    return htmlString

"""
    Function Name:

      searchForChar

    Description:

      Searches left or right in a given String from a given index character by character
      to find a character or the absence of a character, returning the index the feature is found at

    Parameters:

      String  string  the string to search for given character
      char  char  the char to search for the presence or absence of
      int  increment  the increment to change each time (1 to search left by 1, -1 to search right by 1)
      int  startIndex  the index to start from while searching
      bool  presence  if True the presence of the character will be searched for, if False the absence of the character will be searched for

    Returns:

      int  index  the index the request is found at in the given String, if there is an error or the character is not found -1
"""
def searchForChar(string, char, increment, startIndex, presence):
    if startIndex < 0 or startIndex >= len(string):
        return -1
    i = 0
    if presence:
        while startIndex+(i*increment) >= 0 and startIndex+(i*increment) < len(string):
            if string[startIndex+(i*increment)] == char:
                return startIndex+(i*increment)
            i += 1
    else:
    	while startIndex+(i*increment) >= 0 and startIndex+(i*increment) < len(string):
            if string[startIndex+(i*increment)] != char:
                return startIndex+(i*increment)
            i += 1
    return -1

"""
  Function Name:

  	skipBlankLines

  Description:

  	Skips until the next non-blank line and returns it.
      
  Returns:

    String  line  the next line found that is not blank in the file
"""
def skipBlankLines(file):
    while True:
        line = file.readline()
        if re.search("(\w)", line) or re.search("(\*\/)", line):
            return line
    return ""

"""
  Function Name:

  	unformedSyntaxHandler

  Description:

  	Wrapper for exitMessage with an unformed syntax message including the offending line, exiting with code 1
"""
def unformedSyntaxHandler(line):
    exitMessage("Unformed syntax, please check line: " + str(line), 1)


"""
  Function Name:

  	findN

  Description:

  	Returns the index of the nth substring of input

  Parameters:

  	String  s  the string to search
    String  substr  the substring to search for
    int  n  the nth occurrence to search for
"""
def findN(s, substr, n):
    if n <= s.count(substr) and n > -1:
        if n == 1:
            return s.find(substr)
        else:
            return s.find(substr, findN(s, substr, n-1)+1)
    else:
        return -1