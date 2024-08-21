import argparse
import sys
import re
import os
import shutil

from lib.Constant import *
from lib.Function import *
from lib.Library import *
from lib.Variable import *
from lib.utils import *
        
"""
Function Name:

    createDirectories

Description:

  	Creates the neccesary directories for the documentation
"""
def createDirectories(output_directory):

    # Create the base directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # List of subdirectories to create
    subdirs = ["functions", "variables", "constants", "libraries", "indexes", "stylesheets"]
    
    # Create each subdirectory
    for subdir in subdirs:
        os.makedirs(os.path.join(output_directory, subdir), exist_ok=True)

"""
Function Name:

    returnScraper

Description:

    Extracts return information from the function documentation and updates the Function object.

Returns:

    String  line  the next line in the file after scraping the return information.
"""
def returnScraper(file, new_function):
	line = skipBlankLines(file)
	while True:
		if  re.search(".*Parameters: *\n", line) or re.search("(\*\/)", line) or re.search("([ *]*)(N\/A) *\n", line):
			break
		else:
			new_variable = Variable()
			groups  = re.search("([ *]*)([\w*]*)([ ]*)([\w]*)([ ]*)([\w\[.!?\\-\]`~\{\}\"\'\;\:,\/=+@#$%^&*() ]*[\w\[.!?\\-\]`~\{\}\"\'\;\:,\/=+@#$%^&*()])( *\n)",  line, re.I | re.U)
			new_variable.description = groups.group(6)
			new_variable.name = groups.group(4)
			new_variable.dataType = groups.group(2)
			new_variable.pointer_depth = new_variable.dataType.count("*")
			new_variable.dataType = new_variable.dataType.replace("*", "")
			new_function.returnValue = new_variable
		line = skipBlankLines(file)
	return line

"""
Function Name:

    parameterScraper

Description:

    Extracts parameter information from the function documentation and updates the Function object.

Returns:

    String  line  the next line in the file after scraping the parameter information.
""" 
def parameterScraper(file, new_function):
	line = skipBlankLines(file)
	while True:
		if  re.search(".*Returns: *\n", line) or re.search("(\*\/)", line) or re.search("([ *]*)(N\/A) *\n", line):
			break
		else:
			new_variable = Variable()
			groups  = re.search("([ *]*)([\w*\[\]]*)([ ]*)([\w]*)([ ]*)([\w\[.!?\\-\]`~\{\}\"\'\;\:,\/=+@#$%^&*() <>]*[\w\[.!?\\-\]`~\{\}\"\'\;\:,\/=+@#$%^&*()<>])( *\n)",  line, re.I | re.U)

			new_variable.description = groups.group(6)
			new_variable.name = groups.group(4)
			new_variable.dataType = groups.group(2)
			new_variable.pointer_depth = new_variable.dataType.count("*")
			new_variable.dataType = new_variable.dataType.replace("*", "")
			new_function.appendParameter(new_variable)
		line = skipBlankLines(file)
	return line

"""
Function Name:

    descriptionScraper

Description:

    Extracts the description from the function documentation and updates the Function object.

Returns:

    String  line  the next line in the file after scraping the description.
"""
def descriptionScraper(file, new_function):
    description = ""
    line = skipBlankLines(file)
    while True:
        if re.search(".*Parameters: *\n", line) or re.search(".*Returns: *\n", line) or re.search("(\*\/)", line):
            break
        elif re.search("^.*Description: *\n", line) or re.search("^.*Function Name: *\n", line):
            unformedSyntaxHandler(line)
        else:
            description += re.search("([ *]*)([\w\[.!?\\\\-\]`~\{\}\"\'\;\:,\/=+@#$%^&*() <>]*[\w\[.!?\\-\]`~\{\}\"\'\;\:,\/=+@#$%^&*()<>])( *\n)",  line, re.I | re.U).group(2) + "\n"
        line = skipBlankLines(file)

    #Remove last end of line character if present
    if description.endswith("\n"):
        description = description[:-1]

    new_function.description = description
    return line

