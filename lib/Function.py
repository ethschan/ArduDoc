import re
from lib.utils import *

"""
***************************************************************
CLASS NAME:

  Function

DESCRIPTION:

	Object repersenting a Function in the program
***************************************************************
"""
class Function:
  """
  Function Name:

  	__init__

  Description:

  	Constructor for Function

  Variables:

  	String  name  name of the function
    String  description  description of the function
    Variable[]  parameters  parameters of the function
    Variable  returnValue  return value of the function
	Variable[]  variables  the global variables manipulated by the function
    Constant[] constants  the global constants referenced by the fucntion
	Functions[]  functionCalls  functions called by the function
	String  code  the plain text code of the function
  """
  def __init__(self):
      self._description = ""
      self._parameters = []
      self._return_value = None
      self._variables = []
      self._function_calls = []
      self._constants = []
      self._code = ""
      self._name = ""

  def setName(self, name):
      self._name = name

  def setCode(self, code):
      self._code = code

  def setDescription(self, description):
      self._description = description

  def appendParameter(self, parameter):
      self._parameters.append(parameter)

  def setReturnValue(self, returnValue):
      self._return_value = returnValue

  def appendFunctionCall(self, function):
      self._function_calls.append(function)

  def appendVariable(self, variable):
      self._variables.append(variable)

  def appendConstant(self, constant):
      self._constants.append(constant)

  def getName(self):
      return self._name

  def getDescription(self):
      return self._description

  def getParameters(self):
      return self._parameters

  def getReturnValue(self):
      return self._return_value

  def getCode(self):
      return self._code

  def getFunctionCalls(self):
      return self._function_calls

  def getVariables(self):
      return self._variables

  def getConstants(self):
      return self._constants

  """
  Function Name:

    toString

  Description:

  	Prints out the current instance of the Function object to the command line for debugging.
  """
  def toString(self):
      print("========================================")
      print("Name: " + str(self._name) + "\n")
      print("Description:")
      print(self._description + "\n")
      print("Parameters:")
      for parameter in self._parameters:
          parameter.toString()
          print()
          print("\nReturn value:")
      if self._return_value != None:
        self._return_value.toString()
      print("Code:")
      print(self._code)
      print("Variables used:")
      for variable in self._variables:
          print(variable.name)
      print("Functions called:")
      for function in self._function_calls:
          print(function.name)
      print("========================================")

  #Property Calls
  name = property(getName, setName)
  description = property(getDescription, setDescription)
  parameters = property(getParameters)
  returnValue = property(getReturnValue, setReturnValue)
  code = property(getCode, setCode)
  functionCalls = property(getFunctionCalls)
  variables = property(getVariables)
  constants = property(getConstants)

"""
  Function Name:

  	isFunctionHeader

  Description:

  	Checks if the given line is the start of a function header

  Parameters:

  	String  line  the line to check

  Returns:

  	boolean  isFunctionHeader  returns True if line contains the start of a function header, returns False otherwise
"""
def isFunctionHeader(line):
    if re.search("^.*Function Name: *\n", line):
        return True
    return False


"""
Function Name:

    functionsIndexHTML

Description:

  	Creates the HTML for the function index page
"""
def functionsIndexHTML(output_directory, state):

    functions = state["functions"]

    fileHTML = htmlHead("Functions", "..")
    fileHTML += "\n<body>"
    fileHTML += htmlNavBar("Functions")
    fileHTML += "\n<main>"
    fileHTML += "\n<div class=\"header\">"
    fileHTML += "\n<a id=\"whitespace\"></a>"
    fileHTML += "\n<h2 title=\"Functions\" class=\"title\">Functions</h2>"
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

    if len(functions) >= 1:
        fileHTML += "\n<table class=\"memberSummary\">"
        fileHTML += "\n<caption><span>Index</span><span class=\"tabEnd\">&nbsp;</span></caption>"
        fileHTML += "\n<tr>"
        fileHTML += "\n<th class=\"colFirst\" scope=\"col\">Name</th>"
        fileHTML += "\n<th class=\"colSecond\" scope=\"col\">Parameter Count</th>"
        fileHTML += "\n<th class=\"colSecond\" scope=\"col\">Return Type</th>"
        fileHTML += "\n<th class=\"colSecond\" scope=\"col\">Functions Called</th>"
        fileHTML += "\n<th class=\"colSecond\" scope=\"col\">Global Variables Manipulated</th>"
        fileHTML += "\n<th class=\"colLast\" scope=\"col\">Constants Referenced</th>"
        fileHTML += "</tr>"
        fileHTML += "<tr id=\"i0\" class=\"altColor\">"


        for function in functions:
            fileHTML += "\n<tr id=\"i0\" class=\"altColor\">"
            fileHTML += "\n<td class=\"colFirst\"><code><a href=\"../functions/" + function.name + ".html\">" + function.name + "</a></code></td>"
            fileHTML += "\n<td class=\"colSecond\"><div class=\"block\"><code>" + str(len(function.parameters)) + "</code></div></td>"
            if function.returnValue != None:
                fileHTML += "\n<th class=\"colSecond\" scope=\"row\"><code>" + function.returnValue.pointer_depth * "*" + function.returnValue.dataType + "</code></th>"
            else:
                fileHTML += "\n<th class=\"colSecond\" scope=\"row\"><code>void</code></th>"
            fileHTML += "\n<td class=\"colSecond\"><div class=\"block\"><code>" + str(len(function.functionCalls)) + "</code></div></td>"
            fileHTML += "\n<td class=\"colSecond\"><div class=\"block\"><code>" + str(len(function.variables)) + "</code></div></td>"
            fileHTML += "\n<td class=\"colLast\"><div class=\"block\"><code>" + str(len(function.constants)) + "</code></div></td>"
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

    htmlFile = open(output_directory + "/indexes/functions.html", "w")
    htmlFile.write(fileHTML)
    htmlFile.close()

