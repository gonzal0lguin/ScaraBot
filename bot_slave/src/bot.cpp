#include "bot.h"

Bot::Bot(){
    m0.init(stepPin1, dirPin1, enPin1, false);
    m1.init(stepPin2, dirPin2, enPin2, false);

    m0.update_config(1600);

    inverse_kinematics(x, y, q0, q1); // sets start position
    // m0.overwrite_pos((int32_t) q0 * 1600 / (2*PI));

    pinMode(joy_btn, INPUT_PULLUP);

}

void Bot::home(){
    // M0.setCurrentPosition(0);
    // M1.setCurrentPosition(PI / 2 * RAD_M1_TO_STEPS);
}

void Bot::go_home(){
    move_motor_linear(__L1_mm, __L2_mm, __vel);
}

void Bot::enableMotors(){
    m0.enable();
    m1.enable();
}

void Bot::disbleMotors(){
    m0.disable();
    m1.disable();
}

void Bot::set_move_mode(bool abs_true)
{
  __absmode = abs_true;
}

void Bot::pen_up(){
    servo.attach(servo_pin);
    servo.write(__servoUp_deg);
    delay(__servoDelay_ms);
    servo.detach();
}

void Bot::pen_down(){
    servo.attach(servo_pin);
    servo.write(__servoDown_deg);
    delay(__servoDelay_ms);
    servo.detach();
}

// #################################
// KINEMATICS
// #################################  

double Bot::scale_M1_speed(Stepper mx, double mx_speed, double S0, double S1){
    double _S1 = abs(S1 - mx.get_steps());
    double _S0 = abs(S0 - mx.get_steps());
    return mx_speed * _S1 / _S0;
}

void Bot::move_motor_linear(double x_target, double y_target, double vmax){

    vmax = vmax == _NOCMD_ ? __vel : vmax;

    double x_start, y_start;
    forward_kinematics(x_start,y_start,q0,q1);

    // change targets if relative mode is set, this means it will travel the
    // distance commanded no matter what the current position is

    // Serial.print(x_target);
    // Serial.print("  ");
    // Serial.println(y_target);

    if (!__absmode){
        x_target = x_target == _NOCMD_ ? x_start : x_start + x_target;
        y_target = y_target == _NOCMD_ ? y_start : y_start + y_target;
    }
    else {
        x_target = x_target == _NOCMD_ ? x_start : x_target;
        y_target = y_target == _NOCMD_ ? y_start : y_target;
    } 

    // calculate total distance and accelerated distance [mm]
    float move_dist_mm = sqrt(pow(x_target - x_start, 2) + pow(y_target - y_start, 2));
    // Serial.print("move dist= ");
    // Serial.println(move_dist_mm);

    if (move_dist_mm == 0.0) {
        //Serial.println("se returneo");
        return;
        }

    float accel_dist_mm = pow(vmax, 2) / (2 * __accel);

    if(move_dist_mm < (2 * accel_dist_mm)){
        accel_dist_mm = move_dist_mm / 2;
    }

    float inflect_t0_s = sqrt((2 * accel_dist_mm) / __accel); // time to accelerate
    float inflect_t1_s = inflect_t0_s + (move_dist_mm - (2 * accel_dist_mm)) / vmax;
    float move_time_s = inflect_t1_s + inflect_t0_s; // total time

    // Calculate when to take steps on the fly 
    uint8_t motion_state = 0; // 0: accelerating, 1: plateau, 2: decelerating, 3: finalize
    uint32_t t_start = micros();
    uint32_t t_step;

    float linear_dist_mm, t_elapsed_s, move_percent;
    double xtar_mm, ytar_mm;

    while(true)
    {
        t_step = micros();
        t_elapsed_s = t_step - t_start;
        t_elapsed_s /= 1000000;

        switch(motion_state) {
            case 0: {
                linear_dist_mm = (__accel * pow(t_elapsed_s, 2)) / 2;
                if(t_elapsed_s > inflect_t0_s) motion_state++;
                break;
            }
            case 1: {
                linear_dist_mm = accel_dist_mm + vmax * (t_elapsed_s - inflect_t0_s);
                if(t_elapsed_s > inflect_t1_s) motion_state++;
                break;
            }
            case 2: {
                linear_dist_mm = move_dist_mm - ((__accel * pow(move_time_s - t_elapsed_s, 2)) / 2);
                if(t_elapsed_s > move_time_s) motion_state++;
                break;
            }
            case 3: {
                linear_dist_mm = move_dist_mm;
                break;
            }
        }

        move_percent = linear_dist_mm / move_dist_mm;
        xtar_mm = x_start + move_percent * (x_target - x_start);
        ytar_mm = y_start + move_percent * (y_target - y_start);

        if (inverse_kinematics(q0, q1, xtar_mm, ytar_mm))
        {
            m1.set_rad_target(q0+q1);
            m0.set_rad_target(q0); 
        } else break;

        bool stepped1= false, stepped2= false;
        stepped1 = m0.step_if_needed() ? true : stepped1;
        stepped2 = m1.step_if_needed() ? true : stepped2;

        if(motion_state == 3 && !stepped1 && !stepped2) break;
    }
}

