import re
from lib.utils import *

"""
***************************************************************
CLASS NAME:

  Constant

DESCRIPTION:

	Object that repersents a constant declaration in the program
***************************************************************
"""
class Constant:
  """
  Function Name:

  	__init__

  Description:

  	Constructor for Constant

  Variables:

  	String  dataType  predicted data type of the constant
    String  name  name of the constant
    String  description  description of the constant
    Functions[]  usage  functions the constant is used in
    String  value  the value of the constant
    String  code  the plain text code of the constant declaration
  """
  def __init__(self):
    self._dataType = ""
    self._name = ""
    self._description = ""
    self._usage = []
    self._value = ""
    self._code = ""

  def setDataType(self, dataType):
     self._dataType = dataType

  def setName(self, name):
    self._name = name

  def setDescription(self, description):
    self._description = description

  def setValue(self, value):
    self._value = value

  def setCode(self, code):
    self._code = code

  def appendUsage(self, function):
    self._usage.append(function)

  def getDataType(self):
    return self._dataType

  def getName(self):
    return self._name

  def getDescription(self):
    return self._description

  def getValue(self):
    return self._value

  def getCode(self):
    return self._code

  def getUsage(self):
    return self._usage

  """
  Function Name:

    toString

  Description:

  	Prints out the Constant object to the command line
  """
  def toString(self):
    print("Name: " + self._name)
    print("Value: " + self._value)
    print("Type: " + self._dataType)
    print("Description: " + self._description)
    print("Usage: ")
    for function in self._usage:
        print(function.name)
    print()

  #Property Calls
  dataType = property(getDataType, setDataType)
  name = property(getName, setName)
  description = property(getDescription, setDescription)
  value = property(getValue, setValue)
  code = property(getCode, setCode)
  usage = property(getUsage)



"""
  Function Name:

  	isConstantDeclaration

  Description:

  	Checks if the given line is a constant declaration

  Parameters:

  	String  line  the line to check

  Returns:

  	boolean  isConstant  returns True if line contains constant declaration, returns False otherwise
"""
def isConstantDeclaration(line):
    if re.search("^.*#define", line):
        return True
    return False


"""
Function Name:

    constantsIndexHTML

Description:

  	Creates the HTML for the constants index page
"""
def constantsIndexHTML(output_directory, state):

    constants = state["constants"]

    fileHTML = htmlHead("Constant Index", "..")
    fileHTML += "\n<body>"
    fileHTML += htmlNavBar("Constants")
    fileHTML += "\n<main>"
    fileHTML += "\n<div class=\"header\">"
    fileHTML += "\n<a id=\"whitespace\"></a>"
    fileHTML += "\n<h2 title=\"Constants\" class=\"title\">Constants</h2>"
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


    if len(constants) >= 1:
        fileHTML += "\n<table class=\"memberSummary\">"
        fileHTML += "\n<caption><span>Index</span><span class=\"tabEnd\">&nbsp;</span></caption>"
        fileHTML += "\n<tr>"
        fileHTML += "\n<th class=\"colFirst\" scope=\"col\">Name</th>"
        fileHTML += "\n<th class=\"colSecond\" scope=\"col\">Value</th>"
        fileHTML += "\n<th class=\"colLast\" scope=\"col\">Function Usage Count</th>"
        fileHTML += "\n<th class=\"colLast\" scope=\"col\">Assumed Data Type</th>"
        fileHTML += "</tr>"
        fileHTML += "<tr id=\"i0\" class=\"altColor\">"


        for constant in constants:
            fileHTML += "\n<tr id=\"i0\" class=\"altColor\">"
            fileHTML += "\n<td class=\"colFirst\"><code><a href=\"../constants/" + constant.name + ".html\">" + constant.name + "</a></code></td>"
            fileHTML += "\n<th class=\"colSecond\" scope=\"row\"><code>" + constant.value + "</code></th>"
            fileHTML += "\n<th class=\"colSecond\" scope=\"row\"><code>" + str(len(constant.usage)) + "</code></th>"
            fileHTML += "\n<td class=\"colLast\">"
            fileHTML += "\n<div class=\"block\">" + constant.dataType + "</div>"
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

    htmlFile = open(output_directory + "/indexes/constants.html", "w")
    htmlFile.write(fileHTML)
    htmlFile.close()


"""
Function Name:

    constantToHTML

Description:

  	Converts a Constant object into a HTML file

Parameters:

    Constant  constant  the constant to turn into a HTML file

"""
def constantToHTML(output_directory, constant):
    fileHTML = htmlHead(constant.name, "..")
    fileHTML += "\n<body>"
    fileHTML += htmlNavBar("")
    fileHTML += "\n<main>"
    fileHTML += "\n<div class=\"header\">"
    fileHTML += "\n<a id=\"whitespace\"></a>"
    fileHTML += "\n<h2 title=\"Constant Name\" class=\"title\">" + constant.name + "</h2>"
    fileHTML += "\n</div>"
    fileHTML += "\n<div class=\"contentContainer\">"
    fileHTML += "\n<div class=\"description\">"
    fileHTML += "\n</ul>"
    fileHTML += "\n</div>"
    fileHTML += htmlConstantSummary(constant)
    fileHTML += htmlConstantReferences(constant)
    fileHTML += htmlConstantBody(constant)
    fileHTML += "\n</div>"
    fileHTML += "\n</main>"
    fileHTML += "\n</body>"
    fileHTML += "\n</html>"

    htmlFile = open(output_directory + "/constants/" + constant.name + ".html", "w")
    htmlFile.write(fileHTML)
    htmlFile.close()


