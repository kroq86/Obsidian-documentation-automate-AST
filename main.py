#!/usr/bin/env python

import os
import ast
import json
import argparse
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
import webbrowser
from datetime import datetime


@dataclass
class AnalysisConfig:
    """Configuration for code analysis."""
    target_directories: List[str]
    exclude_patterns: List[str] = None
    include_patterns: List[str] = None
    max_depth: int = 10
    analyze_decorators: bool = True
    analyze_imports: bool = True
    analyze_calls: bool = True
    generate_html: bool = False
    open_in_browser: bool = False


@dataclass
class FunctionInfo:
    """Information about a function."""
    name: str
    decorators: List[str]
    line: int
    file_path: str
    args: List[str]
    returns: Optional[str] = None
    complexity: int = 0
    calls: List[str] = None


@dataclass
class ClassInfo:
    """Information about a class."""
    name: str
    methods: List[FunctionInfo]
    decorators: List[str]
    base_classes: List[str]
    line: int
    file_path: str


@dataclass
class ArchitecturalInsight:
    """Architectural insight or recommendation."""
    type: str  # 'warning', 'info', 'recommendation'
    title: str
    description: str
    files_affected: List[str]
    severity: str  # 'low', 'medium', 'high'


class CodeArchitectureAnalyzer:
    """Advanced code architecture analyzer with commercial features."""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.classes: Dict[str, ClassInfo] = {}
        self.functions: Dict[str, FunctionInfo] = {}
        self.decorators: Dict[str, List[Dict]] = defaultdict(list)
        self.imports: Dict[str, List[str]] = defaultdict(list)
        self.insights: List[ArchitecturalInsight] = []
        self.file_stats = {}
        
    def analyze_codebase(self, root_path: str) -> Dict:
        """Analyze the entire codebase and generate insights."""
        print("🔍 Starting comprehensive codebase analysis...")
        
        files_analyzed = 0
        total_lines = 0
        
        for target_dir in self.config.target_directories:
            full_path = Path(root_path) / target_dir
            if not full_path.exists():
                print(f"⚠️  Directory not found: {full_path}")
                continue
                
            for py_file in self._find_python_files(full_path):
                try:
                    file_info = self._analyze_file(py_file)
                    if file_info:
                        files_analyzed += 1
                        total_lines += file_info.get('lines', 0)
                        
                except Exception as e:
                    print(f"❌ Error analyzing {py_file}: {e}")
        
        # Generate architectural insights
        self._generate_insights()
        
        analysis_result = {
            'summary': {
                'files_analyzed': files_analyzed,
                'total_lines': total_lines,
                'classes_found': len(self.classes),
                'functions_found': len(self.functions),
                'decorators_found': len(self.decorators),
                'insights_generated': len(self.insights)
            },
            'classes': {name: asdict(cls) for name, cls in self.classes.items()},
            'functions': {name: asdict(func) for name, func in self.functions.items()},
            'decorators': dict(self.decorators),
            'imports': dict(self.imports),
            'insights': [asdict(insight) for insight in self.insights],
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"✅ Analysis complete: {files_analyzed} files, {len(self.insights)} insights")
        return analysis_result
    
    def _find_python_files(self, directory: Path) -> List[Path]:
        """Find all Python files in directory."""
        python_files = []
        for root, dirs, files in os.walk(directory):
            # Apply exclude patterns
            if self.config.exclude_patterns:
                dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.config.exclude_patterns)]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    
                    # Apply include patterns if specified
                    if self.config.include_patterns:
                        if not any(pattern in str(file_path) for pattern in self.config.include_patterns):
                            continue
                    
                    python_files.append(file_path)
        
        return python_files
    
    def _analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            lines = len(content.splitlines())
            
        except (SyntaxError, UnicodeDecodeError) as e:
            return {'error': str(e), 'lines': 0}
        
        file_info = {
            'path': str(file_path),
            'lines': lines,
            'classes': [],
            'functions': [],
            'imports': [],
            'complexity': 0
        }
        
        # Analyze AST nodes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._analyze_class(node, file_path)
            elif isinstance(node, ast.FunctionDef):
                self._analyze_function(node, file_path)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                self._analyze_import(node, file_path)
        
        return file_info
    
    def _analyze_class(self, node: ast.ClassDef, file_path: Path):
        """Analyze a class definition."""
        methods = []
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = FunctionInfo(
                    name=item.name,
                    decorators=[self._get_decorator_name(d) for d in item.decorator_list],
                    line=item.lineno,
                    file_path=str(file_path),
                    args=[arg.arg for arg in item.args.args],
                    complexity=self._calculate_complexity(item)
                )
                methods.append(method_info)
        
        class_info = ClassInfo(
            name=node.name,
            methods=methods,
            decorators=[self._get_decorator_name(d) for d in node.decorator_list],
            base_classes=[self._get_name(base) for base in node.bases],
            line=node.lineno,
            file_path=str(file_path)
        )
        
        self.classes[node.name] = class_info
    
    def _analyze_function(self, node: ast.FunctionDef, file_path: Path):
        """Analyze a function definition."""
        func_info = FunctionInfo(
            name=node.name,
            decorators=[self._get_decorator_name(d) for d in node.decorator_list],
            line=node.lineno,
            file_path=str(file_path),
            args=[arg.arg for arg in node.args.args],
            returns=self._get_name(node.returns) if node.returns else None,
            complexity=self._calculate_complexity(node)
        )
        
        self.functions[node.name] = func_info
        
        # Track decorator usage
        for decorator in func_info.decorators:
            if decorator:
                self.decorators[decorator].append({
                    'function': node.name,
                    'file': str(file_path),
                    'line': node.lineno
                })
    
    def _analyze_import(self, node, file_path: Path):
        """Analyze import statements."""
        if isinstance(node, ast.Import):
            for alias in node.names:
                self.imports[alias.name].append(str(file_path))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                self.imports[f"{module}.{alias.name}"].append(str(file_path))
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity
    
    def _get_decorator_name(self, decorator) -> str:
        """Extract decorator name."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            return self._get_name(decorator.func)
        elif isinstance(decorator, ast.Attribute):
            return self._get_name(decorator)
        return str(decorator)
    
    def _get_name(self, node) -> str:
        """Extract name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value = self._get_name(node.value)
            return f"{value}.{node.attr}" if value else node.attr
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        return ""
    
    def _generate_insights(self):
        """Generate architectural insights and recommendations."""
        # High complexity functions
        high_complexity_funcs = [
            func for func in self.functions.values() 
            if func.complexity > 10
        ]
        
        if high_complexity_funcs:
            self.insights.append(ArchitecturalInsight(
                type='warning',
                title='High Complexity Functions Detected',
                description=f'Found {len(high_complexity_funcs)} functions with complexity > 10. Consider refactoring.',
                files_affected=list(set(func.file_path for func in high_complexity_funcs)),
                severity='medium'
            ))
        
        # Decorator pattern analysis
        decorator_usage = {}
        for decorator, usages in self.decorators.items():
            if len(usages) > 1:
                decorator_usage[decorator] = len(usages)
        
        if decorator_usage:
            self.insights.append(ArchitecturalInsight(
                type='info',
                title='Decorator Patterns Found',
                description=f'Found {len(decorator_usage)} decorators used across multiple functions. This indicates good architectural patterns.',
                files_affected=[],
                severity='low'
            ))
        
        # Potential architectural issues
        checksum_decorators = [d for d in self.decorators.keys() if 'Checksum' in d]
        if len(checksum_decorators) > 1:
            self.insights.append(ArchitecturalInsight(
                type='recommendation',
                title='Multiple Checksum Decorator Implementations',
                description='Found multiple checksum decorator implementations. Consider consolidating for consistency.',
                files_affected=[],
                severity='medium'
            ))


