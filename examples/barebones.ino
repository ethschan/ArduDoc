//INCLUDE STATMENTS

#include <math.h> //module for mathematical operations
#include <SPI.h> //module for serial peripherals
#include <SD.h> //module for communication to the SD module

//CONSTANT DEFINITIONS

#define selectPin 25 //the input pin for the select button
#define enterPin 27 //enterPin  the input pin for the enter button
#define chipSelectPin 4 //chipSelectPin  the chip select pin for the SD card module
#define adcPin A1 //adcPin  the input pin for adc reading


#define NULL 0 //0/none type defintion
#define true 1 //true boolean type definition
#define false 0 //false boolean type definition

#define dataPointLimit 100 //the maximum amount of data points that can be analyzed at once
#define voltageMaxNum 1240 //the numeric upper limit of the voltage readings
#define voltageMax 1.5 //the voltage upper limit of the voltage readings in volts
#define xSmoothing 5 //the number of points that are averaged together when processing the signal
#define maxConsec 50 //the number of times the average signal value must be at voltMin to indicate full activation
double voltInit = 1023; //the voltage threshold to start recording sample data at
double voltMin = 1018; //the volage threshold to stop recording sample data at
double maxProx = 0.01; //maxProx  maximum proximity to thresholds to count as being at the threshold

#define sampleHeader "Time,Voltage" //sampleHeader  the header put at the start of every sample file

#define config_file_name "config.txt" //the name of the config file
#define defaultConfig "0,0,0,0,0," //the default values for the config file
String config_file_header = "config file"; //the header of the config file
#define config_file_max_length 5 //the maximum length of the config file

#define polynomialCoefficientsLength 5 //the degree of the polynomial calibration curve
double polynomialCoefficients[] = {-1.429853631, -12706.68318, -14167424.16, -7134542069, -1237387574000}; //the coefficents of the polynomial calibration curve

#define translationSlope -382.60163696 //the linear slope to fit adc readings to fluoride concentrations
#define translationIntercept 1.8971014383603841 //the linear intercept to fit the adc readings to fluoride concentrations

//DYNAMIC VARIABLES

int selectState = 0; //variable for the state of the select button
int enterState = 0; //variable for the state of the enter button

double xPoints[dataPointLimit]; //xPoints  an array that stores the x-axis of data points collected when reading a sample
double yPoints[dataPointLimit]; //yPoints  an array that stores the y-axis of data points collected when reading a sample
int dataPointsLength; //the number of data points stored in xPoints and yPoints

String config_file[config_file_max_length]; //An array that stores the values collected from the config file
int config_length = 0; //the number of values stored in the config file

File fileOpen; //the current file open on the SD card

/*
* Function Name:
*
*   sdResponse
*
* Description:
*
*   Takes in a file object from a SD card and returns a string with all the data from that file
*
* Parameters:
*
*   File  file  the file to read the response from
*
* Returns:
*
*   String  response  characters from the SD card sent to the microcontroller
*/
String sdResponse(File file) {
  String response = "";
  while (file.available()) {
      response = response + char(file.read());
  }//end of while(file.available())
  file.close();
  return response;
}//end of sdResponse


/*
* Function Name:
*
*   stripString
*
* Description:
*
*   Takes in a string and removes the characters new line (\n), carriage return (\r), command in (>), and command out (<).
*
* Parameters:
*
*   String  s  input string to replace characters from
*
* Returns:
*
*   String  s  output string with characters replaced
*/
String stripString(String s) {
  s.replace("\n", "");
  s.replace("\r", "");
  s.replace(">", "");
  s.replace("<", "");
  return s;
}//end of stripString


/*
* Function Name:
*
*   writeConfig
*
* Description:
*
*   Deletes the current config file and creates a new one with the current values stored in the config_file array.
*
* Parameters:
*
*   N/A
*
* Returns:
*
*   N/A
*/
void writeConfig() {
  //delete the current config_file
  SD.remove(config_file_name);

  //create the new config_file and write to it
  fileOpen = SD.open(config_file_name, FILE_WRITE);
  fileOpen.print(config_file_header);
  fileOpen.write("\n");
  for (int i = 0; i < config_length; i++) {
    fileOpen.print(config_file[i] + ",");
  }//end of for

  fileOpen.close();
}//end of writeConfig

/*
* Function Name:
*
*   fatalErrorHandler
*
* Description:
*
*   Outputs the given error message for the fatal error and then exits.
*
* Parameters:
*
*   String  error  the error message
*
* Returns:
*
*   N/A
*/
void fatalErrorHandler(String error) {
  Serial.println(error);
  delay(100);
  exit(0);
}//end of fatalErrorHandler

