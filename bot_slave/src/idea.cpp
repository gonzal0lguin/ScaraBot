// #include <Arduino.h>


// void move_motor_linear(float x_target_mm, float y_target_mm, float v_max)
// {
//   // Get start position
//   float x_start, y_start;
//   get_pos(x_start, y_start); // get coordinates of current position

//   // Populate with defaults if any are none
//   v_max = v_max == NOVALUE ? def_vel : v_max / 60;
//   float accel = def_accel;

//   // If relative mode, do that
//   if (absmode == false)
//   {
//     x_target_mm = x_target_mm == NOVALUE ? x_start : x_target_mm + x_start;
//     y_target_mm = y_target_mm == NOVALUE ? y_start : y_target_mm + y_start;
//   }
//   else
//   {
//     x_target_mm = x_target_mm == NOVALUE ? x_start : x_target_mm;
//     y_target_mm = y_target_mm == NOVALUE ? y_start : y_target_mm;
//   }

//   // Calculate some basic move statistics
//   float move_dist_mm = sqrt(pow(x_target_mm - x_start, 2) + pow(y_target_mm - y_start, 2)); // distancia a movers
//   float accel_dist_mm = pow(v_max, 2) / (2 * accel);

//   if(move_dist_mm < (2 * accel_dist_mm))
//   {
//     // si la distancia a recorrer es menor a la con aceleracion, setear aceleracion tal que sea
//     // peak en la mitad de la distancia
//     accel_dist_mm = move_dist_mm / 2;
//   }

//   float inflect_t0_s = sqrt((2 * accel_dist_mm) / accel);
//   float inflect_t1_s = inflect_t0_s + (move_dist_mm - (2 * accel_dist_mm)) / v_max;
//   float move_time_s = inflect_t1_s + inflect_t0_s; // t_acelerado + t_cte


//   // Calculate when to take steps on the fly like a -boss- skrub
//   uint8_t motion_state = 0; // 0: accelerating, 1: plateau, 2: decelerating, 3: finalize
//   uint32_t t_start = micros();
//   uint32_t t_step;

//   float linear_dist_mm, t_elapsed_s, move_percent, xtar_mm, ytar_mm;

//   while(true)
//   {
//     t_step = micros(); // tiempo de inicio
//     t_elapsed_s = t_step - t_start; // tiempo de movimiento
//     t_elapsed_s /= 1000000; // t movimiento en segundos

//     switch(motion_state)
//     {
//       case 0: {
//         linear_dist_mm = (accel * pow(t_elapsed_s, 2)) / 2; // aumentar la distancia aceleradamente
//         if(t_elapsed_s > inflect_t0_s) motion_state++;
//         break;
//       }
//       case 1: {
//         linear_dist_mm = accel_dist_mm + v_max * (t_elapsed_s - inflect_t0_s); // aumentar linealmente  
//         if(t_elapsed_s > inflect_t1_s) motion_state++;
//         break;
//       }
//       case 2: {
//         linear_dist_mm = move_dist_mm - ((accel * pow(move_time_s - t_elapsed_s, 2)) / 2);
//         if(t_elapsed_s > move_time_s) motion_state++;
//         break;
//       }
//       case 3: {
//         linear_dist_mm = move_dist_mm;
//         break;
//       }
//     }
//     move_percent = linear_dist_mm / move_dist_mm;
//     xtar_mm = x_start + move_percent * (x_target_mm - x_start);
//     ytar_mm = y_start + move_percent * (y_target_mm - y_start);

//     float t0, t1;
//     ik_solve(xtar_mm, ytar_mm, t0, t1);
//     s0.set_rad_target(t0);
//     s1.set_rad_target(t1);

//     bool stepped = false;
//     stepped = s0.step_if_needed() ? true : stepped;
//     stepped = s1.step_if_needed() ? true : stepped;

// //    debug_print();

//     if(motion_state == 3 && !stepped) break;
//   }
// }