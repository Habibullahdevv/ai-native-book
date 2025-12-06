## Data Model: Module 2 (Digital Twin)

### Entities

#### Module
- **Description**: Represents a distinct section of the book, specifically "Digital Twin".
- **Attributes**:
    - `Name` (String): The title of the module (e.g., "Digital Twin").
    - `Status` (Enum: Draft, Review, Final): The current editorial status of the module.
    - `Outline` (Hierarchical Structure): A structured representation of the module's main topics and sub-topics.
    - `Chapters` (List of Chapter IDs): References to the chapters contained within this module.

#### Chapter
- **Description**: A major subdivision within a Module.
- **Attributes**:
    - `Title` (String): The title of the chapter.
    - `Order` (Integer): The sequential position of the chapter within its module.
    - `Content Sections` (List of Content Section IDs): References to the individual content sections within this chapter.

#### Content Section
- **Description**: A specific part of a chapter containing draft text, figures, and code.
- **Attributes**:
    - `Title` (String): The title of the content section.
    - `Draft Text` (Markdown String): The narrative, code examples, and explanations for the section.
    - `Status` (Enum: Pending, In Progress, Completed): The current development status of the content section.