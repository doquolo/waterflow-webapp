#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <AltSoftSerial.h>

#include <SFE_BMP180.h>
#include <Wire.h>

#define ALTITUDE 1655.0 // Altitude of SparkFun's HQ in Boulder, CO. in meters
#define loa 13
#define motor1 7
#define motor2 6
#define set 5
#define ledStt 4

#define rxPin 2
#define txPin 3
SoftwareSerial sim800L(rxPin,txPin); 
AltSoftSerial neogps(9,8);
//GPS Module RX pin to Arduino 9
//GPS Module TX pin to Arduino 8
TinyGPSPlus gps;
SFE_BMP180 pressure;
unsigned long previousMillis = 0;
long interval = 60000;
int valSet = 0;
String sendtext;

void setup()
{
//...............BMP.....................
  pinMode (13,OUTPUT); // speaker
  pinMode (ledStt,OUTPUT); 
  pinMode (motor2,OUTPUT); 
  pinMode (motor1,OUTPUT); 
  pinMode (set,INPUT); 
  
  digitalWrite(13,LOW);
  digitalWrite(ledStt,LOW);
  Serial.begin(9600);
  Serial.println("REBOOT");
  if (pressure.begin())
    Serial.println("BMP180 init success");
  else
  {
    Serial.println("BMP180 init fail\n\n");
    while(1); // Pause forever.
  }

//.......................................
  
  //Begin serial communication with Arduino and Arduino IDE (Serial Monitor)
  Serial.begin(115200);
 
  //Begin serial communication with Arduino and SIM800L
  sim800L.begin(9600);

  //Begin serial communication with Arduino and SIM800L
  neogps.begin(9600);

  Serial.println("Initializing...");
  //delay(10000);

  //Once the handshake test is successful, it will back to OK
  sendATcommand("AT", "OK", 2000);
  sendATcommand("AT+CMGF=1", "OK", 2000);
  //sim800L.print("AT+CMGR=40\r");
}

void loop()
{
  while(sim800L.available()){
    Serial.println(sim800L.readString());
  }
  while(Serial.available())  {
    sim800L.println(Serial.readString());
  }

    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis > interval) {
       previousMillis = currentMillis;
       sendGpsToServer();
    }
  if (digitalRead(set) == HIGH)
  {
    valSet = 1;
  }
  if (valSet == 1)
  {
    digitalWrite(ledStt,HIGH);
    sensor();
  }
}

int sendGpsToServer()
{
    //Can take up to 60 seconds
    boolean newData = false;
    for (unsigned long start = millis(); millis() - start < 2000;){
      while (neogps.available()){
        if (gps.encode(neogps.read())){
          newData = true;
          break;
        }
      }
    }
  
    //If newData is true
    if(true){
      newData = false;
      
      String latitude, longitude;
      float altitude;
      unsigned long date, time, speed, satellites;
  
      latitude = String(gps.location.lat(), 6); // Latitude in degrees (double)
      longitude = String(gps.location.lng(), 6); // Longitude in degrees (double)
      altitude = gps.altitude.meters(); // Altitude in meters (double)
      date = gps.date.value(); // Raw date in DDMMYY format (u32)
      time = gps.time.value(); // Raw time in HHMMSSCC format (u32)
      speed = gps.speed.kmph();
      sendtext = "Canh bao : Phao bung o vi tri :  "+latitude+"   "+longitude;
      Serial.print("Latitude= "); 
      Serial.print(latitude);
      Serial.print(" Longitude= "); 
      Serial.println(longitude);
  
      //if (latitude == 0) {return 0;}
      
      String url, temp;
      url = "http://gpslocationdn.000webhostapp.com/gpsdata.php?lat=";
      url += latitude;
      url += "&lng=";
      url += longitude;

      //url = "http://ahmadssd.000webhostapp.com/gpsdata.php?lat=222&lng=222";

      Serial.println(url);    
      delay(300);
          
    sendATcommand("AT+CFUN=1", "OK", 2000);
    //AT+CGATT = 1 Connect modem is attached to GPRS to a network. AT+CGATT = 0, modem is not attached to GPRS to a network
    sendATcommand("AT+CGATT=1", "OK", 2000);
    //Connection type: GPRS - bearer profile 1
    sendATcommand("AT+SAPBR=3,1,\"Contype\",\"GPRS\"", "OK", 2000);
    //sets the APN settings for your network provider.
    sendATcommand("AT+SAPBR=3,1,\"APN\",\"internet\"", "OK", 2000);
    //enable the GPRS - enable bearer 1
    sendATcommand("AT+SAPBR=1,1", "OK", 2000);
    //Init HTTP service
    sendATcommand("AT+HTTPINIT", "OK", 2000); 
    sendATcommand("AT+HTTPPARA=\"CID\",1", "OK", 1000);
    //Set the HTTP URL sim800.print("AT+HTTPPARA="URL","http://ahmadssd.000webhostapp.com/gpsdata.php?lat=222&lng=222"\r");
    sim800L.print("AT+HTTPPARA=\"URL\",\"");
    sim800L.print(url);
    sendATcommand("\"", "OK", 1000);
    //Set up the HTTP action
    sendATcommand("AT+HTTPACTION=0", "0,200", 1000);
    //Terminate the HTTP service
    sendATcommand("AT+HTTPTERM", "OK", 1000);
    //shuts down the GPRS connection. This returns "SHUT OK".
    sendATcommand("AT+CIPSHUT", "SHUT OK", 1000);

  }
  return 1;    
}

