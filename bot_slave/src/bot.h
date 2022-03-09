#ifndef BOT_SLAVE_BOT_H
#define BOT_SLAVE_BOT_H

#include <Arduino.h>
#include <math.h>
#include <Servo.h>

#include "StepperLib.h"

#define _NOCMD_ 99999

#define stepPin1 4
#define dirPin1 5
#define enPin1 3
#define stepPin2 7
#define dirPin2 8
#define enPin2 6
#define servo_pin 2

#define joy_x A2
#define joy_y A1
#define joy_btn 12

class Bot {
    
    public:
        // VARIABLES AND CONSTANTS
        double q0= 0, q1= 0; // angulos se inicializan con IK
        double x= __L1_mm, y= __L2_mm; 

        // MOTORS
        Stepper m0, m1;
        Servo servo;

        // FUNCTIONS 
        Bot(); // constructor 
        void home();
        void go_home();
        void initMotors();
        void enableMotors();
        void disbleMotors();
        void set_move_mode(bool abs_true);
        void pen_up();
        void pen_down();
        double scale_M1_speed(Stepper mx, double mx_speed, double S0, double S1);
        void move_motor_linear(double x_target, double y_target, double vmax);
        void move_motor_linear_no_accel(double x_target, double y_target, double vmax);
        void forward_kinematics(double &x, double &y, double q0, double q1);
        bool inverse_kinematics(double &q0, double &q1, double x, double y);
        void joystick_mode(bool joy_true);
        void joystick_run();

    private:
        bool __absmode = true;
        bool __joymode = false;
        bool __joybtn_pressed = false;
        float __vel = 500.0;
        float __accel = 1500.0;
        double __L1_mm = 81.5;
        double __L2_mm = 82.0;
        double __L12_mm = __L1_mm + __L2_mm;
        int8_t __servoUp_deg = 65;
        int8_t __servoDown_deg = 90;
        uint16_t __servoDelay_ms = 320;
};

#endif 

