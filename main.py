import os
import ast
import networkx as nx
import cProfile
import pstats

class ClassFinder:
    def __init__(self, path):
        self.path = path

    def find_classes(self):
        classes = {}
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".py") and pathToFolder in root:
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
        [graph.add_node(class_name) for class_name in classes]
        for class_name, data in classes.items():
            [graph.add_edge(class_name, method_name) for method_name in data["methods"]]
            [graph.add_edge(class_name, attribute_name) for attribute_name in data["attributes"]]

        return graph

class MarkdownGenerator:
    def __init__(self, root_path):
        self.root_path = root_path

    def generate_md_files(self, classes, graph):
        class_map = {class_name: os.path.join(self.root_path, "MD", f"{class_name}.md") for class_name in classes}
        os.makedirs(os.path.join(self.root_path, "MD"), exist_ok=True)

        # Profile the generation of Markdown files
        profiler = cProfile.Profile()
        profiler.enable()

        for class_name, data in classes.items():
            md_file_path = class_map[class_name]
            with open(md_file_path, "w") as md_file:
                md_file.write(f"# {class_name}\n\n")
                md_file.write(f"Called by: [[Main]](main.md)\n\n")

                if class_name in graph:
                    neighbors = [neighbor for neighbor in graph[class_name] if neighbor in class_map]
                    for neighbor in neighbors:
                        md_file.write(f"- [[{neighbor}]]({os.path.relpath(class_map[neighbor], os.path.dirname(md_file_path))})\n")
                    for neighbor in set(graph[class_name]) - set(neighbors):
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

            # Append profiling information to the Markdown file
            stats_file = f"{class_name}_profile.txt"
            with open(stats_file, "w") as stats:
                p = pstats.Stats(profiler, stream=stats)
                p.strip_dirs()
                p.sort_stats("cumtime")
                p.print_stats()
            with open(md_file_path, "a") as md_file:
                md_file.write(f"\n## Profiling Information\n\n```txt\n{open(stats_file).read()}\n```\n")

        profiler.disable()




class DocumentationGenerator:
    def __init__(self, root_path):
        self.root_path = root_path
        self.class_finder = ClassFinder(self.root_path)
        self.graph_builder = GraphBuilder()
        self.markdown_generator = MarkdownGenerator(self.root_path)

    def generate(self):
        # Profile the find_classes method
        pr = cProfile.Profile()
        pr.enable()
        classes = self.class_finder.find_classes()
        pr.disable()
        # Save the profiling results to a file
        with open('find_classes_profile.txt', 'w') as f:
            ps = pstats.Stats(pr, stream=f).sort_stats('tottime')
            ps.print_stats()

        # Profile the build_graph method
        pr = cProfile.Profile()
        pr.enable()
        graph = self.graph_builder.build_graph(classes)
        pr.disable()
        # Save the profiling results to a file
        with open('build_graph_profile.txt', 'w') as f:
            ps = pstats.Stats(pr, stream=f).sort_stats('tottime')
            ps.print_stats()

        # Generate the markdown files
        self.markdown_generator.generate_md_files(classes, graph)

# put here path to folder
pathToFolder = "notes-main"
generator = DocumentationGenerator(pathToFolder)
generator.generate()