"""
Function Name:

    functionToHTML

Description:

  	Converts a function object into a HTML file

Parameters:

    Function  function  the function to turn into a HTML file

"""
def functionToHTML(output_directory, function):
    fileHTML = htmlHead(function.name, "..")
    fileHTML += "\n<body>"
    fileHTML += htmlNavBar("")
    fileHTML += "\n<main>"
    fileHTML += "\n<div class=\"header\">"
    fileHTML += "\n<a id=\"whitespace\"></a>"
    fileHTML += "\n<h2 title=\"Function Name\" class=\"title\">" + function.name + "</h2>"
    fileHTML += "\n</div>"
    fileHTML += "\n<div class=\"contentContainer\">"
    fileHTML += "\n<div class=\"description\">"
    fileHTML += "\n</ul>"
    fileHTML += "\n</div>"
    fileHTML += htmlFunctionSummary(function)
    fileHTML += htmlFunctionReferences(function)
    fileHTML += htmlFunctionBody(function)
    fileHTML += "\n</div>"
    fileHTML += "\n</main>"
    fileHTML += "\n</body>"
    fileHTML += "\n</html>"

    htmlFile = open(output_directory + "/functions/" + function.name + ".html", "w")
    htmlFile.write(fileHTML)
    htmlFile.close()


"""
    Function Name:

        htmlFunctionSummary

    Description:

  	    Returns a String contaning a function summary in HTML

    Parameter:

        Function  in_function  the function to turn into a HTML function summary

    Returns:

        String  htmlString  the html file string
"""
def htmlFunctionSummary(in_function):

    htmlString = ""

    if in_function.description != "" or len(in_function.parameters) >= 1 or in_function.returnValue != None:
        htmlString += "\n<div class=\"details\">"
        htmlString += "\n<ul class=\"blockList\">"
        htmlString += "\n<section>"
        htmlString += "\n<ul class=\"blockList\">"
        htmlString += "\n<li class=\"blockList\">"
        htmlString += "\n<h3>Function Summary</h3>"

        if in_function.description != "":
            htmlString += "\n<ul class=\"blockList\">"
            htmlString += "\n<li class=\"blockList\">"
            htmlString += "\n<h4>Description</h4>"
            htmlString += "\n<div class=\"block\">" + in_function.description.replace("\n", "<br \/>") + "</div>"

        htmlString += "\n</li>"

        if len(in_function.parameters) >= 1:
            htmlString += "\n<table class=\"memberSummary\">"
            htmlString += "\n<caption><span>Parameters</span><span class=\"tabEnd\">&nbsp;</span></caption>"
            htmlString += "\n<tr>"
            htmlString += "\n<th class=\"colFirst\" scope=\"col\">Data Type</th>"
            htmlString += "\n<th class=\"colSecond\" scope=\"col\">Name</th>"
            htmlString += "\n<th class=\"colLast\" scope=\"col\">Description</th>"
            htmlString += "</tr>"
            htmlString += "<tr id=\"i0\" class=\"altColor\">"


            for parameter in in_function.parameters:
                htmlString += "\n<tr id=\"i0\" class=\"altColor\">"
                htmlString += "\n<td class=\"colFirst\"><code>" + "*" * parameter.pointer_depth + parameter.dataType + "</code></td>"
                htmlString += "\n<th class=\"colSecond\" scope=\"row\"><code>" + parameter.name + "</code></th>"
                htmlString += "\n<td class=\"colLast\">"
                htmlString += "\n<div class=\"block\">" + parameter.description.replace("\n", " ") + "</div>"
                htmlString += "\n</td>"
                htmlString += "\n</tr>"

            htmlString += "\n</table>"

        if in_function.returnValue != None:
            htmlString += "\n<table class=\"memberSummary\">"
            htmlString += "<caption><span>Returns</span><span class=\"tabEnd\"> &nbsp;</span></caption>"
            htmlString += "\n<tr>"
            htmlString += "\n<th class=\"colFirst\" scope=\"col\">Data Type</th>"
            htmlString += "\n<th class=\"colSecond\" scope=\"col\">Name</th>"
            htmlString += "\n<th class=\"colLast\" scope=\"col\">Description</th>"
            htmlString += "\n</tr>"
            htmlString += "\n<tr id=\"i0\" class=\"altColor\">"
            htmlString += "\n<td class=\"colFirst\"><code>" + "*" * in_function.returnValue.pointer_depth + in_function.returnValue.dataType + "</code></td>"
            htmlString += "\n<th class=\"colSecond\" scope=\"row\"><code>" + in_function.returnValue.name + "</code></th>"
            htmlString += "\n<td class=\"colLast\">"
            htmlString += "\n<div class=\"block\">" + in_function.returnValue.description + "</div>"
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

        htmlFunctionReferences

    Description:

  	    Returns a String contaning the references of a function file in HTML

    Parameter:

        Function  in_function  the function to create the HTML references section for

    Returns:

        String  htmlString  the html file string