"""
Function Name:

    harvestFunction

Description:

    Parses a function's documentation and code from the file, creating a Function object.

"""
def harvestFunction(file, state):

	new_function = Function()
	#Keep going until we find a non-blank line (has the function name)
	line = skipBlankLines(file)

	if re.search("^.*Description: *\n", line):
		unformedSyntaxHandler(line)

	#Harvest function name from line
	new_function.name = re.sub("(\W)", "",  line)
	#Keep going until we encounter another field, (description field)
	line = skipBlankLines(file)

	#Check if field is description field
	if re.search("^.*Description: *\n", line):
		line = descriptionScraper(file, new_function)
	else:
		#Couldn't find description header
		unformedSyntaxHandler(line)

	headingsHarvestedCount = 0

	while headingsHarvestedCount < 2:
		if re.search(".*Parameters: *\n", line):
			line = parameterScraper(file, new_function)
		elif re.search(".*Returns: *\n", line):
			line = returnScraper(file, new_function)
		elif re.search("([ *]*)(N\/A) *\n", line):
			line = skipBlankLines(file)
			headingsHarvestedCount -= 1
		elif re.search("(\*\/)", line):
			#Done harvesting the function header
			break
		headingsHarvestedCount += 1

    #Confirm end of header was found
	if not re.search("(\*\/)", line):
		line = skipBlankLines(file)
		if not re.search("(\*\/)", line):
			unformedSyntaxHandler()

	line = skipBlankLines(file)

	code = ""

    #Harvest plain-text code
	opening_curly_count = line.count("{")
	closing_curly_count = line.count("}")
	code = line

	while opening_curly_count >= 1 and opening_curly_count != closing_curly_count:
		line = file.readline()
		opening_curly_count += line.count("{")
		closing_curly_count += line.count("}")
		code += line

	new_function.code = code

    #Append the created Function object
	state["functions"].append(new_function)

"""
Function Name:

    writeCSS

Description:

  	Writes CSS stylesheet to the top level directory of the documentation for reference from HTML files

"""
def writeCSS(output_directory, source_directory="./lib"):
    # Define the file paths
    cssFilePath = output_directory + "/stylesheets/stylesheet.css"
    
    # Define the source CSS file path
    source_css_path = os.path.join(source_directory, "stylesheet.css")
    
    # Read the content from the source CSS file
    with open(source_css_path, "r") as source_css_file:
        stylesheetCSS = source_css_file.read()
    
    # Write the content to the destination CSS file
    with open(cssFilePath, "w") as cssFile:
        cssFile.write(stylesheetCSS)

"""
Function Name:

    dataToHTML

Description:

    Writes data present in objects to HTML files within respective files along with writing index files

"""
def dataToHTML(output_directory, state):
    for function in state["functions"]:
        functionToHTML(output_directory, function)

    
    for variable in state["variables"]:
        variableToHTML(output_directory, variable)

    
    for constant in state["constants"]:
        constantToHTML(output_directory, constant)

    
    for library in state["libraries"]:
        libraryToHTML(output_directory, library)
    
"""
Function Name:

    writeIndexHTML

Description:

    Writes out the HTML for creating indexs under the indexes directory of generated documentation

"""
def writeIndexHTML(output_directory, state):
    functionsIndexHTML(output_directory, state)
    variablesIndexHTML(output_directory, state)
    constantsIndexHTML(output_directory, state)
    librariesIndexHTML(output_directory, state)

