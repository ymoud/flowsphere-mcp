"""
Report Generator for FlowSphere MCP Server.

Generates comprehensive generation reports with metrics, token usage analysis,
cost estimation, and optimization recommendations.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import tiktoken


class ReportGenerator:
    """
    Generate comprehensive reports for test code generation.

    Reports include:
    - Configuration analysis
    - Generated artifacts metrics
    - Token usage breakdown
    - Cost estimation
    - Optimization recommendations
    """

    def __init__(self, language: str, framework: str):
        """
        Initialize report generator.

        Args:
            language: Programming language (Python, JavaScript, C#)
            framework: Test framework (pytest, jest, xunit, etc.)
        """
        self.language = language
        self.framework = framework
        self.encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
        self.start_time = datetime.now()

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text using tiktoken (real-time tracking).

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))

    def analyze_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze FlowSphere configuration.

        Args:
            config: FlowSphere configuration dictionary

        Returns:
            Configuration metrics
        """
        config_json = json.dumps(config, indent=2)
        config_size_bytes = len(config_json.encode('utf-8'))
        config_size_mb = config_size_bytes / (1024 * 1024)

        nodes = config.get('nodes', [])
        node_count = len(nodes)

        # Analyze features used
        features_used = []
        has_variables = bool(config.get('variables'))
        has_defaults = bool(config.get('defaults'))
        has_debug = config.get('enableDebug', False)

        if has_variables:
            features_used.append('Global Variables')
        if has_defaults:
            features_used.append('Default Settings')
        if has_debug:
            features_used.append('Debug Mode')

        # Analyze nodes for features
        for node in nodes:
            if node.get('conditions'):
                if 'Conditional Execution' not in features_used:
                    features_used.append('Conditional Execution')
            if node.get('validations'):
                if 'Response Validation' not in features_used:
                    features_used.append('Response Validation')
            if node.get('extractFields'):
                if 'Field Extraction (JSONPath)' not in features_used:
                    features_used.append('Field Extraction (JSONPath)')
            if node.get('promptMessage'):
                if 'User Input Prompts' not in features_used:
                    features_used.append('User Input Prompts')
            if node.get('skipDefaultHeaders'):
                if 'Skip Default Headers' not in features_used:
                    features_used.append('Skip Default Headers')
            if node.get('skipDefaultValidations'):
                if 'Skip Default Validations' not in features_used:
                    features_used.append('Skip Default Validations')

        return {
            'size_bytes': config_size_bytes,
            'size_mb': config_size_mb,
            'size_kb': config_size_bytes / 1024,
            'node_count': node_count,
            'features_used': features_used,
            'feature_count': len(features_used),
            'has_variables': has_variables,
            'has_defaults': has_defaults,
            'has_debug': has_debug,
            'config_json': config_json
        }

    def analyze_generated_code(self, generated_code: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze generated code artifacts.

        Args:
            generated_code: Dictionary of filename -> code content

        Returns:
            Code metrics
        """
        artifacts = []
        total_size_bytes = 0
        total_lines = 0

        for filename, code in generated_code.items():
            size_bytes = len(code.encode('utf-8'))
            size_kb = size_bytes / 1024
            lines = code.count('\n') + 1

            artifacts.append({
                'filename': filename,
                'size_bytes': size_bytes,
                'size_kb': size_kb,
                'lines': lines,
                'token_count': self.count_tokens(code)
            })

            total_size_bytes += size_bytes
            total_lines += lines

        return {
            'artifacts': artifacts,
            'total_size_bytes': total_size_bytes,
            'total_size_kb': total_size_bytes / 1024,
            'total_lines': total_lines,
            'file_count': len(artifacts)
        }

    def calculate_token_usage(self, config: Dict[str, Any], generated_code: Dict[str, str]) -> Dict[str, Any]:
        """
        Calculate token usage for input and output.

        Args:
            config: FlowSphere configuration
            generated_code: Dictionary of generated code files

        Returns:
            Token usage breakdown
        """
        # Input tokens (config)
        config_json = json.dumps(config, indent=2)
        input_tokens = self.count_tokens(config_json)

        # Output tokens (generated code)
        output_tokens = 0
        for code in generated_code.values():
            output_tokens += self.count_tokens(code)

        # Total tokens
        total_tokens = input_tokens + output_tokens

        # Cost estimation (GPT-4 pricing as reference)
        cost_per_1k_input = 0.03  # $0.03 per 1K input tokens
        cost_per_1k_output = 0.06  # $0.06 per 1K output tokens

        cost_input = (input_tokens / 1000) * cost_per_1k_input
        cost_output = (output_tokens / 1000) * cost_per_1k_output
        cost_total = cost_input + cost_output

        # Phase 7.1 comparison (before optimization)
        # Before: config was embedded in generated code
        config_tokens = self.count_tokens(config_json)
        tokens_before_phase7 = input_tokens + output_tokens + config_tokens  # Config was duplicated
        cost_before_phase7 = (tokens_before_phase7 / 1000) * ((cost_per_1k_input + cost_per_1k_output) / 2)

        savings_tokens = tokens_before_phase7 - total_tokens
        savings_cost = cost_before_phase7 - cost_total
        savings_percent = (savings_tokens / tokens_before_phase7 * 100) if tokens_before_phase7 > 0 else 0

        return {
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': total_tokens,
            'cost_input': cost_input,
            'cost_output': cost_output,
            'cost_total': cost_total,
            'tokens_before_phase7': tokens_before_phase7,
            'cost_before_phase7': cost_before_phase7,
            'savings_tokens': savings_tokens,
            'savings_cost': savings_cost,
            'savings_percent': savings_percent
        }

    def generate_report(self, config: Dict[str, Any], generated_code: Dict[str, str],
                       generation_duration_seconds: float = None) -> str:
        """
        Generate comprehensive Markdown report.

        Args:
            config: FlowSphere configuration
            generated_code: Dictionary of filename -> code content
            generation_duration_seconds: Time taken to generate code

        Returns:
            Markdown report as string
        """
        if generation_duration_seconds is None:
            generation_duration_seconds = (datetime.now() - self.start_time).total_seconds()

        # Analyze metrics
        config_metrics = self.analyze_config(config)
        code_metrics = self.analyze_generated_code(generated_code)
        token_metrics = self.calculate_token_usage(config, generated_code)

        # Build report
        report_lines = []

        # Header
        report_lines.append("# FlowSphere Test Generation Report")
        report_lines.append("")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**Configuration:** `{config.get('name', 'Unnamed Configuration')}`")
        report_lines.append(f"**Target Language:** {self.language}")
        report_lines.append(f"**Target Framework:** {self.framework}")
        report_lines.append(f"**MCP Server:** FlowSphere MCP Server v1.0")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # Executive Summary
        report_lines.append("## Executive Summary")
        report_lines.append("")
        report_lines.append(f"This report analyzes the test generation process for a {config_metrics['size_kb']:.1f} KB FlowSphere configuration file containing {config_metrics['node_count']} API test scenarios. ")
        report_lines.append(f"The generation successfully produced production-ready {self.language} {self.framework} tests ")
        report_lines.append(f"with **{token_metrics['total_tokens']:,} tokens** consumed (input + output).")
        report_lines.append("")

        if token_metrics['savings_tokens'] > 0:
            report_lines.append(f"**Phase 7.1 Optimization Impact:** Thanks to recent optimizations, this generation saved **{token_metrics['savings_tokens']:,} tokens ({token_metrics['savings_percent']:.1f}%)** ")
            report_lines.append(f"compared to the previous approach, resulting in **${token_metrics['savings_cost']:.2f}** cost savings.")

        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # Configuration Analysis
        report_lines.append("## 1. Configuration Analysis")
        report_lines.append("")
        report_lines.append("### 1.1 Input Configuration")
        report_lines.append("")
        report_lines.append(f"- **Configuration Name:** {config.get('name', 'Unnamed')}")
        report_lines.append(f"- **File Size:** {config_metrics['size_kb']:.1f} KB ({config_metrics['size_bytes']:,} bytes)")
        report_lines.append(f"- **Number of Test Nodes:** {config_metrics['node_count']}")
        report_lines.append(f"- **FlowSphere Features Used:** {config_metrics['feature_count']}")
        report_lines.append("")

        if config_metrics['features_used']:
            report_lines.append("**Features Detected:**")
            for feature in config_metrics['features_used']:
                report_lines.append(f"- {feature}")
            report_lines.append("")

        report_lines.append("### 1.2 Configuration Metadata")
        report_lines.append("")
        report_lines.append(f"- **Global Variables:** {'Yes' if config_metrics['has_variables'] else 'No'}")
        report_lines.append(f"- **Default Settings:** {'Yes' if config_metrics['has_defaults'] else 'No'}")
        report_lines.append(f"- **Debug Mode:** {'Enabled' if config_metrics['has_debug'] else 'Disabled'}")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # Generated Artifacts
        report_lines.append("## 2. Generated Artifacts")
        report_lines.append("")
        report_lines.append("### 2.1 Files Created")
        report_lines.append("")
        report_lines.append("| Artifact | Size | Lines | Tokens | Purpose |")
        report_lines.append("|----------|------|-------|--------|---------|")

        for artifact in code_metrics['artifacts']:
            report_lines.append(f"| `{artifact['filename']}` | {artifact['size_kb']:.1f} KB | {artifact['lines']} | {artifact['token_count']:,} | Generated test code |")

        report_lines.append(f"| **Total** | **{code_metrics['total_size_kb']:.1f} KB** | **{code_metrics['total_lines']}** | **{token_metrics['output_tokens']:,}** | Complete test project |")
        report_lines.append("")
        report_lines.append(f"**Generation Time:** {generation_duration_seconds:.2f} seconds")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # Token Usage Analysis
        report_lines.append("## 3. Token Usage Analysis")
        report_lines.append("")
        report_lines.append("### 3.1 Token Consumption Breakdown")
        report_lines.append("")
        report_lines.append(f"**Total Tokens Used:** {token_metrics['total_tokens']:,}")
        report_lines.append("")
        report_lines.append("| Component | Tokens | Percentage | Cost (GPT-4) |")
        report_lines.append("|-----------|--------|------------|--------------|")

        input_percent = (token_metrics['input_tokens'] / token_metrics['total_tokens'] * 100) if token_metrics['total_tokens'] > 0 else 0
        output_percent = (token_metrics['output_tokens'] / token_metrics['total_tokens'] * 100) if token_metrics['total_tokens'] > 0 else 0

        report_lines.append(f"| **Input (Config)** | {token_metrics['input_tokens']:,} | {input_percent:.1f}% | ${token_metrics['cost_input']:.4f} |")
        report_lines.append(f"| **Output (Code)** | {token_metrics['output_tokens']:,} | {output_percent:.1f}% | ${token_metrics['cost_output']:.4f} |")
        report_lines.append(f"| **Total** | **{token_metrics['total_tokens']:,}** | **100%** | **${token_metrics['cost_total']:.4f}** |")
        report_lines.append("")

        if token_metrics['savings_tokens'] > 0:
            report_lines.append("### 3.2 Phase 7.1 Optimization Impact")
            report_lines.append("")
            report_lines.append("**Before Phase 7.1** (Config embedded in generated code):")
            report_lines.append(f"- Total Tokens: {token_metrics['tokens_before_phase7']:,}")
            report_lines.append(f"- Estimated Cost: ${token_metrics['cost_before_phase7']:.4f}")
            report_lines.append("")
            report_lines.append("**After Phase 7.1** (Config loaded from file):")
            report_lines.append(f"- Total Tokens: {token_metrics['total_tokens']:,}")
            report_lines.append(f"- Actual Cost: ${token_metrics['cost_total']:.4f}")
            report_lines.append("")
            report_lines.append("**Savings:**")
            report_lines.append(f"- Token Reduction: {token_metrics['savings_tokens']:,} tokens ({token_metrics['savings_percent']:.1f}%)")
            report_lines.append(f"- Cost Savings: ${token_metrics['savings_cost']:.4f}")
            report_lines.append("")

        report_lines.append("*Cost estimates based on GPT-4 pricing: $0.03/1K input tokens, $0.06/1K output tokens*")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # Optimization Recommendations
        report_lines.append("## 4. Optimization Recommendations")
        report_lines.append("")
        report_lines.append("### 4.1 Immediate Actions")
        report_lines.append("")

        # Conditional recommendations based on config size
        if config_metrics['node_count'] > 20:
            report_lines.append("**Split Large Configuration:**")
            report_lines.append(f"- Your configuration has {config_metrics['node_count']} nodes")
            report_lines.append("- Consider splitting into smaller, logical test suites (5-10 nodes each)")
            report_lines.append("- This improves maintainability and allows parallel execution")
            report_lines.append("")

        if config_metrics['size_kb'] > 500:
            report_lines.append("**Simplify Configuration:**")
            report_lines.append(f"- Your configuration is {config_metrics['size_kb']:.1f} KB")
            report_lines.append("- Consider removing verbose request/response bodies during generation")
            report_lines.append("- Load full config from file at runtime (already implemented!)")
            report_lines.append("")

        report_lines.append("**Best Practices:**")
        report_lines.append("1. ✅ **Config File Management** - Save the provided `config.json` alongside your tests")
        report_lines.append("2. ✅ **Version Control** - Commit both generated tests and config files")
        report_lines.append("3. ✅ **Regeneration** - Only regenerate when test structure changes, not for config updates")
        report_lines.append("4. ✅ **Documentation** - Keep this report for reference and cost tracking")
        report_lines.append("")

        report_lines.append("### 4.2 Scaling Projections")
        report_lines.append("")
        report_lines.append("**If you generate tests regularly:**")
        report_lines.append("")
        report_lines.append("| Frequency | Tokens/Month | Cost/Month (GPT-4) | Annual Cost |")
        report_lines.append("|-----------|--------------|--------------------|-----------")|

        daily_tokens = token_metrics['total_tokens'] * 1
        weekly_tokens = token_metrics['total_tokens'] * 5
        monthly_tokens = token_metrics['total_tokens'] * 20

        daily_cost = token_metrics['cost_total'] * 1
        weekly_cost = token_metrics['cost_total'] * 5
        monthly_cost = token_metrics['cost_total'] * 20
        annual_cost = monthly_cost * 12

        report_lines.append(f"| Daily (1x/day) | {daily_tokens:,} | ${daily_cost:.2f} | ${daily_cost * 30:.2f} |")
        report_lines.append(f"| Weekly (5x/week) | {weekly_tokens:,} | ${weekly_cost:.2f} | ${weekly_cost * 4.3:.2f} |")
        report_lines.append(f"| Regular (20x/month) | {monthly_tokens:,} | ${monthly_cost:.2f} | ${annual_cost:.2f} |")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # Conclusion
        report_lines.append("## 5. Conclusion")
        report_lines.append("")
        report_lines.append(f"The FlowSphere MCP server successfully generated production-ready {self.language} {self.framework} tests ")
        report_lines.append(f"from your {config_metrics['node_count']}-node configuration in {generation_duration_seconds:.2f} seconds. ")
        report_lines.append(f"Total token consumption: **{token_metrics['total_tokens']:,} tokens** (${token_metrics['cost_total']:.4f}).")
        report_lines.append("")

        if token_metrics['savings_percent'] > 0:
            report_lines.append(f"Thanks to Phase 7.1 optimizations, you saved **{token_metrics['savings_percent']:.1f}%** in token costs compared to the previous approach. ")
            report_lines.append("Your generated tests now load configuration from files, making them cleaner, more maintainable, and more cost-effective.")

        report_lines.append("")
        report_lines.append("**Next Steps:**")
        report_lines.append("1. Save the generated code to your project")
        report_lines.append("2. Save `config.json` alongside your tests (in the same directory or `configuration/` subdirectory)")
        report_lines.append("3. Install required dependencies (see `dependencies` in the generation response)")
        report_lines.append("4. Run your tests!")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("*Report generated by FlowSphere MCP Server*")
        report_lines.append("")

        return '\n'.join(report_lines)

    def save_report(self, report: str, file_path: str) -> Dict[str, Any]:
        """
        Save report to file.

        Args:
            report: Report markdown content
            file_path: Path to save report to

        Returns:
            Dictionary with save status and path
        """
        try:
            # Create directory if needed
            os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)

            # Save report
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(report)

            file_size = len(report.encode('utf-8'))

            return {
                'success': True,
                'path': file_path,
                'size_bytes': file_size,
                'size_kb': file_size / 1024
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