"""
    Function Name:

        htmlConstantBody

    Description:

  	    Returns a String contaning the the constant body portion of the constant page in HTML

    Parameter:

        Constant  in_constant  the constant to create the constant body in HTML for

    Returns:

        String  htmlString  the html file string
"""
def htmlConstantBody(in_constant):
    htmlString = ""
    htmlString += "\n<div class=\"details\">"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    htmlString += "\n<section>"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    
    htmlString += "\n<h3>Constant Declaration</h3>"
    
    htmlString += "\n<ul class=\"blockListLast\">"
    htmlString += "\n<li class=\"blockList\">"
    htmlString += "\n<h4>" + in_constant.name + "</h4>"
    codeString = in_constant.code
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

    htmlString += "\n<pre class=\"methodSignature\">" + buildCodeString + "</pre>"
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

        htmlConstantReferences

    Description:

  	    Returns a String contaning the references of a constant file in HTML

    Parameter:

        Constant  in_constant  the constant to create the HTML references section for

    Returns:

        String  htmlString  the html file string
"""
def htmlConstantReferences(in_constant):
    htmlString = ""

    if len(in_constant.usage) >= 1:
        htmlString += "\n<div class=\"details\">"
        htmlString += "\n<ul class=\"blockList\">"
        htmlString += "\n<section>"
        htmlString += "\n<ul class=\"blockList\">"
        htmlString += "\n<li class=\"blockList\">"
        
        htmlString += "\n<h3>Usage</h3>"
        
        htmlString += "\n<ul class=\"blockList\">"

        htmlString += "\n<li class=\"blockList\">"
        htmlString += "\n<h4>Usage in Functions</h4>"

        buildString = ""

        firstFlag = True

        for function in in_constant.usage:
            if firstFlag:
                buildString += "<a href=\"../functions/" + function.name + ".html\">" + function.name + "</a>"
                firstFlag = False
            else:
                buildString += ", <a href=\"../functions/" + function.name + ".html\">" + function.name + "</a>"

        htmlString += "\n<code>" + buildString + "</code>"

        htmlString += "\n</li>"

        htmlString += "\n</section>"

        htmlString += "\n</li>"
        htmlString += "\n</ul>"
        htmlString += "\n</ul>"
        htmlString += "\n</ul>"

        htmlString += "\n</div>"

    return htmlString

"""
    Function Name:

        htmlConstantSummary

    Description:

  	    Returns a String contaning the constant summary of a constant page in HTML

    Parameter:

        Constant  in_constant  the constant to turn into a HTML constat summary

    Returns:

        String  htmlString  the html file string
"""
def htmlConstantSummary(in_constant):

    htmlString = ""

    htmlString += "\n<div class=\"details\">"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<section>"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    
    htmlString += "\n<h3>Constant Summary</h3>"
    

    htmlString += "\n<ul v class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    htmlString += "\n<h4>Description</h4>"
    htmlString += "\n<div class=\"block\">" + in_constant.description.replace("\n", "<br \/>") + "</div>"
    htmlString += "\n</li>"

    
    htmlString += "\n<table class=\"memberSummary\">"
    htmlString += "<caption><span>Fields</span><span class=\"tabEnd\"> &nbsp;</span></caption>"
    htmlString += "\n<tr>"
    htmlString += "\n<th class=\"colFirst\" scope=\"col\">Data Type</th>"
    htmlString += "\n<th class=\"colSecond\" scope=\"col\">Name</th>"
    htmlString += "\n<th class=\"colLast\" scope=\"col\">Value</th>"
    htmlString += "\n</tr>"
    htmlString += "\n<tr id=\"i0\" class=\"altColor\">"
    htmlString += "\n<td class=\"colFirst\"><code>" + in_constant.dataType + "</code></td>"
    htmlString += "\n<th class=\"colSecond\" scope=\"row\"><code>" + in_constant.name + "</code></th>"
    htmlString += "\n<td class=\"colLast\">"
    htmlString += "\n<div class=\"block\">" + in_constant.value + "</div>"
    htmlString += "\n</td>"
    htmlString += "\n</tr>"
    htmlString += "\n</table>"

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

    isConstantDeclaration

Description:

    Checks if a line of code is a constant declaration.

Returns:

    Boolean  True if the line is a constant declaration, False otherwise.
"""
def isConstantDeclaration(line):
    if re.search("^.*#define", line):
        return True
    return False