# turtlesim-catch-them-all

A ROS2 multi-node robotics application built with `rclpy`, custom message/service interfaces, parameterized launch files, and a closed-loop proportional controller. Turtles spawn at random positions in `turtlesim`; a controller node continuously computes distance/heading to the nearest (or oldest) turtle and drives toward it, calling a custom service to "catch" (despawn) it on arrival.

## Architecture

Three ROS2 packages composed with a single launch file:

- **`my_robot_interfaces`** — custom interface definitions used across nodes:
  - `Turtle.msg` (name, x, y, theta) / `TurtleArray.msg` (list of alive turtles)
  - `CatchTurtle.srv` (request: turtle name → response: success bool)
- **`turtlesim_catch_them_all`** — the two application nodes:
  - `turtle_spawner` — spawns turtles at random poses on a timer, publishes the list of currently-alive turtles on `/alive_turtles`, and exposes the `catch_turtle` service (kills a turtle in `turtlesim` and removes it from the tracked list).
  - `turtle_controller` — subscribes to `/turtle1/pose` and `/alive_turtles`, selects a target turtle (closest-first or spawn-order, via a runtime parameter), and runs a proportional controller publishing `Twist` commands to `/turtle1/cmd_vel`. On reaching the target it calls the `catch_turtle` service asynchronously.
- **`my_robot_bringup`** — a single XML launch file that starts `turtlesim`, the controller, and the spawner together, with parameters loaded from a shared YAML config.

## Key ROS2 concepts demonstrated

- Publishers/subscribers (`Pose`, `Twist`, custom `TurtleArray`)
- Custom `.msg` / `.srv` interface definitions (`ament`/`rosidl`)
- Services with async clients (non-blocking `call_async` + callback pattern)
- Declared/loaded runtime parameters (YAML-driven config, no hardcoded values)
- Timer-driven control loop with proportional (P) control for linear + angular velocity, including angle-wrapping to keep heading error in `[-π, π]`
- Composable launch files (`my_robot_bringup`) that bring multiple nodes up together with shared parameter files

## Running it

```bash
# from a ROS2 workspace root (e.g. ~/ros2_ws)
cp -r src/* ~/ros2_ws/src/
cd ~/ros2_ws
colcon build
source install/setup.bash
ros2 launch my_robot_bringup turtlesim_catch_them_all.launch.xml
```

This starts `turtlesim`, then the spawner (dropping a new turtle roughly every 1.5s) and the controller (which will immediately start hunting turtles down).

## Notes

Originally built while working through a ROS2 fundamentals course, then cleaned up and pushed here as a standalone project. Built and tested against ROS2 (rclpy, `ament_python`/`ament_cmake` build types).
