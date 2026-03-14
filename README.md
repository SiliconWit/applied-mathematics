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

A foundation course covering mathematical methods for engineering problem-solving and scientific analysis. Topics include linear algebra, computational methods, and the art of building useful mathematical models from real-world systems.

## Lessons

| # | Title |
|---|-------|
| 1 | Linear Algebra in Applied Mathematics |
| 2 | The Art of Simplification: Spherical Cows and Model Building |

## File Structure

```
applied-mathematics/
├── index.mdx
├── linear-algebra.mdx
├── spherical-cows-engineering-model-building.mdx
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
- `<BionicText>` may be used in later content sections but not in lesson intro paragraphs
- Code blocks should include a title attribute:
  ````mdx
  ```python title="matrix_operations.py"
  import numpy as np
  A = np.array([[1, 2], [3, 4]])
  ```
  ````
- Use Starlight components (`<Tabs>`, `<TabItem>`, `<Steps>`, `<Card>`) where appropriate
- Keep paragraphs concise and focused on practical application
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
