import re
from lib.utils import *

"""
***************************************************************
CLASS NAME:

  Variable

DESCRIPTION:

  Object that repersents a global variable declaration in the program
***************************************************************
"""
class Variable:
  """
  Function Name:

  	__init__

  Description:

  	Constructor for Variable

  Variables:

  	String  dataType  type of the variable
    String  name  name of the variable
    String  description  description of the variable
    String  inital_value  the inital value set to the variable
    Functions[]  usage  functions the variable is used in
    int  pointer_depth  the pointer depth of the variable
    String  code  the plain text code of the variable declaration
  """
  def __init__(self):
    self._dataType = ""
    self._name = ""
    self._description = ""
    self._usage = []
    self._inital_value = "null"
    self._pointer_depth = 0
    self._code = ""

  def setDataType(self, dataType):
     self._dataType = dataType

  def setName(self, name):
    self._name = name

  def setDescription(self, description):
    self._description = description

  def setInitalValue(self, inital_value):
    self._inital_value = inital_value

  def setPointerDepth(self, pointer_depth):
    self._pointer_depth = pointer_depth

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

  def getUsage(self):
    return self._usage

  def getInitalValue(self):
    return self._inital_value

  def getPointerDepth(self):
    return self._pointer_depth

  def getCode(self):
    return self._code

  """
  Function Name:

    toString

  Description:

  	Prints out the current instance of a Variable object to the command line
  """
  def toString(self):
      print("Name: " + self._name)
      print("Inital Value: " + self._inital_value)
      print("Type: " + self._dataType)
      print("Description: " + self._description)
      print("Pointer depth: " + str(self._pointer_depth))
      print("Used in:")
      for function in self._usage:
          print(function.name)
      print()

  #Property Calls
  dataType = property(getDataType, setDataType)
  name = property(getName, setName)
  description = property(getDescription, setDescription)
  usage = property(getUsage)
  inital_value = property(getInitalValue, setInitalValue)
  pointer_depth = property(getPointerDepth, setPointerDepth)
  code = property(getCode, setCode)


"""
  Function Name:

  	isVariableDeclaration

  Description:

  	Checks if the given line is a variable declaration

  Parameters:

  	String  line  the line to check

  Returns:

  	boolean  isVariable  returns True if line contains variable declaration, returns False otherwise
"""
def isVariableDeclaration(line):
    variableDeclarationTypes = ["double", "int", "bool", "float", "char", "long", "unsigned", "void", "string", "File", "short", "SdVolume", "Sd2Card", "SdFile"]
    for dataType in variableDeclarationTypes:
        if re.search(" *" + dataType, line):
            if re.search("//", line) and re.search(";", line):
                return True
            break
    return False

"""
  Function Name:

  	isVariableDeclaration

  Description:

  	Checks if the given line is a variable declaration

  Parameters:

  	String  line  the line to check

  Returns:

  	boolean  isVariable  returns True if line contains variable declaration, returns False otherwise
"""
def isVariableDeclaration(line):
    variableDeclarationTypes = ["double", "int", "bool", "float", "char", "long", "unsigned", "void", "string", "File", "short", "SdVolume", "Sd2Card", "SdFile"]
    for dataType in variableDeclarationTypes:
        if re.search(" *" + dataType, line):
            if re.search("//", line) and re.search(";", line):
                return True
            break
    return False


"""
Function Name:

    variablesIndexHTML

Description:

  	Creates the HTML for the variable index page
"""
def variablesIndexHTML(output_directory, state):

    variables = state["variables"]

    fileHTML = htmlHead("Variable Index", "..")
    fileHTML += "\n<body>"
    fileHTML += htmlNavBar("Variables")
    fileHTML += "\n<main>"
    fileHTML += "\n<div class=\"header\">"
    fileHTML += "\n<a id=\"whitespace\"></a>"
    fileHTML += "\n<h2 title=\"Variables\" class=\"title\">Variables</h2>"
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


    if len(variables) >= 1:
        fileHTML += "\n<table class=\"memberSummary\">"
        fileHTML += "\n<caption><span>Index</span><span class=\"tabEnd\">&nbsp;</span></caption>"
        fileHTML += "\n<tr>"
        fileHTML += "\n<th class=\"colFirst\" scope=\"col\">Name</th>"
        fileHTML += "\n<th class=\"colSecond\" scope=\"col\">Data Type</th>"
        fileHTML += "\n<th class=\"colSecond\" scope=\"col\">Inital Value</th>"
        fileHTML += "\n<th class=\"colLast\" scope=\"col\">Function Usage Count</th>"
        fileHTML += "</tr>"
        fileHTML += "<tr id=\"i0\" class=\"altColor\">"


        for variable in variables:
            fileHTML += "\n<tr id=\"i0\" class=\"altColor\">"
            fileHTML += "\n<td class=\"colFirst\"><code><a href=\"../variables/" + variable.name + ".html\">" + variable.name + "</a></code></td>"
            fileHTML += "\n<th class=\"colSecond\" scope=\"row\"><code>" + variable.pointer_depth * "*" + variable.dataType + "</code></th>"
            fileHTML += "\n<th class=\"colSecond\" scope=\"row\"><code>" + variable.inital_value + "</code></th>"
            fileHTML += "\n<td class=\"colLast\">"
            fileHTML += "\n<div class=\"block\"><code>" + str(len(variable.usage)) + "</code></div>"
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

    htmlFile = open(output_directory + "/indexes/variables.html", "w")
    htmlFile.write(fileHTML)
    htmlFile.close()