"""
def htmlFunctionReferences(in_function):
    htmlString = ""

    if len(in_function.functionCalls) >= 1 or len(in_function.variables) >= 1 or len(in_function.constants) >= 1:
        htmlString += "\n<div class=\"details\">"
        htmlString += "\n<ul class=\"blockList\">"
        htmlString += "\n<section>"
        htmlString += "\n<ul class=\"blockList\">"
        htmlString += "\n<li class=\"blockList\">"
        htmlString += "\n<h3>References</h3>"
        htmlString += "\n<ul class=\"blockList\">"
        if len(in_function.functionCalls) >= 1:
            htmlString += "\n<li class=\"blockList\">"
            htmlString += "\n<h4>Referenced Functions</h4>"

            buildString = ""

            firstFlag = True

            for function in in_function.functionCalls:
                if firstFlag:
                    buildString += "<a href=\"../functions/" + function.name + ".html\">" + function.name + "</a>"
                    firstFlag = False
                else:
                    buildString += ", <a href=\"../functions/" + function.name + ".html\">" + function.name + "</a>"

            htmlString += "\n<code>" + buildString + "</code>"

            htmlString += "\n</li>"

        if len(in_function.variables) >= 1:
            htmlString += "\n<li class=\"blockList\">"
            htmlString += "\n<h4>Referenced Variables</h4>"

            buildString = ""

            firstFlag = True

            for variable in in_function.variables:
                if firstFlag:
                    buildString += "<a href=\"../variables/" + variable.name + ".html\">" + variable.name + "</a>"
                    firstFlag = False
                else:
                    buildString += ", <a href=\"../variables/" + variable.name + ".html\">" + variable.name + "</a>"


            htmlString += "\n<code>" + buildString +  "</code>"

            htmlString += "\n</li>"

        if len(in_function.constants) >= 1:
            htmlString += "\n<li class=\"blockList\">"
            htmlString += "\n<h4>Referenced Constants</h4>"

            buildString = ""

            firstFlag = True

            for constant in in_function.constants:
                if firstFlag:
                    buildString += "<a href=\"../constants/" + constant.name + ".html\">" + constant.name + "</a>"
                    firstFlag = False
                else:
                    buildString += ", <a href=\"../constants/" + constant.name + ".html\">" + constant.name + "</a>"


            htmlString += "\n<code>" + buildString +  "</code>"
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

        htmlFunctionBody

    Description:

  	    Returns a String contaning the the function body portion of the function page in HTML

    Parameter:

        Function  in_function  the function to create the function body in HTML for

    Returns:

        String  htmlString  the html file string
"""
def htmlFunctionBody(in_function):
    htmlString = ""
    htmlString += "\n<div class=\"details\">"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    htmlString += "\n<section>"
    htmlString += "\n<ul class=\"blockList\">"
    htmlString += "\n<li class=\"blockList\">"
    htmlString += "\n<a id=\"whitespace\"></a>"
    htmlString += "\n<h3>Function Body</h3>"
    htmlString += "\n<a id=\"whitespace\"></a>"
    htmlString += "\n<ul class=\"blockListLast\">"
    htmlString += "\n<li class=\"blockList\">"
    htmlString += "\n<h4>" + in_function.name + "</h4>"
    codeString = in_function.code
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

        analyzeFunctionBody

    Description:

  	    Analyzes and parses a function body.
"""
def analyzeFunctionBody(function_to_analyze, state):
    code_to_analyze = function_to_analyze.code
    for function in state["functions"]:
        if function.name != function_to_analyze.name:
            if re.search(function.name + "(\(.*\))",  code_to_analyze, re.I | re.U):
                function_to_analyze.appendFunctionCall(function)

    for variable in state["variables"]:
        if variable.name in code_to_analyze:
            function_to_analyze.appendVariable(variable)
            variable.appendUsage(function_to_analyze)

    for constant in state["constants"]:
        if constant.name in code_to_analyze:
            function_to_analyze.appendConstant(constant)
            constant.appendUsage(function_to_analyze)

