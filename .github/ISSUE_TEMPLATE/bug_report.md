---
name: "🐛 Bug Report"
description: "Report a bug or unexpected behavior"
title: "[Bug]: "
labels: ["bug"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report! Please provide as much detail as possible to help us understand and reproduce the issue.
  - type: textarea
    id: description
    attributes:
      label: "Description"
      description: "A clear and concise description of what the bug is."
      placeholder: "Describe the bug..."
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: "Steps to Reproduce"
      description: "Steps to reproduce the behavior"
      placeholder: |
        1. Go to "..."
        2. Click on "..."
        3. Scroll down to "..."
        4. See error
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: "Expected Behavior"
      description: "A clear and concise description of what you expected to happen."
      placeholder: "Describe what should happen..."
    validations:
      required: true
  - type: textarea
    id: actual
    attributes:
      label: "Actual Behavior"
      description: "A clear and concise description of what actually happened."
      placeholder: "Describe what actually happened..."
    validations:
      required: true
  - type: textarea
    id: screenshots
    attributes:
      label: "Screenshots"
      description: "If applicable, add screenshots to help explain your problem."
      placeholder: "Add screenshots..."
  - type: textarea
    id: logs
    attributes:
      label: "Logs"
      description: "If applicable, add logs or error messages."
      placeholder: "Paste logs here..."
  - type: dropdown
    id: os
    attributes:
      label: "Operating System"
      description: "What operating system are you using?"
      options:
        - "Windows"
        - "macOS"
        - "Linux"
        - "Other"
    validations:
      required: true
  - type: input
    id: version
    attributes:
      label: "Paper Formatter Version"
      description: "What version of Paper Formatter are you using?"
      placeholder: "e.g., v2.2.2"
    validations:
      required: true
  - type: textarea
    id: context
    attributes:
      label: "Additional Context"
      description: "Add any other context about the problem here."
      placeholder: "Any additional information..."
