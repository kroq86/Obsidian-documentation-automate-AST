import os
import ast
import networkx as nx

def _find_classes(path):
    classes = {}

    for root, dirs, files in os.walk(path):
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

def _build_graph(classes):
    graph = nx.DiGraph()

    for class_name in classes:
        graph.add_node(class_name)

    for class_name, data in classes.items():
        for method_name in data["methods"]:
            graph.add_edge(class_name, method_name)

        for attribute_name in data["attributes"]:
            graph.add_edge(class_name, attribute_name)

    return graph

def _generate_md_files(classes, graph, root_path):
    class_map = {}
    for class_name in classes:
        md_file_path = os.path.join(root_path, "MD", f"{class_name}.md")
        class_map[class_name] = md_file_path

    os.makedirs(os.path.join(root_path, "MD"), exist_ok=True)

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


def generate_index_file(classes, root_path):
    with open(os.path.join(root_path, "MD", "index.md"), "w") as index_file:
        index_file.write("# Index\n\n")
        for class_name in classes:
            index_file.write(f"- [[{class_name}]](./{class_name}.md)\n")
        index_file.write("\n")

def generate_main_file(classes, root_path):
    with open(os.path.join(root_path, "MD", "main.md"), "w") as main_file:
        main_file.write("# Main\n\n")
        main_file.write("## Classes\n\n")
        for class_name in classes:
            main_file.write(f"- [[{class_name}]](./{class_name}.md)\n")
        main_file.write("\n")
        main_file.write(f"- [[Index]](./index.md)\n")


def generate_documentation(root_path):
    classes = _find_classes(root_path)
    graph = _build_graph(classes)
    _generate_md_files(classes, graph, root_path)
    generate_index_file(classes, root_path)
    generate_main_file(classes, root_path)


if __name__ == "__main__":
    generate_documentation(".")
