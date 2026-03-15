---
title: "Applied Mathematics - Collaboration Guide"
description: "Contributing guide for Applied Mathematics course content"
tableOfContents: true
sidebar:
  order: 999
---

# Applied Mathematics

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Contributors Welcome](https://img.shields.io/badge/contributors-welcome-orange)

**Read this course at:** [https://siliconwit.com/education/applied-mathematics/](https://siliconwit.com/education/applied-mathematics/)

Nine lessons covering the mathematics engineers use most often: modeling, calculus, linear algebra, complex numbers, probability, differential equations, Fourier analysis, numerical methods, and feedback control. Every topic starts with a real problem, introduces the math as the tool to solve it, and includes Python code where it helps.

## Lessons

| # | Title |
|---|-------|
| 1 | Spherical Cows and the Art of Model Building |
| 2 | Calculus for Engineers |
| 3 | Linear Algebra: Vectors, Matrices, and Transforms |
| 4 | Complex Numbers and Phasors |
| 5 | Probability, Statistics, and Noise |
| 6 | Differential Equations and Real Systems |
| 7 | Fourier Analysis and the Frequency Domain |
| 8 | Numerical Methods: Math in Code |
| 9 | Feedback and Control Systems |

## File Structure

```
applied-mathematics/
├── index.mdx
├── spherical-cows-model-building.mdx
├── calculus-for-engineers.mdx
├── linear-algebra-vectors-matrices.mdx
├── complex-numbers-and-phasors.mdx
├── probability-statistics-noise.mdx
├── differential-equations-real-systems.mdx
├── fourier-analysis-frequency-domain.mdx
├── numerical-methods-computation.mdx
├── feedback-control-systems.mdx
└── README.md
```

## How to Contribute

1. Fork the repository: [SiliconWit/applied-mathematics](https://github.com/SiliconWit/applied-mathematics)
2. Create a feature branch: `git checkout -b feature/your-topic`
3. Make your changes and commit with a clear message
4. Push to your fork and open a Pull Request against `main`
5. Describe what you changed and why in the PR description

## Content Standards

- All lesson files use `.mdx` format
- Do not use `<BionicText>` in this course
- Code blocks should include a title attribute:
  ````mdx
  ```python title="matrix_operations.py"
  import numpy as np
  A = np.array([[1, 2], [3, 4]])
  ```
  ````
- Use ASCII diagrams in `text` code blocks where they help visualize circuits, signals, or systems
- Use Starlight components (`<Tabs>`, `<TabItem>`, `<Steps>`, `<Card>`) where appropriate
- Every formula should be preceded by intuition (explain what it means before showing the equation)
- Include working Python examples that readers can run directly
- Mathematical notation uses LaTeX in MDX

## Local Development

Clone the main site repository and initialize submodules:

```bash
git clone --recurse-submodules <main-repo-url>
cd siliconwit-com
npm install
npm run dev
```

To test a production build:

```bash
npm run build
```

## License

This course content is released under the [MIT License](LICENSE).