"""
Function Name:

    writeHomeHTML

Description:

    Writes the home page HTML for the documentation

"""
def writeHomeHTML(output_directory, state):
    fileHTML = htmlHead("Home", ".")
    fileHTML += "\n<body>"
    fileHTML += "\n<body>"
    fileHTML += "\n<header>"
    fileHTML += "\n<nav>"
    fileHTML += "<div class=\"topNav\">"
    fileHTML += "<a id=\"navbar.top\"></a>"
    fileHTML += "\n<ul class=\"navList\" title=\"Navigation\">"

    fileHTML += "\n<li class=\"navBarCell1Rev\">Home</li>"
    fileHTML += "\n<li><a href=\"./indexes/functions.html\">Functions</a></li>"
    fileHTML += "\n<li><a href=\"./indexes/variables.html\">Variables</a></li>"
    fileHTML += "\n<li><a href=\"./indexes/constants.html\">Constants</a></li>"
    fileHTML += "\n<li><a href=\"./indexes/libraries.html\">Libraries</a></li>"
    fileHTML += "\n</header>"

    fileHTML += "\n<main>"
    fileHTML += "\n<div class=\"header\">"
    fileHTML += "\n<a id=\"whitespace\"></a>"
    fileHTML += "\n<h2 title=\"Homepage Header\" class=\"title\">" + output_directory + "</h2>"
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
    fileHTML += "\n<a id=\"whitespace\"></a>"
    fileHTML += """<ul class="blockList">
                <li class="blockList">
                <h3>Documentation Overview</h3>
                <div class="block">
                    Documentation is generated for  generates pages for snippets of code that correspond to the following categories.<br><br>
                    <b>Functions</b><br><br>
                    Functions with documented parameters, return values, references.<br><br>
                    <b>Variables</b><br><br>
                    Global variables with documented data types, initial values, and references.<br><br>
                    <b>Constants</b><br><br>
                    Constant with documented inferred data types and values.<br><br>
                    <b>Libraries</b><br><br>
                    Documentation on libraries and versions used in the program.
                </div>
                </li>"""

    fileHTML += "\n<table class=\"memberSummary\">"
    fileHTML += "\n<caption><span>Size</span><span class=\"tabEnd\">&nbsp;</span></caption>"
    fileHTML += "\n<tr>"
    fileHTML += "\n<th class=\"colFirst\" scope=\"col\">Functions</th>"
    fileHTML += "\n<th class=\"colSecond\" scope=\"col\">Variables</th>"
    fileHTML += "\n<th class=\"colSecond\" scope=\"col\">Constants</th>"
    fileHTML += "\n<th class=\"colSecond\" scope=\"col\">Libraries</th>"
    fileHTML += "</tr>"
    fileHTML += "<tr id=\"i0\" class=\"altColor\">"

    fileHTML += "\n<tr id=\"i0\" class=\"altColor\">"
    fileHTML += "\n<td class=\"colFirst\"><code>" + str(len(state["functions"])) + "</code></td>"
    fileHTML += "\n<td class=\"colSecond\"><code>" + str(len(state["variables"])) + "</code></td>"
    fileHTML += "\n<td class=\"colSecond\"><code>" + str(len(state["constants"])) + "</code></td>"
    fileHTML += "\n<td class=\"colSecond\"><code>" + str(len(state["libraries"])) + "</code></td>"
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

    htmlFile = open(output_directory + "/home.html", "w")
    htmlFile.write(fileHTML)
    htmlFile.close()

"""
Function Name:

    harvestLibraryImport

Description:

    Extracts library import information from a line of code and updates the state object with a Library instance.

"""
def harvestLibraryImport(state, line):
    new_library = Library()
    groups = re.search("( *)(#include)( *)([<\"\'][\w.\"\']*[\"\'>])( *)(\/\/)([\w ]*[\w ])( *\n)",  line, re.I | re.U)
    new_library.name = groups.group(4)
    new_library.description = groups.group(7)
    new_library.code = groups.group(1) + groups.group(2) + groups.group(3) + groups.group(4)
    state["libraries"].append(new_library)