/*
* Function Name:
*
*   createDefaultConfig
*
* Description:
*
*   Creates a default config file.
*
* Parameters:
*
*   N/A
*
* Returns:
*
*   N/A
*/
void createDefaultConfig() {
  fileOpen = SD.open(config_file_name, FILE_WRITE);
  fileOpen.print(config_file_header);
  fileOpen.write("\n");
  fileOpen.print(defaultConfig);
  fileOpen.close();
}//end of createDefaultConfig


/*
* Function Name:
*
*   loadConfig
*
* Description:
*
*   Reads the config file from the SD card and puts extracted values into the array config_file for later use
*   if there is no config file or it is corrupted create a default config file.
*
* Parameters:
*
*   N/A
*
* Returns:
*
*   N/A
*/
void loadConfig() {
  //check if config file exists
  if (!SD.exists(config_file_name)) {
    //if it dosen't exist create it
    createDefaultConfig();
  }//end of if

  //config file must exist by this point
  fileOpen = SD.open(config_file_name);

  //read data from the config file
  String response = stripString(sdResponse(fileOpen));

  //check if the config file is not corrupted by checking if it's header is intact
  if (response.substring(0, config_file_header.length()) != config_file_header) {
    //if not delete existing config file and create default one
    Serial.println("corrupted config file");
    SD.remove(config_file_name);
    createDefaultConfig();
    //read back the newly created default config file
    fileOpen = SD.open(config_file_name);
    response = stripString(sdResponse(fileOpen));
  }//end of if

  //get the data collected from the config file ready for collecting data
  response.replace(String(config_file_header), "");

  //setup flags to extract values from config file
  int count = 0;
  int lastIndex = 0;
  for (int i = 0; i < response.length(); i++) {
    //if comma is encountered
    if (response.substring(i, i + 1) == ",") {
      //put piece of data casted into integer into config_file for storage
      config_file[count] = response.substring(lastIndex, i);
      lastIndex = i + 1;
      count += 1;
    }//end of if
  }//end of for
  config_length = count;
}//end of loadConfig

/*
 * Function Name:
 *
 *  averagedAnalogInput
 *
 * Description:
 *
 *  Reads a number of analog values, from the given pin, equal to xSmoothing times. Returns averaged results.
 *
 * Parameters:
 *
 *  int  analogPin  the analog pin to read signals from
 *
 * Returns:
 *
 *  double averagedValue the average of the last xSmoothing number of points read
 */
double averagedAnalogInput(int analogPin) {
  double averagedValue = 0;

  for (int i = 0; i < xSmoothing; i++) {
    averagedValue += analogRead(analogPin);
    //wait 3ms to let adc stabilize
    delay(3);
  }//end of for

  averagedValue = averagedValue / xSmoothing;

  return averagedValue;
}//end of averagedAnalogInput



/*
* Function Name:
*
*   loadSampleData
*
* Description:
*
*   Takes in an index of a sample file and loads data from a sample file into the xPoints and yPoints arrays.
*
* Parameters:
*
*   int   index   the index of the sample file to read from
*
* Returns:
*
*   N/A
*/
void loadSampleData(int index) {

  //resolve sample file name
  String fileName = "SAMPLE" + String(index) + ".csv";

  //check file exists
  if (!SD.exists(fileName)) {
    fatalErrorHandler("Sample file does not exist.");
  }

  //open file in reading mode
  fileOpen = SD.open(fileName);

  Serial.println("file opened to read back data");

  int totalDatapoints = 0;

  String response = "";

  //clear sample header
  while (fileOpen.available()) {
    response = response + char(fileOpen.read());
    if (response.substring(0, String(sampleHeader).length()) == sampleHeader) {
      break;
    }//end of if
  }//end of while

  Serial.println(response);

    Serial.println("sample header cleared");

  response = String("");

  //every time a comma is encountered, increment the amount of data points by 1
  while (fileOpen.available()) {
    if (char(fileOpen.read()) == ',') {
      totalDatapoints++;
    }//end of if
  }//end of while
  fileOpen.close();

  //calculate dataPoints to keep
  int interval = totalDatapoints/dataPointLimit;
  if (interval < 1) {
    interval = 1;
  }

    Serial.println("sample commas counted: " + String(totalDatapoints));
  int currentinterval = interval;

  //re-open file in read mode
  fileOpen = SD.open(fileName);

  Serial.println("re-open file to read this time");

  //clear sample header
  while (fileOpen.available()) {
    response = response + char(fileOpen.read());
    if (response.substring(0, String(sampleHeader).length() + 1) == String(sampleHeader) + "\n") {
      break;
    }//end of if
  }//end of while

  Serial.println("header has been cleared again");

  response = String("");
  char charIn;

  int dataPointsCollected = 0;
  //start recording data at intervals
  while (fileOpen.available()) {
    charIn = char(fileOpen.read());
    response = response + charIn;
    if (charIn == '\n') {
      if (interval == currentinterval) {
        xPoints[dataPointsCollected] = response.substring(0, response.indexOf(",")).toDouble();
        yPoints[dataPointsCollected] = response.substring(response.indexOf(",") + 1, response.indexOf("\n")).toDouble();
        dataPointsCollected++;
        currentinterval = 1;
      }//end of if
      else {
        currentinterval++;
      }//end of else
      response = String("");
    }//end of if
  }//end of while

  dataPointsLength = dataPointsCollected;
}//end of loadFluorideSample

