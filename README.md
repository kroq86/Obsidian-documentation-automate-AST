# documentation-automate-AST
Reads through all .py files in a given directory and its subdirectories, parses the AST (Abstract Syntax Tree) of each file to identify classes, methods, and attributes, builds a directed graph with classes as nodes and methods/attributes as edges, and generates Markdown files for each class with links to its methods and attributes.
[Obsidian graph](https://github.com/kroq86/documentation-automate-AST/blob/main/image.png)

Generating documentation for Python code can be a time-consuming and error-prone process. Fortunately, there are tools available that can automate this task, such as the Python code mentioned above that reads through all .py files in a given directory and generates documentation for the code.

The process starts with the code reading through all the .py files in a given directory and its subdirectories. It then parses the AST (Abstract Syntax Tree) of each file to identify classes, methods, and attributes. This information is then used to build a directed graph with classes as nodes and methods/attributes as edges.

Once the graph has been built, the code generates Markdown files for each class with links to its methods and attributes. Additionally, the code generates an index file that lists all classes and a main file that links to the index and all classes.

The code is organized into several functions that handle different tasks. The main function is responsible for calling the other functions in the correct order. The find_classes function is responsible for identifying all classes in the code. The build_graph function is responsible for building the directed graph with classes as nodes and methods/attributes as edges. This function calls the get_class_dependencies, add_method_edges, and add_attribute_edges functions to complete its task.

The generate_markdown_files function is responsible for generating Markdown files for each class with links to its methods and attributes. This function calls the generate_method_markdown and generate_attribute_markdown functions to complete its task.

Finally, the generate_index_file function is responsible for generating an index file that lists all classes and a main file that links to the index and all classes.

The call stack graph for this code shows the order in which the functions are called and how they relate to each other. The main function is at the top of the graph and calls the find_classes, build_graph, generate_markdown_files, and generate_index_file functions in order. The build_graph function calls the get_class_dependencies, add_method_edges, and add_attribute_edges functions, and the generate_markdown_files function calls the generate_method_markdown and generate_attribute_markdown functions.

This call stack graph can be a useful tool for understanding how the code works and how it generates documentation for Python code. It can also help developers identify any potential issues or errors in the code.

The new feature in GitHub, Git-lab, and Jet-brains IDE allows developers to easily generate documentation for their Python code using the code mentioned above. This feature provides a simple and automated way to document Python code, which can save developers time and reduce errors.

In conclusion, the call stack graph for the Python code that generates documentation for Python code is a useful tool for understanding how the code works and how it generates documentation. The new feature in GitHub, Git-lab, and Jet-brains IDE allows developers to easily generate documentation for their Python code, which can save time and reduce errors.