"""
Function Name:

    harvestConstant

Description:

    Extracts constant information from a line of code and updates the state object with a Constant instance.

"""
def harvestConstant(state, line):
  #Create a new instance of a Constant object
  new_constant = Constant()

  #collect indexes
  first_space_index = findN(line, " ", 1)
  second_space_index = findN(line, " ", 2)
  comment_index = findN(line, "//", 1)

  #check for an unformed file, this check should be expanded for more context then single space delimiters for arguments
  if first_space_index == -1 or second_space_index == -1 or (comment_index != -1 and comment_index < second_space_index):
      unformedSyntaxHandler(line)

  #harvest value by searching from left of comment to first character, then searching for whitespace
  value_right_index = -1

  if comment_index != -1:
      value_right_index = searchForChar(line, " ", -1, comment_index-1, False)
  else:
      value_right_index = searchForChar(line, " ", -1, len(line)-2, False)

  value_left_index = searchForChar(line, " ", -1, value_right_index, True)

  #now that we know the indexs we can harvest the value
  new_constant.value = line[value_left_index+1:value_right_index+1]

  name_right_index = searchForChar(line, " ", -1, value_left_index-1, False)
  name_left_index = searchForChar(line, " ", -1, name_right_index, True)
  new_constant.name = line[name_left_index+1:name_right_index+1]
  #harvest description
  if comment_index != -1:
      if line.endswith("\n"):
          new_constant.description = line[comment_index+2:len(line)-1]
      else:
          new_constant.description = line[comment_index+2:len(line)]

  #check for int
  intFlag = False

  try:
      temp = int(new_constant.value)
      intFlag = True
  except ValueError:
      pass

  #check for float, 1 period and able to be removed and then check if digit
  floatFlag = False

  if new_constant.value.count(".") == 1:
      floatFlag = new_constant.value.replace(".", "", 1).replace("-", "", 1).isdigit()

  #quotes indicate it being a string
  stringFlag = False

  if (new_constant.value[-1] == "\"" and new_constant.value[0] == "\"") or (new_constant.value[-1] == "\'" and new_constant.value[0] == "\'"):
      stringFlag = True

  booleanFlag = False
  if new_constant.value == "true" or new_constant.value == "false":
      booleanFlag = True

  #check statement where String>float>int
  if booleanFlag:
      new_constant.dataType = "bool"
  elif stringFlag:
      new_constant.dataType = "String"
  elif floatFlag:
      new_constant.dataType = "float"
  elif intFlag:
      new_constant.dataType = "int"
  else:
      new_constant.dataType = "keyword"

  new_constant.code = line[0:value_right_index+1]

  state["constants"].append(new_constant)

"""
Function Name:

    harvestVariable

Description:

    Extracts variable information from a line of code and updates the state object with a Variable instance.

"""
def harvestVariable(state, line):

  new_variable = Variable()

  #collect indexes
  semicolon_index = findN(line, ";", 1)
  comment_index = findN(line, "//", 1)
  equals_index = findN(line, "=", 1)

  #check for an unformed file
  if semicolon_index == -1 or comment_index == -1 or comment_index < semicolon_index:
      unformedSyntaxHandler(line)

  #harvest description
  if comment_index != -1:
      if line.endswith("\n"):
          new_variable.description = line[comment_index+2:len(line)-1]
      else:
          new_variable.description = line[comment_index+2:len(line)]

  asteriskCount = 0
  name_right_index = -1

  if equals_index != -1 and equals_index < semicolon_index:
      name_right_index = searchForChar(line, " ", -1, equals_index-1, False)
  else:
      name_right_index = searchForChar(line, " ", -1, semicolon_index-1, False)

  name_left_index = searchForChar(line, " ", -1, name_right_index, True)
  tempName = line[name_left_index+1:name_right_index+1]

  #function pointer check
  if ")" not in tempName:
      asteriskCount += tempName.count("*")
      tempName = tempName.replace("*", "").replace(" ", "")
      arrayTag = False
      if "[" in tempName and "]" in tempName:
          sqaure_left_index = findN(tempName, "[", 1)
          sqaure_right_index = findN(tempName, "]", 1)
          tempName = tempName[0: sqaure_left_index:] + tempName[sqaure_right_index + 1::]
          arrayTag = True
      new_variable.name = tempName
      dataType_right_index = searchForChar(line, " ", -1, name_left_index-1, False)
      dataType_left_index = searchForChar(line, " ", 1, 0, False)
      tempDataType = line[dataType_left_index:dataType_right_index+1]
      asteriskCount += tempDataType.count("*")
      if arrayTag:
          new_variable.dataType = tempDataType.replace("*", "").replace(" ", "") + "[]"
      else:
          new_variable.dataType = tempDataType.replace("*", "").replace(" ", "")
  else:
      parameter_right_index = searchForChar(line, ")", -1, semicolon_index-1, True)
      parameter_left_index = searchForChar(line, "(", -1, parameter_right_index-1, True)
      body_right_index = searchForChar(line, ")", -1, parameter_left_index-1, True)
      body_left_index = searchForChar(line, "(", -1, body_right_index-1, True)
      pointer_left_index = searchForChar(line, " ", 1, 0, False)
      pointerAsteriskLine = line[0:body_right_index+1]
      asteriskCount += pointerAsteriskLine.count("*")
      bodyLine = pointerAsteriskLine.replace("*", "")
      new_variable.name = bodyLine[findN(bodyLine, "(", 1)+1:findN(bodyLine, ")", 1)].replace(" ", "")
      new_variable.dataType = line[pointer_left_index:parameter_right_index+1].replace(" ", "").replace(new_variable.name, "")

  new_variable._pointer_depth = asteriskCount

  #collect inital value
  if equals_index != -1 and equals_index < semicolon_index:
      inital_value_left_index = searchForChar(line, " ", 1, equals_index+1, False)
      inital_value_right_index = searchForChar(line, " ", -1, semicolon_index-1, False)
      new_variable.inital_value = line[inital_value_left_index:inital_value_right_index+1]
  else:
      new_variable.inital_value = "null"

  new_variable.code = line[0:semicolon_index+1]

  state["variables"].append(new_variable)


