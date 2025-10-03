# Compiler Design: A Visual Exploration

A **visual compiler simulator** that processes source code through all major compilation phases—**lexical analysis, syntax analysis, semantic analysis, intermediate code generation, optimization, and target code generation**—providing **graphical outputs** and **real-time feedback** for educational understanding, debugging, and experimentation.

---

## 📖 About the Project

Learning compiler design concepts can be challenging due to their abstract nature. This project, **“Compiler Design: A Visual Exploration”**, simplifies the learning process by visually representing each stage of the compilation pipeline.

The simulator accepts source code input and guides the user through the **entire compilation workflow**, highlighting each transformation step—right from **token generation** to **optimized target code**.

By integrating **graphical outputs** (such as parse trees and intermediate code visualizations) with **real-time feedback**, the tool enhances comprehension, aids in debugging, and bridges the gap between theoretical concepts and practical implementation.

---

## ✨ Features

- 📝 **Lexical Analysis** – Tokenization of the input source code  
- 🌳 **Syntax Analysis** – Parse tree construction to represent the syntactic structure  
- 🧠 **Semantic Analysis** – Type checking, scope resolution, and error reporting  
- ⚙️ **Intermediate Code Generation** – Displays intermediate representations like three-address code  
- 🚀 **Code Optimization** – Shows optimized intermediate code for better performance  
- 💻 **Target Code Generation** – Generates simplified target code for execution  
- 🎨 **Graphical Visualization** – Real-time graphical display of parse trees and other compiler outputs  
- 🖥️ **Interactive GUI** – User-friendly interface for step-by-step exploration of compiler phases  
- 📊 **Debugging Assistance** – Highlights compilation errors at each stage for easy troubleshooting  

---

## 🖥️ Software Requirements

- **Operating System:** Windows 10/11, Linux (Ubuntu 20.04+), or macOS 11+  
- **Programming Language:** Python 3.8+  
- **Libraries and Frameworks:**  
  - [`tkinter`](https://docs.python.org/3/library/tkinter.html) – For GUI development  
  - [`ply`](https://www.dabeaz.com/ply/) – Python Lex-Yacc for lexical and syntax analysis  
  - [`graphviz`](https://graphviz.org/) or [`networkx`](https://networkx.org/) – For parse tree visualization  
  - [`matplotlib`](https://matplotlib.org/) – For graphical representation of intermediate code and other metrics  
- **Development Environment:** VS Code / PyCharm / Jupyter Notebook  
- **Version Control:** Git  

---

## 💻 Hardware Requirements

- **Processor:** Intel i3 / AMD Ryzen 3 or higher  
- **RAM:** Minimum 4 GB (8 GB recommended)  
- **Storage:** 500 MB free disk space  
- **Display:** 1366×768 resolution or higher  

---

## 📂 Project Structure

compiler_design_PBL/

│

├── main.py # Source code for compiler phases

│ ├── lexer.py # Lexical analyzer implementation

│ ├── parser.py # Syntax analyzer and parse tree generator

│ ├── semantic.py # Semantic analysis module

│ ├── intermediate.py # Intermediate code generation logic

│ ├── optimizer.py # Code optimization module

│ ├── codegen.py # Target code generator

│ └── gui.py # GUI integration for visual outputs

│

├── parser.out # Output file

├── ast.png # Images, icons, and sample visualization outputs

├── utils.py # Python dependencies

├── README.md # Project documentation

└── LICENSE # License details



---

## ⚙️ Installation and Setup

1. **Clone the repository**
   git clone https://github.com/abhinavsaluja2004/Compiler-Design-A-Visual-Exploration.git
   cd Compiler-Design-A-Visual-Exploration
   
2. **Install dependencies**
   pip install -r requirements.txt

3. **Run the application**
   python gui.py

## 🚀 Usage

1. Launch the application using the above command

2. Enter or upload your source code in the input window

3. Click “Run” or the desired compiler phase button to visualize each stage:

  - View tokens generated during lexical analysis
  
  - Examine the parse tree during syntax analysis

  - Check for semantic errors and corrections

  - Observe intermediate code and optimization steps

   - Generate and preview the final target code

4. Save the generated outputs or visualizations for further study

## 📚 Educational Value

This project serves as an educational tool to:

1. Help students visualize how compilers work internally

2. Aid instructors in demonstrating compilation stages in classrooms

3. Assist developers and researchers in debugging and experimenting with compiler logic

## 🔧 Future Enhancements

1. Support for additional programming languages

2. Integration of advanced optimization techniques

3. Exportable reports and logs for each compiler phase

4. Enhanced error highlighting and suggestion engine for semantic analysis

5. Web-based interface for platform-independent accessibility


## 📜 License

This project is licensed under the GNU GENERAL PUBLIC LICENSE.
.

## ⭐ Acknowledgments

We thank the contributors, open-source libraries, and educational platforms that supported the development of this project.

