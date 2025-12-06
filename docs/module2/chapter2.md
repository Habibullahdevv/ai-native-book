# Chapter 2: Zero Moment Point (ZMP) Control and Balance

## 2.1 Understanding the Zero Moment Point (ZMP)

The Zero Moment Point (ZMP) is a fundamental concept in bipedal locomotion, crucial for understanding and controlling the balance of humanoid robots. The ZMP is defined as the point on the ground where the net moment of all active forces (gravity, inertia, and ground reaction forces) is zero. When the ZMP remains within the support polygon (the convex hull of the points of contact between the robot's feet and the ground), the robot is in static equilibrium and will not tip over.

### 2.1.1 ZMP Trajectory

For dynamic walking, the ZMP doesn't stay fixed but rather follows a desired trajectory within the support polygon. This ZMP trajectory directly influences the robot's stability and gait pattern. Planning a smooth and feasible ZMP trajectory is a key aspect of stable walking control.

**Diagram**: Illustration of ZMP and support polygon for a bipedal robot (refer to image `assets/module2/zmp_support_polygon.png`)

## 2.2 ZMP-based Control Strategies

Various control strategies have been developed to keep the ZMP within the stability region or to follow a desired ZMP trajectory. These strategies often involve adjusting the robot's center of mass (CoM) and foot placement.

### 2.2.1 Preview Control

Preview control is a popular method for ZMP-based walking. It uses a model of the robot (often a simplified Linear Inverted Pendulum Model - LIPM) and looks ahead in time to calculate future control inputs (e.g., CoM accelerations) that will ensure the ZMP follows the desired trajectory.

### 2.2.2 Online ZMP Compensation

For real-time applications, online ZMP compensation techniques are used to react to unexpected disturbances or uneven terrain. This involves continuously monitoring the actual ZMP and adjusting joint torques or foot positions to maintain balance.

## 2.3 Linear Inverted Pendulum Model (LIPM)

The Linear Inverted Pendulum Model (LIPM) simplifies the humanoid robot dynamics to a point mass (representing the CoM) moving on a horizontal plane, connected to the ZMP by a massless rigid leg of fixed length. This simplification allows for analytical solutions for ZMP control and gait planning.

**Example: LIPM ZMP Calculation (Simplified)**

For a 2D LIPM, the ZMP can be approximated by:

```python
# Simplified 2D LIPM ZMP calculation

g = 9.81  # gravity
zc = 0.8  # constant CoM height

def calculate_zmp_x(com_x, com_x_dot, com_x_ddot):
    return com_x - (zc / g) * com_x_ddot

# Assuming CoM position and derivatives
com_x = 0.0
com_x_dot = 0.1
com_x_ddot = 0.05

zmp_x = calculate_zmp_x(com_x, com_x_dot, com_x_ddot)
print("Calculated ZMP_x:", zmp_x)
```

## 2.4 Center of Mass (CoM) Trajectory Generation

Generating appropriate CoM trajectories is crucial for achieving stable ZMP tracking. These trajectories are often optimized to minimize energy consumption or maximize walking speed while satisfying ZMP constraints.

## 2.5 Conclusion

ZMP control is a cornerstone of stable humanoid locomotion. By understanding the ZMP, implementing effective control strategies like preview control, and leveraging simplified models like the LIPM, engineers can design robots that walk dynamically and maintain balance in various conditions. The next chapter will explore other simplified models for locomotion analysis.
