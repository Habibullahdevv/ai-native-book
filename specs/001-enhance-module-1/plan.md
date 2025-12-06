# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11, C++ (ROS 2)
**Primary Dependencies**: ROS 2 Humble/Foxy, rclpy, Gazebo Fortress, Unity, NVIDIA Isaac Sim
**Storage**: N/A
**Testing**: pytest (Python), ament_cmake_gtest (C++)
**Target Platform**: Linux
**Project Type**: Single project (code examples for book)
**Performance Goals**: **Performance Goals**: Real-time communication for robotics: sub-millisecond latency for critical tasks, high throughput for data, minimal jitter (microsecond range). rclpy is suitable for many components, but rclcpp may be preferred for the most stringent real-time requirements.
**Constraints**: Reproducibility on ROS 2 Humble/Foxy, Gazebo Fortress, Unity, Isaac Sim. Adherence to ROS 2 standards.
**Scale/Scope**: Module 1 explanations and practical examples for ROS 2 middleware fundamentals, primitives, rclpy integration, and URDF modeling.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Refer to the project constitution at `.specify/memory/constitution.md` for:
- Core Principles (e.g., scientific accuracy, clarity, reproducibility, ethical AI integration)
- Key Standards (e.g., citation style, source verification, testing of diagrams/simulations)
- Project Constraints (e.g., length, diagrams, compatible environments)
- Success Criteria (e.g., technical correctness, zero plagiarism, verified simulations)


## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
