#include <micro_ros_arduino.h>

#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

#include <geometry_msgs/msg/twist.h>

rcl_subscription_t subscriber;
geometry_msgs__msg__Twist msg;
rclc_executor_t executor;
rcl_allocator_t allocator;
rclc_support_t support;
rcl_node_t node;

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}

void wheelAct(int leftFront, int leftBack, int rightFront, int rightBack)
{
 digitalWrite(14, leftFront);
 digitalWrite(2, leftBack);
 digitalWrite(13, rightFront);
 digitalWrite(15, rightBack);
}

void subscription_callback(const void *msgin)
{
  const geometry_msgs__msg__Twist * msg = (const geometry_msgs__msg__Twist *)msgin;
  if (msg->linear.x == 0.5) wheelAct(HIGH, LOW, HIGH, LOW);
  else if (msg->linear.x == -0.5) wheelAct(LOW, HIGH, LOW, HIGH);
  else wheelAct(LOW, LOW, LOW, LOW);
}

void error_loop()
{
  while(1)
  {
    // Serial.print("error loop");
    delay(100);
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();
  
  pinMode(14, OUTPUT);  // Left Front
  pinMode(2, OUTPUT);   // Left Back
  pinMode(13, OUTPUT);  // Right Front
  pinMode(15, OUTPUT);

  //set_microros_transports();
  set_microros_wifi_transports("****", "****", "****", ****);
  
  delay(3000);

  allocator = rcl_get_default_allocator();

   //create init_options
  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

  // create node
  RCCHECK(rclc_node_init_default(&node, "micro_ros_arduino_node", "", &support));

  // create subscriber
  RCCHECK(rclc_subscription_init_default(
    &subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist), "/cmd_vel"));

  // create executor
  RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
  RCCHECK(rclc_executor_add_subscription(&executor, &subscriber, &msg, &subscription_callback, ON_NEW_DATA));

  wheelAct(LOW, LOW, LOW, LOW);
}

void loop()
{
  delay(100);
  RCCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));
}
