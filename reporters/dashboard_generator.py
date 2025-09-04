"""
Dashboard Generator for UTA System

Creates a comprehensive dashboard for showcasing the Universal Tester-Agent
system to potential clients, including overview, strategies, scenarios, and reports.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape

class DashboardGenerator:
    """Generates comprehensive dashboard for UTA system."""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.templates_dir = self.base_dir / "reporters" / "templates"
        self.scenarios_dir = self.base_dir / "scenarios"
        self.agents_dir = self.base_dir / "agents"
        self.judges_dir = self.base_dir / "judges"
        
    def generate_dashboard(self, output_dir: str = "dashboard") -> str:
        """Generate complete dashboard with all pages."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate all dashboard pages
        pages = {
            "index": self._generate_overview_page(output_path),
            "strategies": self._generate_strategies_page(output_path),
            "scenarios": self._generate_scenarios_page(output_path),
            "reports": self._generate_reports_page(output_path),
            "architecture": self._generate_architecture_page(output_path)
        }
        
        return str(output_path)
    
    def _generate_overview_page(self, output_path: Path) -> str:
        """Generate main overview/dashboard page."""
        # Collect system statistics
        stats = self._collect_system_stats()
        
        # Get recent reports
        recent_reports = self._get_recent_reports()
        
        # Get available scenarios by category
        scenarios_by_category = self._get_scenarios_by_category()
        
        # Get available strategies
        strategies = self._get_available_strategies()
        
        env = Environment(loader=FileSystemLoader(self.templates_dir), autoescape=select_autoescape())
        template = env.get_template('dashboard_overview.html.j2')
        
        html = template.render(
            stats=stats,
            recent_reports=recent_reports,
            scenarios_by_category=scenarios_by_category,
            strategies=strategies
        )
        
        page_path = output_path / "index.html"
        page_path.write_text(html, encoding='utf-8')
        return str(page_path)
    
    def _generate_strategies_page(self, output_path: Path) -> str:
        """Generate strategies showcase page."""
        strategies = self._get_detailed_strategies()
        
        env = Environment(loader=FileSystemLoader(self.templates_dir), autoescape=select_autoescape())
        template = env.get_template('dashboard_strategies.html.j2')
        
        html = template.render(strategies=strategies)
        
        page_path = output_path / "strategies.html"
        page_path.write_text(html, encoding='utf-8')
        return str(page_path)
    
    def _generate_scenarios_page(self, output_path: Path) -> str:
        """Generate scenarios showcase page."""
        scenarios = self._get_detailed_scenarios()
        
        env = Environment(loader=FileSystemLoader(self.templates_dir), autoescape=select_autoescape())
        template = env.get_template('dashboard_scenarios.html.j2')
        
        html = template.render(scenarios=scenarios)
        
        page_path = output_path / "scenarios.html"
        page_path.write_text(html, encoding='utf-8')
        return str(page_path)
    
    def _generate_reports_page(self, output_path: Path) -> str:
        """Generate reports showcase page."""
        reports = self._get_all_reports()
        
        env = Environment(loader=FileSystemLoader(self.templates_dir), autoescape=select_autoescape())
        template = env.get_template('dashboard_reports.html.j2')
        
        html = template.render(reports=reports)
        
        page_path = output_path / "reports.html"
        page_path.write_text(html, encoding='utf-8')
        return str(page_path)
    
    def _generate_architecture_page(self, output_path: Path) -> str:
        """Generate architecture overview page."""
        architecture_info = self._get_architecture_info()
        
        env = Environment(loader=FileSystemLoader(self.templates_dir), autoescape=select_autoescape())
        template = env.get_template('dashboard_architecture.html.j2')
        
        html = template.render(architecture=architecture_info)
        
        page_path = output_path / "architecture.html"
        page_path.write_text(html, encoding='utf-8')
        return str(page_path)
    
    def _collect_system_stats(self) -> Dict[str, Any]:
        """Collect system statistics."""
        stats = {
            "total_scenarios": 0,
            "total_strategies": 0,
            "total_reports": 0,
            "scenarios_by_type": {},
            "strategies_by_type": {},
            "recent_activity": []
        }
        
        # Count scenarios
        for scenario_file in self.scenarios_dir.rglob("*.yaml"):
            try:
                with open(scenario_file, 'r') as f:
                    scenario = yaml.safe_load(f)
                
                stats["total_scenarios"] += 1
                
                # Categorize by type
                scenario_type = scenario_file.parent.name
                stats["scenarios_by_type"][scenario_type] = stats["scenarios_by_type"].get(scenario_type, 0) + 1
                
            except Exception:
                continue
        
        # Count strategies
        strategy_files = list(self.agents_dir.rglob("strategies/*.py"))
        stats["total_strategies"] = len([f for f in strategy_files if f.name != "__init__.py" and f.name != "base_strategy.py"])
        
        # Count reports
        report_dirs = [d for d in self.base_dir.glob("out_*") if d.is_dir()]
        stats["total_reports"] = len(report_dirs)
        
        return stats
    
    def _get_recent_reports(self) -> List[Dict[str, Any]]:
        """Get recent test reports."""
        reports = []
        
        for report_dir in sorted(self.base_dir.glob("out_*"), key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
            if not report_dir.is_dir():
                continue
                
            results_file = report_dir / "results.json"
            if results_file.exists():
                try:
                    with open(results_file, 'r') as f:
                        data = json.load(f)
                    
                    reports.append({
                        "name": report_dir.name,
                        "path": str(report_dir / "report.html"),
                        "summary": data.get("summary", {}),
                        "timestamp": report_dir.stat().st_mtime
                    })
                except Exception:
                    continue
        
        return reports
    
    def _get_scenarios_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get scenarios organized by category."""
        scenarios_by_category = {}
        
        for scenario_file in self.scenarios_dir.rglob("*.yaml"):
            try:
                with open(scenario_file, 'r') as f:
                    scenario = yaml.safe_load(f)
                
                category = scenario_file.parent.name
                if category not in scenarios_by_category:
                    scenarios_by_category[category] = []
                
                scenarios_by_category[category].append({
                    "id": scenario.get("id", scenario_file.stem),
                    "title": scenario.get("title", "Untitled Scenario"),
                    "description": scenario.get("description", ""),
                    "tags": scenario.get("tags", []),
                    "file": str(scenario_file)
                })
                
            except Exception:
                continue
        
        return scenarios_by_category
    
    def _get_available_strategies(self) -> List[Dict[str, Any]]:
        """Get available testing strategies."""
        strategies = []
        
        # Read strategy registry
        registry_file = self.agents_dir / "strategies" / "registry.py"
        if registry_file.exists():
            with open(registry_file, 'r') as f:
                content = registry_file.read_text()
                
            # Extract only the actually registered strategies (not commented ones)
            import re
            # Look for self.register() calls that are not commented out
            register_matches = re.findall(r'^\s*self\.register\("([^"]+)",\s*(\w+Strategy)\)', content, re.MULTILINE)
            
            for strategy_key, strategy_name in register_matches:
                # Convert FlowIntentStrategy -> flow_intent.py
                file_name = strategy_name.replace("Strategy", "")
                # Convert camelCase to snake_case manually
                import re
                file_name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', file_name).lower()
                strategies.append({
                    "name": strategy_name,
                    "description": self._get_strategy_description(strategy_name),
                    "file": f"agents/strategies/{file_name}.py"
                })
        
        return strategies
    
    def _get_detailed_strategies(self) -> List[Dict[str, Any]]:
        """Get detailed strategy information."""
        strategies = []
        
        # Get only the actually registered strategies from registry
        registry_file = self.agents_dir / "strategies" / "registry.py"
        if registry_file.exists():
            with open(registry_file, 'r') as f:
                content = registry_file.read_text()
                
            # Extract only the actually registered strategies (not commented ones)
            import re
            register_matches = re.findall(r'^\s*self\.register\("([^"]+)",\s*(\w+Strategy)\)', content, re.MULTILINE)
            
            for strategy_key, strategy_name in register_matches:
                # Convert FlowIntentStrategy -> flow_intent.py
                file_name = strategy_name.replace("Strategy", "")
                # Convert camelCase to snake_case manually
                import re
                file_name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', file_name).lower()
                strategy_file = self.agents_dir / "strategies" / f"{file_name}.py"
                
                if strategy_file.exists():
                    try:
                        with open(strategy_file, 'r') as f:
                            file_content = strategy_file.read_text()
                        
                        # Extract docstring
                        docstring_match = re.search(r'"""(.*?)"""', file_content, re.DOTALL)
                        
                        strategies.append({
                            "name": strategy_name,
                            "description": docstring_match.group(1).strip() if docstring_match else self._get_strategy_description(strategy_name),
                            "file": str(strategy_file),
                            "code_preview": self._get_code_preview(file_content)
                        })
                        
                    except Exception:
                        # Fallback if file can't be read
                        strategies.append({
                            "name": strategy_name,
                            "description": self._get_strategy_description(strategy_name),
                            "file": str(strategy_file),
                            "code_preview": "Strategy implementation file"
                        })
        
        return strategies
    
    def _get_detailed_scenarios(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get detailed scenario information."""
        return self._get_scenarios_by_category()
    
    def _get_all_reports(self) -> List[Dict[str, Any]]:
        """Get all available reports."""
        return self._get_recent_reports()
    
    def _get_architecture_info(self) -> Dict[str, Any]:
        """Get architecture information."""
        return {
            "components": [
                {
                    "name": "Test Runner",
                    "description": "Core execution engine that orchestrates test scenarios",
                    "location": "runner/run.py"
                },
                {
                    "name": "Strategy System",
                    "description": "Pluggable testing strategies for different evaluation approaches",
                    "location": "agents/strategies/"
                },
                {
                    "name": "Judge System",
                    "description": "Multi-modal evaluation system (heuristic + LLM judges)",
                    "location": "judges/"
                },
                {
                    "name": "HTTP Adapter",
                    "description": "Integration layer for real AI agent testing",
                    "location": "agents/http_adapter.py"
                },
                {
                    "name": "Report Generator",
                    "description": "Business-ready HTML report generation",
                    "location": "reporters/"
                }
            ],
            "features": [
                "Deterministic Testing with Seeded RNG",
                "Budget Enforcement (turns, latency, cost)",
                "Multi-modal Evaluation (heuristic + LLM)",
                "Real AI Agent Integration",
                "Professional Business Reports",
                "Pluggable Strategy Architecture",
                "Policy-based Compliance Checking"
            ]
        }
    
    def _get_strategy_description(self, strategy_name: str) -> str:
        """Get strategy description."""
        descriptions = {
            "FlowIntentStrategy": "Tests natural conversation flow and intent understanding",
            "ToolHappyPathStrategy": "Tests successful tool usage and function calling",
            "MemoryCarryStrategy": "Tests context retention across conversation turns",
            "ToolErrorStrategy": "Tests error handling and recovery mechanisms"
        }
        return descriptions.get(strategy_name, "Testing strategy for AI agent evaluation")
    
    def _get_code_preview(self, content: str) -> str:
        """Get code preview for strategy."""
        lines = content.split('\n')
        # Get first 20 lines, excluding imports and class definition
        preview_lines = []
        for line in lines[:30]:
            if line.strip() and not line.strip().startswith(('import', 'from', 'class', '"""')):
                preview_lines.append(line)
                if len(preview_lines) >= 10:
                    break
        return '\n'.join(preview_lines)

def generate_dashboard(base_dir: str = ".", output_dir: str = "dashboard") -> str:
    """Generate complete UTA dashboard."""
    generator = DashboardGenerator(base_dir)
    return generator.generate_dashboard(output_dir)

if __name__ == "__main__":
    dashboard_path = generate_dashboard()
    print(f"Dashboard generated at: {dashboard_path}")
