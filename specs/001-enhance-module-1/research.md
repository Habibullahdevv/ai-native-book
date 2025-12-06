# Research Findings: ROS 2 Real-time Performance Goals

## Decision:
For Module 1 of the "Physical AI & Humanoid Robotics" book, real-time communication performance goals in ROS 2 will focus on achieving very low and predictable latency, high throughput, and minimal jitter, specifically for middleware fundamentals (nodes, topics, services, actions) and `rclpy` integration.

## Rationale:
Humanoid robotics applications demand precise and timely interactions. ROS 2, built on DDS, provides the necessary architectural foundation for real-time capabilities. While `rclpy` is suitable for many components due to ease of development, `rclcpp` (C++) is generally preferred for the most stringent real-time requirements.

## Alternatives Considered:

*   **Relying solely on `rclpy` for all components:** Rejected for critical control loops where Python's overhead might introduce unacceptable latency or jitter. `rclcpp` offers more predictable, lower-level control for hard real-time tasks.
*   **Ignoring specific performance metrics:** Rejected because clarity on performance expectations is crucial for an engineering-oriented audience, ensuring reproducibility and practical understanding of ROS 2's capabilities.

## Key Metrics and Goals:

*   **Latency:** Sub-millisecond (< 1 ms) for highly time-sensitive control loops and sensor feedback. Tens of milliseconds for less critical operations.
*   **Throughput:** Maximized to handle large volumes of sensor data and complex command streams, preventing bottlenecks.
*   **Jitter:** Minimal and predictable, ideally in the microsecond range, for deterministic behavior and stable control.

## Sources:
- [researchgate.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGXs8htyTv3VhCOZ1ZzqnzBhz6ep6k6tTKEsUJUm6y8ChOsyyn0Jp-a5GRzpd5yyJvrNS8Qw8aM-wU9lmsQwa658pay3f3BYyHIChnGunIvGUCH59ZnC0DBu8VbPCVwiAjA5GA5QSQXoo_5epZJr9jH9vBoouEzDis-kLaoOhaYsilooREZ1vVqKBq77kQ_jpL4xeZG7-n5wR3aT98fEjhWNfO-xcrFcrkPHlOpgn8YwYJDf5m6oK1y_WOao-OPuYwt3eNMvDDhhan7YAUiu_6dPh4=)
- [researchgate.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHbYgE6Jl0VQZ-3ETGugKA9VEC5gwzzP8WS6sB-ZSV29uA6x0H7uPyjEP7oSuEHgpgT5s1QfantCRx7LeqZFaOWGMs-k-fOqM3trcp0rJ1Joyo7sslyOVD0-Tuwd3hRVJIMO4KBSD4jxhw-z0P1nHJje8wF_2HE2Mcz5gUwJ3Z4D8TTZnNX5CwMX1dGHN-89w==)
- [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHxPdg5mNSxZjByb7fokpFtatROv_2iOij5oDLFHYKcjWk6mRkl_NDzGgzN8xyOtkVtfIJEgz5P_P82EY99hRhtmekmOPwgBnxI2eX50msyKX3GfkLVKADLls-6ysfinyC_oa8SZqzWnTOot-74dauCx8EmlGNicGJWW5GlTuRZRzxzO1KAnBS3zvcBWy2SbW5TT_5p_B0p1M_GxU9v4Q==)
- [patsnap.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHZU3jc-JkvB7MI8YY4qGyC-Orh6K6F4xcdRE1edVNHcxnsQzQeVBet8aLd28EFfR4gh90W166LbusOUptgC3XIy76VqDPxVGyFyf_rWym_3kP2dwtnjJ94DrLaJ-rZpsvrEDOOZLJN6XdmmMqPiGHkW-bwfeXo2zRtuoI9bV10vTDXgDMh_S7jQrhR54EkD4s2ZUL9zVayglJnh2IT-7rQFQ==)
- [openrobotics.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQERJ6Xr8PxTwU5lFF06qjLcQq247KGCHBgpNXqcQbQGisCsOi7heiXC5rcn5Q5TK2GpavnAhRVYNJNxr8WInc0YKx6NnOy_ZypqVRykelIvRWI5_j-LmD8rbIZgkxvjxdpmfwOHQP-x80mDASEBNLAmsgp6GXoDr6gXLVyL_X38IGTNAQ=)