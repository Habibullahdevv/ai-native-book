# Implementation Plan: AI Native Book Docusaurus Cleanup and Fix

**Branch**: `main` | **Date**: 2025-12-15 | **Spec**: ./spec.md
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Clean and fix the AI Native Book Docusaurus repository. This involves organizing book content into correct source folders, ensuring proper sidebar and footer configuration, and creating a functional homepage. Changes will be committed, safely merged, pushed to GitHub, and deployed via GitHub Pages, strictly avoiding modifications to auto-generated or ignored directories.

## Technical Context


**Language/Version**: JavaScript/TypeScript, Node.js  
**Primary Dependencies**: Docusaurus, React  
**Storage**: Filesystem  
**Testing**: Docusaurus build process for validation  
**Target Platform**: Web (GitHub Pages)
**Project Type**: Web application (Docusaurus site)  
**Performance Goals**: Fast loading Docusaurus site  
**Constraints**: Do not modify auto-generated or ignored folders (build/, node_modules/).  
**Scale/Scope**: Single Docusaurus site for the AI Native Book.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*


No Constitution Check violations. The plan aligns with all core principles and contributes to the book's structure and success criteria. Constraints regarding ignored folders are respected.


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
.
├── blog/                   # Blog posts
├── docs/                   # Markdown documents
├── src/
│   ├── components/         # React components
│   └── pages/              # React pages (e.g., homepage)
├── static/                 # Static assets
├── docusaurus.config.js    # Docusaurus configuration
├── sidebars.js             # Sidebar configuration
├── package.json            # Project dependencies and scripts
└── yarn.lock               # Dependency lock file
```

**Structure Decision**: The project uses a standard Docusaurus site structure for documentation and static content. The cleanup will ensure content is correctly placed within `docs/` and `src/pages/`, and configurations in `docusaurus.config.js` and `sidebars.js` are accurate.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
