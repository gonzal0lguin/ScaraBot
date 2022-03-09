#include "StepperLib.h"

void Stepper::init(int s_pin, int d_pin, int e_pin, bool reverse) {
  step_pin = s_pin;
  dir_pin = d_pin;
  en_pin = e_pin;
  pinMode(step_pin, OUTPUT);
  pinMode(dir_pin, OUTPUT);
  pinMode(en_pin, OUTPUT);
  digitalWrite(en_pin, HIGH);
  digitalWrite(step_pin, LOW);
  digitalWrite(dir_pin, LOW);
  step_count = 0;
  if(reverse){
    reverse = -1;
  }
  else{
    reverse = 1;
  }
}

void Stepper::enable() {
  digitalWrite(en_pin, LOW);
}

void Stepper::disable() {
  digitalWrite(en_pin, HIGH);
}

void Stepper::set_dir(bool dir) {
  if(dir && !current_dir)
  {
    digitalWrite(dir_pin, HIGH);
    current_dir = true;
  }
  else if(!dir && current_dir)
  {
    digitalWrite(dir_pin, LOW);
    current_dir = false;
  }
}

void Stepper::overwrite_pos(int32_t newpos) {
  // to set position in rads -> rad_pos / (2 * PI) * steps_per_rev
  step_count = newpos;
}

void Stepper::update_config(int32_t steps_per_rev_new) {
  steps_per_rev = steps_per_rev_new;
}

void Stepper::take_step() {
  digitalWrite(step_pin, HIGH);
  delayMicroseconds(1);
  digitalWrite(step_pin, LOW);
  if(current_dir) step_count++;
  else step_count--;
}

float Stepper::get_rads() {
  return 2 * PI * step_count / steps_per_rev;
}

void Stepper::set_zero_rads(double rads) {
  step_count = steps_per_rev * rads / (2 * PI);
}

void Stepper::set_rad_target(double target) {
  target_rads = target;
}

bool Stepper::step_if_needed() {
  int32_t step_target = (steps_per_rev * target_rads);
  step_target /= 2 * PI;

  if(step_target == (int32_t)step_count) return false;

  if(step_target > (int32_t)step_count)
  {
    set_dir(true);
  }
  else
  {
    set_dir(false);
  }

  take_step();
  return true;
}

/*
      --------
    /|        |\
---/ |        | \----
  0  ta      tc

*/

// explain implementation and its limits (like it being blocking code)

void Stepper::move_motor(float target, float v_max) {
  
  // Get start position
  float ang_start = get_rads();
  float angular_dist = abs(ang_start - target); // total distance to travel
  if (angular_dist == 0) return;
  // Populate with defaults if any are none
  v_max /= 60;

  float accel_dist = pow(v_max, 2) / (2 * accel); // accelerated distance

  if(angular_dist < (2 * accel_dist)){
    accel_dist = angular_dist / 2;
  }

  float inflect_t0_s = sqrt((2 * accel_dist) / accel);
  float inflect_t1_s = inflect_t0_s + (angular_dist - (2 * accel_dist)) / v_max;
  float move_time_s = inflect_t1_s + inflect_t0_s;


  // Calculate when to take steps on the fly 
  uint8_t motion_state = 0; // 0: accelerating, 1: plateau, 2: decelerating, 3: finalize
  uint32_t t_start = micros();
  uint32_t t_step;

  float linear_dist, t_elapsed_s, move_percent, rad_tar;
  while(true)
  {
    t_step = micros();
    t_elapsed_s = t_step - t_start;
    t_elapsed_s /= 1000000;

    switch(motion_state)
    {
      case 0: {
        linear_dist = (accel * pow(t_elapsed_s, 2)) / 2;
        if(t_elapsed_s > inflect_t0_s) motion_state++;
        break;
      } 
      case 1: {
        linear_dist = accel_dist + v_max * (t_elapsed_s - inflect_t0_s);
        if(t_elapsed_s > inflect_t1_s) motion_state++;
        break;
      }
      case 2: {
        linear_dist = angular_dist - ((accel * pow(move_time_s - t_elapsed_s, 2)) / 2);
        if(t_elapsed_s > move_time_s) motion_state++;
        break;
      }
      case 3: {
        linear_dist = angular_dist;
        break;
      }
    }

    move_percent = linear_dist / angular_dist;
    rad_tar = ang_start + move_percent * (target - ang_start);

    set_rad_target(rad_tar);

    bool stepped = false;
    stepped = step_if_needed() ? true : stepped;
    if(motion_state == 3 && !stepped) break;
  }
}
