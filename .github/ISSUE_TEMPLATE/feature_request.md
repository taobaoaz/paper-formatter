---
name: "✨ Feature Request"
description: "Suggest an idea for this project"
title: "[Feature]: "
labels: ["enhancement"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting a new feature! Please provide as much detail as possible to help us understand your needs.
  - type: textarea
    id: description
    attributes:
      label: "Description"
      description: "A clear and concise description of the feature you would like."
      placeholder: "Describe the feature..."
    validations:
      required: true
  - type: textarea
    id: problem
    attributes:
      label: "Problem Statement"
      description: "What problem does this feature solve? Why is it needed?"
      placeholder: "Describe the problem this feature would solve..."
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: "Proposed Solution"
      description: "Describe how you envision this feature working."
      placeholder: "Describe your proposed solution..."
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: "Alternatives Considered"
      description: "Describe any alternative solutions or features you have considered."
      placeholder: "Describe alternatives..."
  - type: textarea
    id: examples
    attributes:
      label: "Examples"
      description: "If applicable, provide examples of how this feature would be used."
      placeholder: "Provide usage examples..."
  - type: textarea
    id: screenshots
    attributes:
      label: "Screenshots/Mockups"
      description: "If applicable, add screenshots or mockups to help visualize the feature."
      placeholder: "Add screenshots or mockups..."
  - type: checkboxes
    id: contribution
    attributes:
      label: "Willing to Contribute"
      description: "Are you willing to help implement this feature?"
      options:
        - label: "Yes, I can help implement this feature"
        - label: "I can help with testing"
        - label: "I can help with documentation"
        - label: "I can provide feedback"
        - label: "No, I cannot contribute at this time"
  - type: textarea
    id: context
    attributes:
      label: "Additional Context"
      description: "Add any other context about the feature request here."
      placeholder: "Any additional information..."
