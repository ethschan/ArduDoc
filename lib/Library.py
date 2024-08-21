import re
from lib.utils import *

"""
***************************************************************
CLASS NAME:

    Library

DESCRIPTION:

    Object that repersents a library import statement
***************************************************************
"""
class Library:
  """
  Function Name:

    __init__

  Description:

    Constructor for Library

  Variables:

  	String  name  the name of the imported library
    String  description  description of the usage of the library in the program
    String  code  the plain text code of the library import statement
  """
  def __init__(self):
    self._name = ""
    self._description = ""
    self._code = ""

  def setName(self, name):
    self._name = name

  def setDescription(self, description):
     self._description = description

  def setCode(self, code):
      self._code = code

  def getName(self):
    return self._name

  def getDescription(self):
     return self._description

  def getCode(self):
      return self._code

  """
  Function Name:

    toString

  Description:

    Prints out the Library object to the command line
  """
  def toString(self):
      print("Name: " + self._name)
      print("Description: " + self._description)
      print("Code: " + self._code)
      print()

  #Property Calls
  name = property(getName, setName)
  description = property(getDescription, setDescription)
  code = property(getCode, setCode)

"""
  Function Name:

  	isLibraryImport

  Description:

  	Checks if the given line is a library import statement

  Parameters:

  	String  line  the line to check

  Returns:

  	boolean  isLibraryImport  returns True if line contains a library import statement, returns False otherwise
"""
def isLibraryImport(line):
    if re.search("^.*#include", line):
        return True
    return False

"""
Function Name:

    librariesIndexHTML

Description:

  	Creates the HTML for the libraries index page
"""
def librariesIndexHTML(output_directory, state):

    libraries = state["libraries"]

    fileHTML = htmlHead("Libraries Index", "..")
    fileHTML += "\n<body>"
    fileHTML += htmlNavBar("Libraries")
    fileHTML += "\n<main>"
    fileHTML += "\n<div class=\"header\">"
    fileHTML += "\n<a id=\"whitespace\"></a>"
    fileHTML += "\n<h2 title=\"Libraries\" class=\"title\">Libraries</h2>"
    fileHTML += "\n</div>"
    fileHTML += "\n<div class=\"contentContainer\">"
    fileHTML += "\n<div class=\"description\">"
    fileHTML += "\n</ul>"
    fileHTML += "\n</div>"
    fileHTML += "\n<div class=\"details\">"
    fileHTML += "\n<ul class=\"blockList\">"
    fileHTML += "\n<section>"
    fileHTML += "\n<ul class=\"blockList\">"
    fileHTML += "\n<li class=\"blockList\">"

    if len(libraries) >= 1:
        fileHTML += "\n<table class=\"memberSummary\">"
        fileHTML += "\n<caption><span>Index</span><span class=\"tabEnd\">&nbsp;</span></caption>"
        fileHTML += "\n<tr>"
        fileHTML += "\n<th class=\"colFirst\" scope=\"col\">Name</th>"
        fileHTML += "\n<th class=\"colLast\" scope=\"col\">Description</th>"
        fileHTML += "</tr>"
        fileHTML += "<tr id=\"i0\" class=\"altColor\">"


        for library in libraries:
            fileHTML += "\n<tr id=\"i0\" class=\"altColor\">"
            fileHTML += "\n<td class=\"colFirst\"><code><a href=\"../libraries/" + library.name.replace(">", "").replace("<", "") + ".html\">" + library.name.replace(">", "").replace("<", "") + "</a></code></td>"
            fileHTML += "\n<td class=\"colLast\">"
            fileHTML += "\n<div class=\"block\">" + library.description.replace("\n", "<br \/>") + "</div>"
            fileHTML += "\n</td>"
            fileHTML += "\n</tr>"

        fileHTML += "\n</table>"

    fileHTML += "\n</section>"
    fileHTML += "\n</li>"
    fileHTML += "\n</ul>"
    fileHTML += "\n</li>"
    fileHTML += "\n</ul>"
    fileHTML += "\n</ul>"
    fileHTML += "\n</div>"

    fileHTML += "\n</div>"
    fileHTML += "\n</main>"
    fileHTML += "\n</body>"
    fileHTML += "\n</html>"

    htmlFile = open(output_directory + "/indexes/libraries.html", "w")
    htmlFile.write(fileHTML)
    htmlFile.close()


