#include "Wire.h"
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

const int addr = 0x08;  // slave address
const int busy = 9;     // busy pin of DFPlayer
byte c1;                // command

SoftwareSerial mySoftwareSerial(10, 11);        // IO10をRX, IO11をTXとしてアサイン
DFRobotDFPlayerMini myDFPlayer;

void handler(int num_bytes)
{
    if (num_bytes == 1) {
        c1 = Wire.read();
        switch (c1) {
            case 0x81: myDFPlayer.volumeDown(); break;
            case 0x82: myDFPlayer.volumeUp(); break;
            case 0x21: myDFPlayer.previous(); break;
            case 0x22: myDFPlayer.next(); break;
            case 0x01: myDFPlayer.stop(); break;
            default:
                if (c1 & 0x40) {
                    int song = int(c1 & 0x0f);
                    myDFPlayer.play(song);
                }
        }
    }
}


void setup()
{
    Wire.begin(addr);
    Wire.onReceive(handler);
    pinMode(busy, INPUT);

    mySoftwareSerial.begin(9600);   // Communicate with DFPlayer

    // For debugging
    Serial.begin(9600);
    Serial.println();
    Serial.println(F("DFRobot DFPlayer Mini Demo"));
    Serial.println(F("Initializing DFPlayer ... (May take 3~5 seconds)"));
 
    // Initialize DFPlayer 
    if (!myDFPlayer.begin(mySoftwareSerial)) {
        Serial.println(F("Unable to begin:"));
        Serial.println(F("1.Please recheck the connection!"));
        Serial.println(F("2.Please insert the SD card!"));
        while (true) {
            delay(0);
        }
    }
    Serial.println(F("DFPlayer Mini online."));
 
    myDFPlayer.volume(20);
    myDFPlayer.play(1);
}

#define DEBUG
void loop()
{
#ifdef DEBUG
    Serial.print("c1:");
    Serial.print(c1, HEX);
    Serial.print(" BUSY:");
    Serial.println(digitalRead(busy));      // HIGH free, LOW is BUSY
    delay(1000);
#endif
}
