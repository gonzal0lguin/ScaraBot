#ifndef BOT_SLAVE_STEPPERLIB_H
#define BOT_SLAVE_STEPPERLIB_H

#include <Arduino.h>


class Stepper
{
  public:
    void init(int s_pin, int d_pin, int e_pin, bool reverse);
    void enable();
    void disable();
    void set_dir(bool dir);
    bool step_if_needed();
    void take_step();
    void overwrite_pos(int32_t newpos);
    void update_config(int32_t steps_per_rev_new);
    void set_rad_target(double target);
    void set_zero_rads(double rads);
    int32_t get_steps();
    float get_rads();
    void moveTo(float target);
    void move_motor(float target, float v_max=100);

  private:
    bool current_dir = false;
    int step_pin;
    int dir_pin;
    int en_pin;
    int reverse;
    double target_rads = 0;
    int32_t step_count = 0;
    float steps_per_rev = 800;
    float accel = 40;
    float vel = 5;
};



#endif