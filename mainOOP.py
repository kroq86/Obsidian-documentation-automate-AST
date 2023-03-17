import os
import ast
import networkx as nx


class ClassFinder:
    def __init__(self, path):
        self.path = path

    def find_classes(self):
        classes = {}
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".py") and "notes-main" in root:
                    with open(os.path.join(root, file), "r") as source:
                        try:
                            tree = ast.parse(source.read())
                        except SyntaxError as e:
                            print(f"Syntax error in {os.path.join(root, file)}: {e}")
                            continue
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ClassDef):
                                class_name = node.name
                                classes[class_name] = {
                                    "methods": [],
                                    "attributes": []
                                }
                                for method_node in ast.walk(node):
                                    if isinstance(method_node, ast.FunctionDef):
                                        method_name = method_node.name
                                        classes[class_name]["methods"].append(method_name)
                                    elif isinstance(method_node, ast.Assign):
                                        if isinstance(method_node.targets[0], ast.Name):
                                            attribute_name = method_node.targets[0].id
                                            classes[class_name]["attributes"].append(attribute_name)

        return classes


class GraphBuilder:
    def build_graph(self, classes):
        graph = nx.DiGraph()

        for class_name in classes:
            graph.add_node(class_name)

        for class_name, data in classes.items():
            for method_name in data["methods"]:
                graph.add_edge(class_name, method_name)

            for attribute_name in data["attributes"]:
                graph.add_edge(class_name, attribute_name)

        return graph


class MarkdownGenerator:
    def __init__(self, root_path):
        self.root_path = root_path

    def generate_md_files(self, classes, graph):
        class_map = {}
        for class_name in classes:
            md_file_path = os.path.join(self.root_path, "MD", f"{class_name}.md")
            class_map[class_name] = md_file_path

        os.makedirs(os.path.join(self.root_path, "MD"), exist_ok=True)

        for class_name, data in classes.items():
            md_file_path = class_map[class_name]
            with open(md_file_path, "w") as md_file:
                md_file.write(f"# {class_name}\n\n")
                md_file.write(f"Called by: [[Main]](main.md)\n\n")

                if class_name in graph:
                    neighbors = list(graph[class_name])
                    for neighbor in neighbors:
                        if neighbor in class_map:
                            md_file.write(f"- [[{neighbor}]]({os.path.relpath(class_map[neighbor], os.path.dirname(md_file_path))})\n")
                        else:
                            md_file.write(f"- {neighbor}\n")
                md_file.write("\n")

                if "attributes" in data:
                    md_file.write("## Attributes\n\n")
                    for attribute_name in data["attributes"]:
                        md_file.write(f"- `{attribute_name}`\n")
                    md_file.write("\n")

                if "methods" in data:
                    md_file.write("## Methods\n\n")
                    for method_name in data["methods"]:
                        md_file.write(f"- [{method_name}]({method_name}.md)\n")
                    md_file.write("\n")


class DocumentationGenerator:
    def __init__(self, root_path):
        self.root_path = root_path
        self.class_finder = ClassFinder(self.root_path)
        self.graph_builder = GraphBuilder()
        self.markdown_generator = MarkdownGenerator(self.root_path)

    def generate(self):
        classes = self.class_finder.find_classes()
        graph = self.graph_builder.build_graph(classes)
        self.markdown_generator.generate_md_files(classes, graph)

# put here path to folder
generator = DocumentationGenerator("pathToFolder")
generator.generate()