class ReportGenerator:
    """Generate various report formats."""
    
    @staticmethod
    def generate_markdown_report(analysis_data: Dict, output_file: str):
        """Generate a comprehensive Markdown report."""
        with open(output_file, 'w') as f:
            f.write("# 🏗️ Code Architecture Analysis Report\n\n")
            
            # Summary
            summary = analysis_data['summary']
            f.write("## 📊 Summary\n\n")
            f.write(f"- **Files Analyzed**: {summary['files_analyzed']}\n")
            f.write(f"- **Total Lines**: {summary['total_lines']:,}\n")
            f.write(f"- **Classes Found**: {summary['classes_found']}\n")
            f.write(f"- **Functions Found**: {summary['functions_found']}\n")
            f.write(f"- **Decorators Found**: {summary['decorators_found']}\n")
            f.write(f"- **Insights Generated**: {summary['insights_generated']}\n\n")
            
            # Insights
            f.write("## 🎯 Architectural Insights\n\n")
            for insight in analysis_data['insights']:
                icon = {'warning': '⚠️', 'info': 'ℹ️', 'recommendation': '💡'}[insight['type']]
                f.write(f"### {icon} {insight['title']}\n")
                f.write(f"**Severity**: {insight['severity'].upper()}\n\n")
                f.write(f"{insight['description']}\n\n")
                if insight['files_affected']:
                    f.write("**Files Affected**:\n")
                    for file_path in insight['files_affected']:
                        f.write(f"- `{file_path}`\n")
                    f.write("\n")
            
            # Decorator Usage
            f.write("## 🎨 Decorator Patterns\n\n")
            for decorator, usages in analysis_data['decorators'].items():
                f.write(f"### `@{decorator}` ({len(usages)} usages)\n")
                for usage in usages[:5]:  # Limit to first 5
                    f.write(f"- `{usage['function']}` in `{usage['file']}:{usage['line']}`\n")
                if len(usages) > 5:
                    f.write(f"- ... and {len(usages) - 5} more\n")
                f.write("\n")
            
            # High Complexity Functions
            f.write("## 🔥 Complexity Analysis\n\n")
            high_complexity = [
                func for func in analysis_data['functions'].values()
                if func['complexity'] > 8
            ]
            
            if high_complexity:
                f.write("### Functions with High Complexity (>8)\n\n")
                for func in sorted(high_complexity, key=lambda x: x['complexity'], reverse=True):
                    f.write(f"- `{func['name']}` (complexity: {func['complexity']}) - `{func['file_path']}:{func['line']}`\n")
            else:
                f.write("✅ No high-complexity functions found!\n")
            
            f.write(f"\n---\n*Report generated on {analysis_data['timestamp']}*\n")
    
    @staticmethod
    def generate_cursor_integration(analysis_data: Dict, output_file: str):
        """Generate Cursor IDE integration file."""
        cursor_data = {
            'version': '1.0',
            'type': 'architecture_analysis',
            'timestamp': analysis_data['timestamp'],
            'summary': analysis_data['summary'],
            'hotspots': [],
            'recommendations': []
        }
        
        # Add high-complexity functions as hotspots
        for func in analysis_data['functions'].values():
            if func['complexity'] > 10:
                cursor_data['hotspots'].append({
                    'type': 'high_complexity',
                    'file': func['file_path'],
                    'line': func['line'],
                    'function': func['name'],
                    'complexity': func['complexity'],
                    'message': f"High complexity function ({func['complexity']}). Consider refactoring."
                })
        
        # Add insights as recommendations
        for insight in analysis_data['insights']:
            cursor_data['recommendations'].append({
                'type': insight['type'],
                'title': insight['title'],
                'description': insight['description'],
                'severity': insight['severity'],
                'files': insight['files_affected']
            })
        
        with open(output_file, 'w') as f:
            json.dump(cursor_data, f, indent=2)


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='🏗️ Code Architecture Analyzer - Understand your codebase architecture'
    )
    parser.add_argument('path', help='Root path to analyze')
    parser.add_argument(
        '--dirs', 
        nargs='+', 
        default=['src'], 
        help='Directories to analyze (default: src)'
    )
    parser.add_argument(
        '--exclude', 
        nargs='+', 
        help='Patterns to exclude'
    )
    parser.add_argument(
        '--output', 
        default='architecture_analysis', 
        help='Output file prefix (default: architecture_analysis)'
    )
    parser.add_argument(
        '--html', 
        action='store_true', 
        help='Generate HTML report'
    )
    parser.add_argument(
        '--cursor', 
        action='store_true', 
        help='Generate Cursor IDE integration file'
    )
    parser.add_argument(
        '--open', 
        action='store_true', 
        help='Open report in browser'
    )
    
    args = parser.parse_args()
    
    # Create configuration
    config = AnalysisConfig(
        target_directories=args.dirs,
        exclude_patterns=args.exclude,
        generate_html=args.html,
        open_in_browser=args.open
    )
    
    # Run analysis
    analyzer = CodeArchitectureAnalyzer(config)
    analysis_data = analyzer.analyze_codebase(args.path)
    
    # Generate reports
    md_file = f"{args.output}.md"
    json_file = f"{args.output}.json"
    
    ReportGenerator.generate_markdown_report(analysis_data, md_file)
    
    with open(json_file, 'w') as f:
        json.dump(analysis_data, f, indent=2)
    
    if args.cursor:
        cursor_file = f"{args.output}_cursor.json"
        ReportGenerator.generate_cursor_integration(analysis_data, cursor_file)
        print(f"📱 Cursor integration file: {cursor_file}")
    
    print(f"📝 Reports generated:")
    print(f"  - Markdown: {md_file}")
    print(f"  - JSON: {json_file}")
    
    if args.open:
        webbrowser.open(f"file://{os.path.abspath(md_file)}")


if __name__ == "__main__":
    main() 
