#include "Parser.h"
#include "bot.h"


void Parser::logDataReceied(double x, double y, double q0, double q1){
  Serial.print("Received coords: X= ");
  Serial.print(x);
  Serial.print(" | y= ");
  Serial.print(y);
  Serial.print(" || output angles: q0= ");
  Serial.print(q0 * RAD_TO_DEG);
  Serial.print(" | q1= ");
  Serial.print(q1 * RAD_TO_DEG);
  Serial.print(" || steps: S0= ");
  Serial.print(q0);
  Serial.print(" q1= ");
  Serial.println(q1);
}

void Parser::ParseInput(double &x, double &y){
    if(Serial.available()){
        String rxString = "";
        String strArr[2]; // number of inputs goes here
        while (Serial.available()) {
            //Delay to allow byte to arrive in input buffer.
            delay(2);
            char ch = Serial.read();
            rxString+= ch;
        }

        int stringStart = 0;
        int arrayIndex = 0;
        for (int i=0; i < (int)rxString.length(); i++){
            //Get character and check if it's our "special" character.
            if(rxString.charAt(i) == ','){
                strArr[arrayIndex] = ""; //Clear previous values from array.
                strArr[arrayIndex] = rxString.substring(stringStart, i); //Save substring into array.
                stringStart = (i+1);
                arrayIndex++;
            }
        }

        x = strArr[0].toDouble();
        y = strArr[1].toDouble();
        parseState = true;
    }
}


bool Parser::read_input(char (&serial_data) [MAX_MSG_LEN])
{
  uint8_t index = 0;
  if (Serial.available() > 0) {
    while (Serial.available() > 0) {
      delayMicroseconds(200); // lowest i could get working
      char newchar = Serial.read();
      if ((newchar != '\n') and (index < MAX_MSG_LEN)) {
        serial_data[index] = newchar;
        index++;
      }
      else {
        break;
      }
    }
    return true;
  }
  return false;
}

void Parser::clear_data(char (&serial_data) [MAX_MSG_LEN]) {
  for (uint16_t i = 0; i < MAX_MSG_LEN; i++) {
    serial_data[i] = '\0';
  }
}

void Parser::parse_inputs(char serial_data[MAX_MSG_LEN], std::vector<std::string> &args) {
    char delim= ' ';
    uint32_t index= 0;
    std::string tmp_str;
    args.clear();

    while (serial_data[index] != '\0') {
        tmp_str += serial_data[index];
        index++;
        if (serial_data[index] == delim) {
            args.push_back(tmp_str);
            tmp_str = "";
            index++;
        }
        // timeout
        if (index > MAX_MSG_LEN) return;
    }
    args.push_back(tmp_str);
}

void Parser::parse_int(std::string inpt, char &cmd, int &value) {
    
    cmd = inpt[0];
    char tmp_char[3]; // commands are no higher tan 999
    char *p = tmp_char;

    for (uint32_t i = 1; i < inpt.length(); i++) {
        *p = inpt[i];
        p++;
    }
    //value = stoi(temp_arg_char);
    value = (int)strtol(tmp_char, nullptr, 10);
}

void Parser::parse_floats(std::string inpt, char &cmd, double &value) {

    cmd = inpt[0];
    char temp_arg_char[8]; // commands are no higher than s9999.00
    char *p = temp_arg_char;

    for (uint32_t i = 1; i < inpt.length(); i++) {
        *p = inpt[i];
        p++;
    }

    value = strtod(temp_arg_char, nullptr);
}


void Parser::update_commands(std::vector<std::string> inputs){

    __commands.clear();
    __values.clear(); 

    if (inputs.size() == 1) // there´s only mode command
        return;

    for(uint32_t arg_i = 1; arg_i < inputs.size(); arg_i++) // desde adelante del comando 1
    {
        char char_value;
        double dob_value;
        parse_floats(inputs[arg_i], char_value, dob_value);

        __commands.push_back(tolower(char_value));
        __values.push_back(dob_value);
    }
}

double Parser::get(char key_cmd){
    auto it = std::find(__commands.begin(), __commands.end(), key_cmd);
    if (it != __commands.end())
        return __values[std::distance(__commands.begin(), it)];

    return _NOCMD_;
}

// ###############################
// ######### LED class ###########
// ###############################


LEDIndicator::LEDIndicator(uint8_t r_pin, uint8_t g_pin, uint8_t b_pin){

    __R_pin = r_pin;
    __G_pin = g_pin;
    __B_pin = b_pin;

    pinMode(__R_pin, OUTPUT);
    pinMode(__G_pin, OUTPUT);
    pinMode(__B_pin, OUTPUT);
}

void LEDIndicator::change_colors(uint16_t* RGB){
    __R = RGB[0];
    __G = RGB[1];
    __B = RGB[2];
    light();
}

void LEDIndicator::light(){
    analogWrite(__R_pin, __R);
    analogWrite(__G_pin, __G);
    analogWrite(__B_pin, __B);
}

void LEDIndicator::fade(uint64_t t){
    analogWrite(__R_pin, __R * abs(sin(2 * PI * 1 * t)));//millis())));
    analogWrite(__G_pin, __G * abs(sin(2 * PI * 1 * t)));//millis())));
    analogWrite(__B_pin, __B * abs(sin(2 * PI * 1 * t)));// millis())));
}
