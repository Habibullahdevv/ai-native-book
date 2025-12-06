<!--
Sync Impact Report:
Version change: 0.0.0 (initial) -> 1.0.0 (initial)
Modified principles: None (initial creation/population)
Added sections: Key Standards, Book Structure (Mandatory Modules), Project Constraints, Success Criteria
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ✅ updated
- .specify/templates/spec-template.md: ✅ updated
- .specify/templates/tasks-template.md: ✅ updated
- .specify/templates/commands/*.md: ✅ updated (no files found, so no updates needed)
Follow-up TODOs: RATIFICATION_DATE
-->
# Book — “Physical AI & Humanoid Robotics” Constitution

## Core Principles

### I. Scientifically Accurate Explanations
Deliver scientifically accurate explanations grounded in robotics, AI, and control theory.

### II. Clarity for Engineering-Oriented Audience
Maintain clarity for an engineering-oriented audience (AI, robotics, CS students).

### III. Reproducibility
Ensure reproducibility of all technical instructions, simulations, and code examples.

### IV. Responsible and Ethical AI–Robot Integration
Promote responsible and ethical AI–robot integration.

## Key Standards

- All claims MUST be supported by primary robotics/AI sources (IEEE, ACM, NVIDIA, ROS docs).
- Terminology and definitions MUST follow robotics standards (ROS 2, Isaac, Gazebo, URDF).
- Minimum 50% citations MUST be peer-reviewed or official technical documentation.
- All diagrams, simulation setups, and code examples MUST be tested and verified.
- Citation style: IEEE format.

## Book Structure (Mandatory Modules)

### Module 1: The Robotic Nervous System (ROS 2)
- ROS 2 middleware fundamentals.
- Nodes, Topics, Services, and Actions.
- rclpy for connecting Python agents to robot controllers.
- URDF modeling for humanoid robots.

### Module 2: The Digital Twin (Gazebo & Unity)
- Simulation physics: gravity, inertial models, collisions.
- High-fidelity rendering and HRI scenes in Unity.
- Sensor simulation: LiDAR, Depth cameras, IMUs.

### Module 3: The AI-Robot Brain (NVIDIA Isaac™)
- Isaac Sim for photorealistic simulation and synthetic data.
- Isaac ROS for GPU-accelerated SLAM and perception.
- Nav2 for bipedal humanoid navigation and locomotion.

### Module 4: Vision-Language-Action (VLA)
- Whisper for voice-to-action command processing.
- LLM-based cognitive planning translating instructions to ROS 2 action sequences.
- Capstone Project: A humanoid that listens, navigates, perceives, and manipulates objects.

## Project Constraints

- Length: 12,000–15,000 words.
- Minimum 20 credible technical sources.
- Include at least 8 diagrams of robotics systems, sensors, and simulations.
- All example code MUST run on ROS 2 Humble/Foxy, Gazebo Fortress, Unity, and Isaac Sim.
- Output: Google Docs draft and final PDF.

## Success Criteria

- All modules deliver technically correct robotics pipelines.
- Zero plagiarism.
- All simulations, diagrams, and and code blocks verified.
- Book forms a complete learning path from ROS → Simulation → AI → VLA control.

## Governance

Amendments to this constitution require documentation, approval, and a migration plan.
All PRs/reviews MUST verify compliance.
Complexity MUST be justified.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2025-12-05