"""
Function Name:

    libraryToHTML

Description:

  	Converts a Library object into a HTML file

Parameters:

    Library  library  the library to turn into a HTML file

"""
def libraryToHTML(output_directory, library):
    fileHTML = htmlHead(library.name, "..")
    fileHTML += "\n<body>"
    fileHTML += htmlNavBar("")
    fileHTML += "\n<main>"
    fileHTML += "\n<div class=\"header\">"
    fileHTML += "\n<a id=\"whitespace\"></a>"
    fileHTML += "\n<h2 title=\"Library Name\" class=\"title\">" + library.name.replace(">", "&gt;").replace("<", "&lt;") + "</h2>"
    fileHTML += "\n</div>"
    fileHTML += "\n<div class=\"contentContainer\">"
    fileHTML += "\n<div class=\"description\">"
    fileHTML += "\n</ul>"
    fileHTML += "\n</div>"
    fileHTML += htmlLibrarySummary(library)
    fileHTML += htmlLibraryBody(library)
    fileHTML += "\n</div>"
    fileHTML += "\n</main>"
    fileHTML += "\n</body>"
    fileHTML += "\n</html>"

    htmlFile = open(output_directory + "/libraries/" + library.name.replace(">", "").replace("<", "") + ".html", "w")
    htmlFile.write(fileHTML)
    htmlFile.close()


"""
    Function Name:

        htmlLibraryBody

    Description:

  	    Returns a String contaning the the library body portion of the library page in HTML

    Parameter:

        Library  in_library  the library to create the library body in HTML for

    Returns:

        String  htmlString  the html file string
"""
def htmlLibraryBody(in_library):
    htmlString = ""
    htmlString += "\n<div class=\"details\">"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    htmlString += "\n<section>"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    
    htmlString += "\n<h3>Library Import Statement</h3>"
    
    htmlString += "\n<ul class=\"blockListLast\">"
    htmlString += "\n<li class=\"blockList\">"
    htmlString += "\n<h4>" + in_library.name + "</h4>"
    codeString = in_library.code
    newLineFlag = False
    buildCodeString = ""
    for letter in codeString:
        if letter == "\n":
            newLineFlag = True
            buildCodeString += "<br \/>"
        elif letter == " " and newLineFlag:
            buildCodeString += "&nbsp;&nbsp;"
        else:
            newLineFlag = False
            buildCodeString += letter

    htmlString += "\n<pre class=\"methodSignature\">" + buildCodeString.replace(">", "&gt;").replace("<", "&lt;") + "</pre>"
    htmlString += "\n</li>"
    htmlString += "\n</ul>"
    htmlString += "\n</li>"
    htmlString += "\n</ul>"
    htmlString += "\n</section>"
    htmlString += "\n</li>"
    htmlString += "\n</ul>"
    htmlString += "\n</div>"

    return htmlString

"""
    Function Name:

        htmlLibrarySummary

    Description:

  	    Returns a String contaning a HTML library summary

    Parameter:

        Library  in_library  the library to turn into a HTML library summary

    Returns:

        String  htmlString  the html file string
"""
def htmlLibrarySummary(in_library):

    htmlString = ""

    htmlString += "\n<div class=\"details\">"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<section>"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    
    htmlString += "\n<h3>Library Summary</h3>"
    

    htmlString += "\n<ul v class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    htmlString += "\n<h4>Description</h4>"
    htmlString += "\n<div class=\"block\">" + in_library.description.replace("\n", "<br \/>") + "</div>"
    htmlString += "\n</li>"

    htmlString += "\n</section>"
    htmlString += "\n</li>"
    htmlString += "\n</ul>"
    htmlString += "\n</li>"
    htmlString += "\n</ul>"
    htmlString += "\n</ul>"
    htmlString += "\n</div>"

    return htmlString

"""
Function Name:

    isLibraryImport

Description:

    Checks if a line of code is a library import.

Returns:

    Boolean  True if the line is a library import, False otherwise.
"""
def isLibraryImport(line):
    if re.search("^.*#include", line):
        return True
    return False