"""
Function Name:

    variableToHTML

Description:

  	Converts a variable object into a HTML file

Parameters:

    Variable  variable  the variable to turn into a HTML file

"""
def variableToHTML(output_directory, variable):
    fileHTML = htmlHead(variable.name, "..")
    fileHTML += "\n<body>"
    fileHTML += htmlNavBar("")
    fileHTML += "\n<main>"
    fileHTML += "\n<div class=\"header\">"
    fileHTML += "\n<a id=\"whitespace\"></a>"
    fileHTML += "\n<h2 title=\"Variable Name\" class=\"title\">" + variable.name + "</h2>"
    fileHTML += "\n</div>"
    fileHTML += "\n<div class=\"contentContainer\">"
    fileHTML += "\n<div class=\"description\">"
    fileHTML += "\n</ul>"
    fileHTML += "\n</div>"
    fileHTML += htmlVariableSummary(variable)
    fileHTML += htmlVariableReferences(variable)
    fileHTML += htmlVariableBody(variable)
    fileHTML += "\n</div>"
    fileHTML += "\n</main>"
    fileHTML += "\n</body>"
    fileHTML += "\n</html>"

    htmlFile = open(output_directory + "/variables/" + variable.name + ".html", "w")
    htmlFile.write(fileHTML)
    htmlFile.close()


"""
    Function Name:

        htmlVariableBody

    Description:

  	    Returns a String contaning the the variable body portion of the variable page in HTML

    Parameter:

        Variable  in_variable  the variable to create the variable body in HTML for

    Returns:

        String  htmlString  the html file string
"""
def htmlVariableBody(in_variable):
    htmlString = ""
    htmlString += "\n<div class=\"details\">"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    htmlString += "\n<section>"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    
    htmlString += "\n<h3>Variable Declaration</h3>"
    
    htmlString += "\n<ul class=\"blockListLast\">"
    htmlString += "\n<li class=\"blockList\">"
    htmlString += "\n<h4>" + in_variable.name + "</h4>"
    codeString = in_variable.code
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

        htmlVariableSummary

    Description:

  	    Returns a String contaning the variable summary of a variable page in HTML

    Parameter:

        Variable  in_variable  the variable to turn into a HTML variable summary

    Returns:

        String  htmlString  the html file string
"""
def htmlVariableSummary(in_variable):

    htmlString = ""

    htmlString += "\n<div class=\"details\">"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<section>"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    
    htmlString += "\n<h3>Variable Summary</h3>"
    

    htmlString += "\n<ul v class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    htmlString += "\n<h4>Description</h4>"
    htmlString += "\n<div class=\"block\">" + in_variable.description.replace("\n", "<br \/>") + "</div>"
    htmlString += "\n</li>"

    
    htmlString += "\n<table class=\"memberSummary\">"
    htmlString += "<caption><span>Fields</span><span class=\"tabEnd\"> &nbsp;</span></caption>"
    htmlString += "\n<tr>"
    htmlString += "\n<th class=\"colFirst\" scope=\"col\">Data Type</th>"
    htmlString += "\n<th class=\"colSecond\" scope=\"col\">Name</th>"
    htmlString += "\n<th class=\"colLast\" scope=\"col\">Inital Value</th>"
    htmlString += "\n</tr>"
    htmlString += "\n<tr id=\"i0\" class=\"altColor\">"
    htmlString += "\n<td class=\"colFirst\"><code>" + "*" * in_variable.pointer_depth + in_variable.dataType + "</code></td>"
    htmlString += "\n<th class=\"colSecond\" scope=\"row\"><code>" + in_variable.name + "</code></th>"
    htmlString += "\n<td class=\"colLast\">"
    htmlString += "\n<div class=\"block\">" + in_variable.inital_value + "</div>"
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

        htmlVariableReferences

    Description:

  	    Returns a String contaning the references of a variable file in HTML

    Parameter:

        Variable  in_variable  the variable to create the HTML references section for

    Returns:

        String  htmlString  the html file string
"""
def htmlVariableReferences(in_variable):
    htmlString = ""

    if len(in_variable.usage) >= 1:
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

        for function in in_variable.usage:
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

    isVariableDeclaration

Description:

    Checks if a line of code is a variable declaration.

Returns:

    Boolean  True if the line is a variable declaration, False otherwise.
"""
def isVariableDeclaration(line):

    variableDeclarationTypes = ["double", "int", "bool", "float", "char", "long", "unsigned", "void", "string", "File", "short", "SdVolume", "Sd2Card", "SdFile"]

    for dataType in variableDeclarationTypes:
        if re.search(" *" + dataType, line):
            if re.search("//", line) and re.search(";", line):
                return True
            break
    return False

