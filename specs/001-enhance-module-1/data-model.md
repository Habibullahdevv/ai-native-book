# Data Model: ROS 2 Middleware Entities

## Overview
This document defines the key data entities and their relationships for Module 1: The Robotic Nervous System (ROS 2), based on the feature specification `001-enhance-module-1: ROS 2 Middleware Enhancements`.

## Entities

### 1. ROS 2 Node
- **Description**: An independent executable process in ROS 2 that performs computation (e.g., sensor driver, controller, algorithm).
- **Fields**:
    - `name`: String, unique identifier for the node.
    - `lifecycle_state`: Enum (Unconfigured, Inactive, Active, Finalized), representing the node's state in the managed lifecycle.
    - `executor_type`: Enum (SingleThreadedExecutor, MultiThreadedExecutor), indicating how callbacks are processed.
- **Relationships**: Interacts with other Nodes via Topics, Services, and Actions.

### 2. ROS 2 Topic
- **Description**: A named bus over which nodes exchange messages using a publish-subscribe communication model.
- **Fields**:
    - `name`: String, unique identifier for the topic.
    - `message_type`: String, the type of data structure being communicated (e.g., `std_msgs/msg/String`, `sensor_msgs/msg/Image`).
    - `qos_profile`: Object, Quality of Service settings (e.g., durability, reliability, history, deadline, lifespan).
- **Relationships**: Published to by a Node, subscribed to by a Node.

### 3. ROS 2 Service
- **Description**: A request-response communication mechanism for immediate, blocking operations between nodes.
- **Fields**:
    - `name`: String, unique identifier for the service.
    - `request_type`: String, the message type for the service request.
    - `response_type`: String, the message type for the service response.
- **Relationships**: Provided by a Node (Service Server), consumed by a Node (Service Client).

### 4. ROS 2 Action
- **Description**: A long-running, goal-oriented communication mechanism for tasks that may take significant time to complete, providing feedback and results.
- **Fields**:
    - `name`: String, unique identifier for the action.
    - `goal_type`: String, the message type for the action goal.
    - `result_type`: String, the message type for the action result.
    - `feedback_type`: String, the message type for periodic feedback during action execution.
- **Relationships**: Provided by a Node (Action Server), consumed by a Node (Action Client).

### 5. URDF Link
- **Description**: A rigid body part of a robot, representing its physical structure.
- **Fields**:
    - `name`: String, unique identifier for the link.
    - `visual`: Object, properties for visual representation (e.g., geometry, material, origin).
    - `collision`: Object, properties for collision detection (e.g., geometry, origin).
    - `inertial`: Object, properties for physics simulation (e.g., mass, inertia matrix, origin).
- **Relationships**: Connected by Joints.

### 6. URDF Joint
- **Description**: Connects two links, defining their relative motion and degrees of freedom.
- **Fields**:
    - `name`: String, unique identifier for the joint.
    - `type`: Enum (revolute, continuous, prismatic, fixed, floating, planar), defining the joint's motion capabilities.
    - `parent_link`: String, name of the parent link.
    - `child_link`: String, name of the child link.
    - `axis`: Object (x, y, z components), direction of rotation/translation.
    - `limit`: Object, upper/lower limits, velocity, effort for motion.
- **Relationships**: Connects a `parent_link` to a `child_link`.

## Validation Rules
- Node names, Topic names, Service names, and Action names must be unique within a ROS graph.
- Message types for Topics, Services, and Actions must be valid ROS 2 message definitions.
- URDF links and joints must adhere to the URDF XML schema for valid robot models.

## State Transitions (for ROS 2 Nodes with managed lifecycle)
- **Unconfigured -> Inactive**: `configure` transition (node is initialized, but not running)
- **Inactive -> Active**: `activate` transition (node starts processing data)
- **Active -> Inactive**: `deactivate` transition (node stops processing data, resources can be released)
- **Inactive -> Unconfigured**: `cleanup` transition (node cleans up resources)
- **Any State -> Finalized**: `shutdown` transition (node is terminated)