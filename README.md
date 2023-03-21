# documentation-automate-AST
[Obsidian graph](https://github.com/kroq86/documentation-automate-AST/blob/main/image.png)

The code include cProfile and generate Markdown files that can be viewed as a graph in Obsidian's graph view.

The code reads through all .py files in a given directory and its subdirectories, parses the AST (Abstract Syntax Tree) of each file to identify classes, methods, and attributes, builds a directed graph with classes as nodes and methods/attributes as edges, and generates Markdown files for each class with links to its methods and attributes. It also generates an index file and a main file that links to the index and all classes. The generated Markdown files can be viewed as a graph in Obsidian's graph view.

To improve the performance of the code, cProfile has been added to profile the execution time of the functions. This allows developers to identify bottlenecks and optimize the code accordingly.

The class ClassFinder is responsible for identifying all classes in the code, while GraphBuilder is responsible for building the directed graph with classes as nodes and methods/attributes as edges. MarkdownGenerator is responsible for generating Markdown files for each class with links to its methods and attributes, as well as the index and main files.
This call stack graph can be a useful tool for understanding how the code works and how it generates documentation for Python code. It can also help developers identify any potential issues or errors in the code.

The new feature in GitHub, Git-lab, and Jet-brains IDE allows developers to easily generate documentation for their Python code using the code mentioned above. This feature provides a simple and automated way to document Python code, which can save developers time and reduce errors.

In conclusion, the call stack graph for the Python code that generates documentation for Python code is a useful tool for understanding how the code works and how it generates documentation. The new feature in GitHub, Git-lab, and Jet-brains IDE allows developers to easily generate documentation for their Python code, which can save time and reduce errors.