int8_t sendATcommand(char* ATcommand, char* expected_answer, unsigned int timeout){

    uint8_t x=0,  answer=0;
    char response[100];
    unsigned long previous;

    //Initialice the string
    memset(response, '\0', 100);
    delay(100);
    
    //Clean the input buffer
    while( sim800L.available() > 0) sim800L.read();
    
    if (ATcommand[0] != '\0'){
      //Send the AT command 
      sim800L.println(ATcommand);
    }

    x = 0;
    previous = millis();

    //this loop waits for the answer with time out
    do{
        //if there are data in the UART input buffer, reads it and checks for the asnwer
        if(sim800L.available() != 0){
            response[x] = sim800L.read();
            //Serial.print(response[x]);
            x++;
            // check if the desired answer (OK) is in the response of the module
            if(strstr(response, expected_answer) != NULL){
                answer = 1;
            }
        }
    }while((answer == 0) && ((millis() - previous) < timeout));

  Serial.println(response);
  return answer;
}

void SendSMS()
{
  Serial.println("Sending SMS...");               //Show this message on serial monitor
  sim800L.print("AT+CMGF=1\r");                   //Set the module to SMS mode
  delay(100);
  sim800L.print("AT+CMGS=\"phone number here\"\r");  //Your phone number don't forget to include your country code, example +8439548596"
  delay(500);
  sim800L.print(sendtext);       //This is the text to send to the phone number, don't make it too long or you have to modify the SoftwareSerial buffer
  delay(500);
  sim800L.print((char)26);// (required according to the datasheet)
  delay(500);
  sim800L.println();
  Serial.println("Text Sent.");
  delay(500);
}
void sensor()
{
  char status;
  double T,P,p0,a;
  Serial.println();
  Serial.print("provided altitude: ");
  Serial.print(ALTITUDE,0);
  Serial.print(" meters, ");
  Serial.print(ALTITUDE*3.28084,0);
  Serial.println(" feet");
  status = pressure.startTemperature();
  if (status != 0)
  {
    delay(status);          // Wait for the measurement to complete
    status = pressure.getTemperature(T);
    if (status != 0)
    {
      Serial.print("temperature: ");
      Serial.print(T,2);
      Serial.print(" deg C, ");
      Serial.print((9.0/5.0)*T+32.0,2);
      Serial.println(" deg F");
      status = pressure.startPressure(3);
      if (status != 0)
      {
        delay(status);
        status = pressure.getPressure(P,T);
        if (status != 0)
        {
          Serial.print("absolute pressure: ");
          Serial.print(P,2);
          Serial.print(" mb, ");
          Serial.print(P*0.0295333727,2);
          Serial.println(" inHg");
          p0 = pressure.sealevel(P,ALTITUDE); // we're at 1655 meters (Boulder, CO)
          float P1 = p0*0.010197162129779283;
          if (P1 > 12.9)
            {
              digitalWrite(13,HIGH);
              for (int i = 1; i<=3;i++)
              {
                digitalWrite(motor2,LOW);
                digitalWrite(motor1,HIGH);
                delay(500);
                digitalWrite(motor1,LOW);
                digitalWrite(motor2,HIGH);
                delay(200);
              }
              SendSMS();
            }
          Serial.print("relative (sea-level) pressure: ");
          Serial.print(p0*0.010197162129779283);
          Serial.print("     ");
          Serial.print(p0,2);
          Serial.print(" mb, ");
          Serial.print(p0*0.0295333727,2);
          Serial.println(" inHg");
          a = pressure.altitude(P,p0);
          Serial.print("computed altitude: ");
          Serial.print(a,0);
          Serial.print(" meters, ");
          Serial.print(a*3.28084,0);
          Serial.println(" feet");
        }
        else Serial.println("error retrieving pressure measurement\n");
      }
      else Serial.println("error starting pressure measurement\n");
    }
    else Serial.println("error retrieving temperature measurement\n");
  }
  else Serial.println("error starting temperature measurement\n");

  delay(5000);  // Pause for 5 seconds.
}

//-----------------------------------------------------------------------------------------------------------------------------
//boolean sendATcommand(String expected_answer="OK", unsigned int timeout=2000) //uncomment if syntax error (arduino)
/*
boolean sendATcommand(String ATcommand, String expected_answer, unsigned int timeout) //uncomment if syntax error (esp8266)
{
  uint8_t x=0, answer=0;
  String response;
  unsigned long previous;
    
  //Clean the input buffer
  while( SIM800.available() > 0) SIM800.read();
  sim800L.println(ATcommand);
//NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
  previous = millis();
  do{
    //if data in UART INPUT BUFFER, reads it
    if(SIM800.available() != 0){
        char c = SIM800.read();
        response.concat(c);
        x++;
        //checks if the (response == expected_answer)
        if(response.indexOf(expected_answer) > 0){
            answer = 1;
        }
    }
  }while((answer == 0) && ((millis() - previous) < timeout));
  //NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
  Serial.println(response);
  return answer;
} 
*/
//-----------------------------------------------------------------------------------------------------------------------------