void Bot::move_motor_linear_no_accel(double x_target, double y_target, double vmax){

    vmax = vmax == _NOCMD_ ? __vel:vmax;

    double x_start, y_start;
    forward_kinematics(x_start,y_start,q0,q1); // creo que basta con usar bot.x y bot.y xd
    // double x_start = x; double y_start = y;

    if (!__absmode){
        x_target = x_target == _NOCMD_ ? x_start : x_start + x_target;
        y_target = y_target == _NOCMD_ ? y_start : y_start + y_target;
    }
    else {
        x_target = x_target == _NOCMD_ ? x_start : x_target;
        y_target = y_target == _NOCMD_ ? y_start : y_target;
    }  

    // calculate total distance and accelerated distance [mm]
    float move_dist_mm = sqrt(pow(x_target - x_start, 2) + pow(y_target - y_start, 2));
    if (move_dist_mm == 0.0) return;

    float move_time_s = move_dist_mm / vmax; // total time

    // Calculate when to take steps on the fly 
    uint8_t motion_state = 0; // 0: accelerating, 1: plateau, 2: decelerating, 3: finalize
    uint32_t t_start = micros();
    uint32_t t_step;

    float linear_dist_mm, t_elapsed_s, move_percent;
    double xtar_mm, ytar_mm;

    while(true)
    {
        t_step = micros();
        t_elapsed_s = t_step - t_start;
        t_elapsed_s /= 1000000;

        switch(motion_state) {
            case 0: {
                linear_dist_mm = vmax * t_elapsed_s;
                if(t_elapsed_s > move_time_s) motion_state++;
                break;
            }

            case 1: {
                linear_dist_mm = move_dist_mm;
                break;
            }
        }

        move_percent = linear_dist_mm / move_dist_mm;
        xtar_mm = x_start + move_percent * (x_target - x_start);
        ytar_mm = y_start + move_percent * (y_target - y_start);


        if (inverse_kinematics(q0, q1, xtar_mm, ytar_mm))
        {
            m1.set_rad_target(q0+q1);
            m0.set_rad_target(q0); 
        } else break;

        bool stepped= false;
        stepped = m0.step_if_needed() ? true : stepped;
        stepped = m1.step_if_needed() ? true : stepped;

        if(motion_state == 1 && !stepped) break;
    }
}

void Bot::forward_kinematics(double &x, double &y, double q0, double q1){
    // q0 = q0 == NONE ? m0.get_rads():Bot::q0;
    // q1 = q1 == NONE ? m1.get_rads():Bot::q1;

    x = __L1_mm * cos(q0) + __L2_mm * cos(q0 + q1);
    y = __L1_mm * sin(q0) + __L2_mm * sin(q0 + q1);
}

bool Bot::inverse_kinematics(double &q0, double &q1, double x, double y){
    /*
     * Updates joint angles (q0, q1) to reach desired
     * (x, y) position in cartesian space (if possible)
    */

    x = x == NAN ? Bot::x : x;
    y = y == NAN ? Bot::y : y;
    
    double r = sqrt(x*x + y*y);

    if (r > __L12_mm) {
        // Serial.println("invalid postition... returning previous angles");
        // Serial.println(r);
        // Serial.println(" ");
        return false;
    }

    else{
        double phi0 = atan2(y, x);
        double phi1 = acos((r*r + __L1_mm*__L1_mm - __L2_mm*__L2_mm) / (2*r*__L1_mm));
        double phi2 = acos((__L1_mm*__L1_mm + __L2_mm*__L2_mm - r*r) / (2*__L1_mm*__L2_mm));

        q0 = phi0 - phi1;
        q1 = PI - phi2; // +q0

        return true;
    }
} 


void Bot::joystick_mode(bool joy_true)
{
    __joymode = joy_true;
    set_move_mode(!joy_true); // sets abs/rel mode
}

void Bot::joystick_run(){

    int x_val = analogRead(joy_x);
    int y_val = analogRead(joy_y);
    auto dx = (double )map(x_val, 1, 1022, -4, 4);
    auto dy = (double )map(y_val, 1, 1022, -4, 4);

    if (dx <= 1.0 && dx >= -1.0) dx=0;
    if (dy <= 1.0 && dy >= -1.0) dy=0; 

    if (digitalRead(joy_btn) == LOW) {
        set_move_mode(true);
        go_home();
        set_move_mode(false);
    }
    else move_motor_linear_no_accel(dx, dy, 90.0);
}