/*
* Function Name:
*
*   startReading
*
* Description:
*
*   Makes sure consecutive adc values are below a certain threshold before resuming execution. This is to trim the activiation time and smooth out noise in the analog signal.
*
* Parameters:
*
*   double   threshold   the threshold to get lower than or equal to for the consecutive points
*
* Returns:
*
*   N/A
*/
void startReading() {
  double readIn;
  int currentConsec = 0;

  while(currentConsec < maxConsec){
    readIn = averagedAnalogInput(adcPin);
    if ((readIn - voltInit) <= maxProx) {
      currentConsec ++;
    }//end of if
    else {
      currentConsec = 0;
    }//end of else
  }//end of while

}//end of startReading

/*
* Function Name:
*
*   writeSampleToSD
*
* Description:
*
*   Trims signal from fully reacted distal tip, and writes the averaged analog input to a file.
*
* Parameters:
*
*   String  fileName  the name of the sample file to write data to
*
* Returns:
*
*   N/A
*/
void writeSampleToSD(String fileName){
  double readIn;
  int currentConsec = 0;
  unsigned long timeBefore = millis();

  //open file to write to
  fileOpen = SD.open(fileName, FILE_WRITE);

  //write sample header to file
  fileOpen.print(sampleHeader);

  //keep recording data while maxium consecutive points have not been hit
  while(currentConsec < maxConsec){
    readIn = averagedAnalogInput(adcPin);

    //write data point to sample file
    fileOpen.write("\n");
    fileOpen.print(String(millis() - timeBefore) + "," + String(readIn));

    //check if the value read in is close enough to threshold
    if ((readIn - voltMin) <= maxProx) {
      currentConsec ++;
    }//end of if
    else {
      currentConsec = 0;
    }//end of else
  }//end of while

  //small delay for the sd card
  delay(50);
  fileOpen.close();

}//end of writeSampleToSD


/*
* Function Name:
*
*   storeSampleData
*
* Description:
*
*   coordinates the functions involved with trimming and writing data to a file on the SD card.
*
* Parameters:
*
*   N/A
*
* Returns:
*
*   N/A
*/
void storeSampleData() {

  //get index of the new sample file
  int index = config_file[0].toInt();

  //update the index in the config file
  Serial.println("Updating Config File Index");
  config_file[0] = String(index + 1);
  writeConfig();

  //create name for new sample file
  String fileName = "SAMPLE" + String(index) + ".csv";

  //delete old file if it exists
  Serial.println("Removing old file");
  SD.remove(fileName);

  //make new file for sampl
  Serial.println("Creating New file: " + fileName);
  fileOpen = SD.open(fileName, FILE_WRITE);
  fileOpen.close();

  //check file has been made
  if (!(SD.exists(fileName))) {
    fatalErrorHandler("Error Creating File: " + fileName);
  }//end of check if file exists

  Serial.println(fileName + " Successfully Created");
  Serial.println("Waiting for Voltage to Drop Below 1.2V");
  startReading();
  Serial.println("Voltage dropped below 1.2V");
  Serial.println("Writing Analog Input to " + fileName);
  writeSampleToSD(fileName);
  Serial.println("Input Written To " + fileName + " on SD card");

}//end of writeSampleData


/*
* Function Name:
*
*   sum
*
* Description:
*
*   Takes in an array and adds up the values of all the elements in the array.
*
* Parameters:
*
*   double[]  ar  the values to sum
*   int  arLen  the length of the array with values to sum
*
* Returns:
*
*   double  sum  the sum of the inputs
*/
double sum (double ar[], int arLen) {
  double fullSum = 0;
  for (int i = 0; i < arLen; i++) {
    fullSum += ar[i];
  }//end of for
  return fullSum;
}//end of sum

