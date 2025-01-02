# Contributing to Emergent

Thank you for considering contributing to the **Emergent** project! We value your input and collaboration to make this package better for everyone. Below are the guidelines to help you get started and ensure smooth contributions.

---

## **Table of Contents**
1. [Getting Started](#getting-started)
2. [Code Contributions](#code-contributions)
3. [Documentation](#documentation)

---

## **Getting Started**

1. **Fork the Repository**: Start by forking the repository to your GitHub account [here](https://github.com/delphictech/emergent/fork).
2. **Clone the Repository**: Clone your forked repository to your local machine:
   ```bash
   git clone https://github.com/<your-username>/emergent.git
   ```
3. **Install Dependencies**: Install the required dependencies in a virtual environment:
   ```bash
   pip install -r requirements.txt
   ```
---

## **Code Contributions**

1. Create a new branch for your work:
   ```bash
   git checkout -b <your-github-username>/<your-feature-name>
   ```
2. Write clean, modular code. Use meaningful variable and function names.
    It may be useful to review [PEP 8](https://pep8.org/) guidelines for writing Python code.
3. Commit your changes. Write clear, concise commit messages, such as:
     ```bash
     git commit -m "Add feature: Implemented XYZ"
     ```
2. **Push Your Branch**:
   ```bash
   git push origin <your-github-username>/<your-feature-name>
   ```
3. **Open a Pull Request**:
   - Go to the original repository on GitHub.
   - Open a pull request (PR) from your branch [here](https://github.com/delphictech/emergent/compare). If you forked the repo, you will need to select the **compare across forks** option. 
   - Provide a detailed description of the changes and their purpose. We may provide feedback or request changes before merging.
---

## **Documentation**
Documentation is essential for both developers working on the `emergent` codebase and users of the package. 

Internal documentation should be located in close proximity to the code in docstrings and module README files, while external user-facing documentation should be located in the `docs` directory.

### **Internal Documentation**
1. **Docstrings**: Include detailed docstrings for all public classes, methods, and functions:
   ```python
   def example_function(param1, param2):
       """
       This function demonstrates an example.

       Args:
           param1 (int): Description of param1.
           param2 (str): Description of param2.

       Returns:
           bool: True if successful, False otherwise.

       Notes:
           Additional internal details for developers.
       """
       pass
   ```
2. **README Files in Subdirectories**: When needed, include a `README.md` file in directories for more detailed documentation about the code within.

### **External Documentation**
1. **Location**: All user-facing documentation resides in the `docs/` directory.
2. **Format**: Use Markdown (`.md`) for all documents unless otherwise specified.
3. **Organization**: Ensure documentation is placed in the appropriate section, e.g., installation instructions in `installation.md` and usage examples in `usage.md`.
4. **Content Standards**:
   - Use simple, jargon-free language.
   - Include code examples whenever possible.
   - Provide clear explanations of all features and APIs.

### **Editing Documentation**
1. Update the appropriate files (either alongside code in `src/` or in the `docs/` directory).
2. Use consistent formatting and adhere to existing styles.
3. If you add a new feature, include it in both internal and external documentation as appropriate.

---

Thank you for contributing! Your efforts make **Emergent** a better tool for everyone. 🚀