"""
Function Name:

    generateDocumentation

Description:

    Generates documentation for the provided Arduino sketch, outputting it to the specified directory.

"""
def generateDocumentation(arduino_sketch_path, output_directory, overwrite):

    # Attempt to open the Arduino sketch file for reading
    try:
        with open(arduino_sketch_path, "r") as file:
            file.close()

    except OSError:
        exitMessage(f"Error: Unable to open file '{arduino_sketch_path}' for reading. Please check the file path and try again.", 1)

    # Initialize the state
    state = {
        "functions": [],
        "variables": [],
        "constants": [],
        "libraries": []
    }

    currentLine = 0

    file = open(arduino_sketch_path, "r")

    line = file.readline()

    while line:

        if isFunctionHeader(line):
            harvestFunction(file, state)
        elif isVariableDeclaration(line):
            harvestVariable(state, line)
        elif isConstantDeclaration(line):
            harvestConstant(state, line)
        elif isLibraryImport(line):
            harvestLibraryImport(state, line)
            
        line = file.readline()
    

    for function in state["functions"]:
        analyzeFunctionBody(function, state)


    
    # Now handle the directory creation or overwrite after parsing
    if os.path.exists(output_directory):
        if overwrite:
            print(f"Overwriting directory: {output_directory}")
            shutil.rmtree(output_directory)  # Delete the directory and its contents
        else:
            exitMessage(f"Directory '{output_directory}' already exists. Use --overwrite to overwrite it.", 1)
    
    
    # Create the directory after parsing and analysis is successful
    os.makedirs(output_directory)
    print(f"Documentation generated at '{output_directory}'")

    createDirectories(output_directory)
    writeCSS(output_directory)
    dataToHTML(output_directory, state)
    writeIndexHTML(output_directory, state)
    writeHomeHTML(output_directory, state)

"""
Function Name:

    exitMessage

Description:

    Prints an exit message and exits the program with the provided code.

"""
def exitMessage(message, code):
    print(message)
    sys.exit(code)

"""
Function Name:

    main

Description:

    Main entry point for the script. Handles argument parsing and calls the documentation generation process.

"""
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process some files and directories.")
    
    # Required positional argument
    parser.add_argument("arduino_sketch", help="Path to the Arduino sketch file")
    
    # Optional flags
    parser.add_argument("-o", "--output", help="Output path for results", required=False)
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing directory")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Check if arduino_sketch has a valid extension
    validExtensions = ["ino", "cpp", "INO", "CPP", "h", "H", "hpp", "HPP", "hxx", "HXX", "cxx", "CXX", "cc", "CC"]
    extensionValid = False
    
    for extension in validExtensions:
        if args.arduino_sketch.endswith(extension):
            extensionValid = True
            noExtensionFileName = os.path.splitext(os.path.basename(args.arduino_sketch))[0]
            break
    
    if not extensionValid:
        exitMessage("Invalid file extension", 2)
    
    # Set default output directory if not provided
    if not args.output:
        args.output = os.path.join("output", noExtensionFileName)
    
    # Open the Arduino sketch file
    try:
        with open(args.arduino_sketch, "r") as file:
            file.close()
    except OSError:
        exitMessage("File not found\nDouble check your path was spelled correctly", 1)
    
    # After all checks, pass arguments to the business logic function
    generateDocumentation(arduino_sketch_path=args.arduino_sketch, 
                          output_directory=args.output, 
                          overwrite=args.overwrite)
    
if __name__ == "__main__":
    main()