/*
* Function Name:
*
*   linearEquation
*
* Description:
*
*   Takes in a set of data points and the amount of data points and then performs linear regression on them and returns a slope.
*
* Parameters:
*
*   double[]  x  the values for the x-axis of the data points
*   double[]  y  the values for the y-axis of the data points
*   int  xLen  the length of the x values
*   int  yLen  the length of the y values
*
* Returns:
*
*   double  m  returns the calculated slope from the points where m is y=mx+b
*
*/
double linearEquation(double x[], double y[], int xLen, int yLen) {
  double xavg = sum(x, xLen) / xLen;
  double yavg = sum(y, yLen) / yLen;
  double tempAdd = 0;
  for (int i = 0; i < xLen || i < yLen; i++) {
    tempAdd += x[i] * y[i];
  }//end of for
  double numer = tempAdd - xLen * xavg * yavg;
  tempAdd = 0;
  for (int i = 0; i < xLen; i++) {
    tempAdd += pow(x[i], 2);
  }//end of for
  double denum = tempAdd - xLen * pow(xavg, 2);
  double m = numer / denum;
  return m;
}//end of linearEquation


/*
* Function Name:
*
*   calculateFluoride
*
* Description:
*
*   This function in a slope and a model and uses the model as a flag to figure out if the
*   linear or polynomial model will be used to calculate the fluoride concentration. Then,
*   the function utilises the input slope either through passing in a value to a polynomial
*   of variable degree defined in constants or through a linear equation and then returns
*   the estimated fluoride concentration.
*
* Parameters:
*
*   double  slope  the slope of the points to use in calculation
*
*   String  model  the model being used to caluclate the fluoride concentration
*
* Returns:
*
*   double  fluorideConcentration  the calculated fluoride concentration in ppm
*/
double calculateFluoride(double slope, String model) {
  if (model == "linear") {
    return slope*translationSlope+translationIntercept;
  }//end of if
  else if (model == "polynomial") {
    double finalOutput = 0;
    for (int i = 0; i < polynomialCoefficientsLength; i++) {
      double temp = polynomialCoefficients[i]*pow(slope, i);
      finalOutput += temp;
    }//end of for
    return finalOutput;
  }//end of else if
}//end of calculateFluoride

/*
* Function Name:
*
*   processSampleData
*
* Description:
*
*   This function takes the xPoints and yPoints collected from a sample file and gets the linear slope then fits the slope to either a polynomial or linear calibration curve to get a fluoride value.
*
* Parameters:
*
*   N/A
*
* Returns:
*
*   double  fluorideConcentration  the calculated fluoride concentration in ppm
*/
double processSampleData(){
 double slope = linearEquation(xPoints, yPoints, dataPointsLength, dataPointsLength);
 return calculateFluoride(slope, "polynomial");
}//end of processSampleData

/*
* Function Name:
*
*   setupPinModes
*
* Description:
*
*   Setups the modes for the pins of the microcontroller.
*
* Parameters:
*
*   N/A
*
* Returns:
*
*   N/A
*/
void setupPinModes() {
  pinMode(selectPin, INPUT);
  pinMode(enterPin, INPUT);
}//end of setupPinModes

/*
* Function Name:
*
*   setupSDCard
*
* Description:
*
*   Setups the SPI connection between the microcontroller and the SD Card module.
*
* Parameters:
*
*   N/A
*
* Returns:
*
*   N/A
*/
void setupSDCard() {
  if (!SD.begin(chipSelectPin)) {
    fatalErrorHandler("Unable to Initialize SD Card. Exiting Program Now");
  }//end of if
}//end of setupSDCard

/*
* Function Name:
*
*   setup
*
* Description:
*
*   Begins Software Serial at a baudrate of 57600, setups input and output for electrical pins, and load config file.
*
* Parameters:
*
*   N/A
*
* Returns:
*
*   N/A
*/
void setup() {
  Serial.begin(57600);
  setupPinModes();
  Serial.println("pins setup");
  setupSDCard();
  Serial.println("sd card initalized");
  loadConfig();
  Serial.println("config file loaded");
  loadSampleData(0);
}//end of setup


/*
* Function Name:
*
*  buttons
*
* Description:
*
*  Waits in a loop until the enter or the select button is in the up state and then is pressed down.
*  Returns an integer corresponding to the button pressed.
*
* Parameters:
*
*   N/A
*
* Returns:
*
*  int  choice  The users choice of button to press in int repersentation: 0 is select, 1 is enter.
*/
int buttons() {

  int historicSelectState = digitalRead(selectPin);
  int historicEnterState = digitalRead(enterPin);

  while (true) {

    delay(20);

    selectState = digitalRead(selectPin);
    enterState = digitalRead(enterPin);

    if (selectState == 1 && historicSelectState == 0) {
      return 0;
    }//end of if

    if (enterState == 1 && historicEnterState == 0) {
      return 1;
    }//end of if

    historicSelectState = selectState;
    historicEnterState = enterState;
  }//end of while
}//end of button

/*
* Function Name:
*
*   loop
*
* Description:
*
*   !!!
*
* Parameters:
*
*   N/A
*
* Returns:
*
*   N/A
*/
void loop() {
  delay(100);
}//end of loop
