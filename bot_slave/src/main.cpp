#include <Arduino.h>
#include <Servo.h>

#include "bot.h"
#include "Parser.h"
#include "StepperLib.h"
#include "figures.h"

#define BAUD_RATE 115200

Bot bot; // initialize bot instance
Parser parser; // initialize parser
Stepper m0, m1;
LEDIndicator led(9, 10, 11);

char serialData[MAX_MSG_LEN];

// #################################
// MAIN LOOP AND SETUP
// #################################  

void setup() {
  Serial.begin(BAUD_RATE);
  Serial.println("Bot initalized\n");
  bot.enableMotors();
}

void loop() {
  char base_cmd;
  int base_val;
  char input_data[MAX_MSG_LEN];
  bool joy = false;
  bool fade = false;
  float freq = 1;


  while (true){
    parser.clear_data(input_data);

    if (parser.read_input(input_data)){

      std::vector<std::string> args;
      parser.parse_inputs(input_data, args);
      parser.parse_int(args[0], base_cmd, base_val);
      parser.update_commands(args);
      //led.light();
      // Serial.print("data sent: ");
      // Serial.println(input_data);
      // Serial.print("base cmd= ");
      // Serial.print(base_cmd);
      // Serial.print(" base val= ");
      // Serial.print(base_val);
      // Serial.print(" x= ");
      // Serial.print(parser.fetch('x'));
      // Serial.print(" y= ");
      // Serial.print(parser.fetch('y'));
      // Serial.print(" speed= ");
      // Serial.println(parser.fetch('f'));
      // Serial.println(" ");

      switch (tolower(base_cmd)) {
          case 'g': {
            switch (base_val) {
              case 0: { // move motor linear no accel
                bot.move_motor_linear_no_accel(
                  parser.get('x'), parser.get('y'), parser.get('f'));
                break;
              }

              case 1: {
                //bot.enableMotors();
                bot.move_motor_linear(
                  parser.get('x'), parser.get('y'), parser.get('f'));
                //bot.disbleMotors();
                break;
              }

              case 90: {
                // Absolute positioning
                bot.set_move_mode(true);
                break;
              }

              case 91: {
                // Relative positioning
                bot.set_move_mode(false);
                break;
              }

              default: break;
            }
            break;
          } // end case G

          case 'm': {
            switch(base_val) {
              case 3: { // no recuerdo si este es servo up o down
                bot.pen_up();
                break;
              }

              case 5: {
                bot.pen_down();
                break;
              }
              
              case 17: {
                bot.enableMotors();
                break;
              }
              
              case 84: {
                bot.disbleMotors();
                break;
              }

              case 69: {
                bot.joystick_mode(true);
                joy = true; 
                break;
              }

              case 70: {
                bot.joystick_mode(false);
                joy = false;
                break;
              }

              default: break;
            }
            break;
          }

          case 'c': {
            switch (base_val) {
              case 0: {
                led.change_colors(led.error_rgb);
                break;
              }

              case 1: {
                led.change_colors(led.ok_rgb);
                break;
              }

              case 2: {
                led.change_colors(led.calibration_rgb);
                break;
              }

              case 3:{
                led.change_colors(led.bot_calculating_rgb);
                break;
              }

              case 4: {
                led.change_colors(led.win_rgb);
                break;
              }

              case 5: {
                fade = true;
                freq = parser.get('w');
                freq = freq == _NOCMD_ ? 1 : freq;
                break;
              }

              case 6: {
                fade = false;
                led.light();
                break;
              }

              case 7:{
                led.change_colors(led.human_turn);
                break;
              }

              case 8: {
                led.change_colors(led.tie_rgb);
                break;
              }

              case 9: {
                led.change_colors(led.off);
                break;
              }

              default: break;
            }
            break;
          }

          default: break;
      }

      Serial.println("ok"); // respond to master
    }

    if (joy)
    {
      bot.joystick_run();
    } 

    if (fade) {
      analogWrite(led.__R_pin, led.__R * abs(sin(2 * PI * freq * millis() / 1000)));
      analogWrite(led.__G_pin, led.__G * abs(sin(2 * PI * freq * millis() / 1000)));
      analogWrite(led.__B_pin, led.__B * abs(sin(2 * PI * freq * millis() / 1000)));
    }
  }
}

/* 
C5 W0.5
C0
C1
C2
C3
C4
C6
C7
C8
C9

100,100,
81.5,82,

M5
M3
M6
M17
G1 X100.2 Y100.5 F1000.5
G1 X100.0 Y100.0 
G1 X100 Y100 F100
G1 X81.5 Y82.0 F200.0
G1 X-70.0 Y80.0 F200.0
G1 X-100.0 Y60.0 F400.0

para probar abs y rel mode
G90 -> abs
G91 -> rel

G1 X20.0 Y20.0 F200.0
G1 X0.0 Y20.0 F200.0
G1 X-10.0 Y-10.0 F200.0
G1 X-20.0 Y0.0 F200.0
G1 X-2.0 Y0.0 F200.0
G1 X2.0 Y2.0 F200.0
G1 X
M84
M17
M69
M70

*/
