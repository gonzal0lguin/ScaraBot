#ifndef BOT_SLAVE_PARSER_H
#define BOT_SLAVE_PARSER_H

#include <Arduino.h>
#include <ArduinoSTL.h>

#define MAX_MSG_LEN 100


class Parser { 
    public:
        // VARIABLES
        bool parseState = false;

        // FUNCTIONS
        void logDataReceied(double x, double y, double q0, double q1);
        void ParseInput(double &x, double &y);
        bool read_input(char (&serial_data) [MAX_MSG_LEN]);
        void clear_data(char (&serial_data) [MAX_MSG_LEN]);
        void parse_inputs(char serial_data[MAX_MSG_LEN], std::vector<std::string> &args);
        void parse_int(std::string inpt, char &cmd, int &value);
        void parse_floats(std::string inpt, char &cmd, double &value);
        void update_commands(std::vector<std::string> inputs);
        double get(char key_cmd);
        
    private:
        std::vector<char> __commands;
        std::vector<double> __values;
};

class LEDIndicator {
    public:
        LEDIndicator(uint8_t r_pin, uint8_t g_pin, uint8_t b_pin);
        void change_colors(uint16_t* RGB);
        void light();
        void fade(uint64_t t);

        uint16_t error_rgb[3] = {255, 0, 0};                // C0
        uint16_t ok_rgb[3] = {0, 255, 0};                   // C1
        uint16_t calibration_rgb[3] = {255, 0, 255};        // C2
        uint16_t bot_calculating_rgb[3] = {0, 255, 255};    // C3
        uint16_t win_rgb [3]= {255, 255, 0};                // C4
        uint16_t human_turn[3] {20, 100, 255};
        uint16_t tie_rgb[3] = {125, 200, 90};
        uint16_t off[3] = {0, 0, 0};

        uint16_t __R = 0;
        uint16_t __G = 0;
        uint16_t __B = 0;
        uint8_t __R_pin;
        uint8_t __G_pin;
        uint8_t __B_pin;
};

#endif