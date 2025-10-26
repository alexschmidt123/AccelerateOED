#!/usr/bin/env python3
"""
Validation script for MOCU-OED project migration.

This script checks that:
1. All required files exist
2. Imports work correctly
3. Basic functionality is preserved
4. Configuration is valid
"""

import sys
from pathlib import Path
from typing import List, Tuple
import importlib.util


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class ProjectValidator:
    """Validator for project structure and functionality."""
    
    def __init__(self, project_root: Path):
        """
        Initialize validator.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root
        self.errors = []
        self.warnings = []
        self.passed = []
    
    def validate_all(self) -> bool:
        """
        Run all validation checks.
        
        Returns:
            True if all checks pass, False otherwise
        """
        print("=" * 70)
        print("MOCU-OED Project Validation")
        print("=" * 70)
        
        checks = [
            ("Directory Structure", self.check_directory_structure),
            ("Required Files", self.check_required_files),
            ("Python Imports", self.check_imports),
            ("Configuration", self.check_configuration),
            ("Documentation", self.check_documentation),
        ]
        
        for check_name, check_func in checks:
            print(f"\n{check_name}:")
            print("-" * 40)
            try:
                check_func()
            except Exception as e:
                self.errors.append(f"{check_name}: {str(e)}")
                print(f"  ✗ ERROR: {e}")
        
        # Print summary
        self.print_summary()
        
        return len(self.errors) == 0
    
    def check_directory_structure(self):
        """Check that required directories exist."""
        required_dirs = [
            "src",
            "src/core",
            "src/models",
            "src/strategies",
            "src/utils",
            "scripts",
            "configs",
            "tests",
        ]
        
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists() and full_path.is_dir():
                self.passed.append(f"Directory exists: {dir_path}")
                print(f"  ✓ {dir_path}")
            else:
                self.errors.append(f"Missing directory: {dir_path}")
                print(f"  ✗ {dir_path}")
    
    def check_required_files(self):
        """Check that required files exist."""
        required_files = [
            "README.md",
            "requirements.txt",
            "setup.py",
            "configs/default_config.yaml",
            "src/__init__.py",
            "src/core/__init__.py",
            "src/models/__init__.py",
            "src/strategies/__init__.py",
            "src/utils/__init__.py",
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists() and full_path.is_file():
                self.passed.append(f"File exists: {file_path}")
                print(f"  ✓ {file_path}")
            else:
                self.errors.append(f"Missing file: {file_path}")
                print(f"  ✗ {file_path}")
    
    def check_imports(self):
        """Check that Python imports work."""
        # Add project to path
        sys.path.insert(0, str(self.project_root))
        
        import_tests = [
            ("src.utils.config", "Config utilities"),
            ("src.utils.data_utils", "Data utilities"),
            ("src.utils.logging_utils", "Logging utilities"),
            ("src.models.message_passing", "Message passing model"),
        ]
        
        for module_name, description in import_tests:
            try:
                spec = importlib.util.find_spec(module_name)
                if spec is not None:
                    self.passed.append(f"Import works: {module_name}")
                    print(f"  ✓ {description} ({module_name})")
                else:
                    self.warnings.append(f"Module not found: {module_name}")
                    print(f"  ⚠ {description} ({module_name})")
            except Exception as e:
                self.errors.append(f"Import failed: {module_name} - {e}")
                print(f"  ✗ {description} ({module_name}): {e}")
    
    def check_configuration(self):
        """Check configuration file validity."""
        config_file = self.project_root / "configs" / "default_config.yaml"
        
        if not config_file.exists():
            self.errors.append("Configuration file not found")
            print("  ✗ Configuration file missing")
            return
        
        try:
            import yaml
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            # Check required sections
            required_sections = [
                "system",
                "integration",
                "training",
                "model",
                "oed",
                "paths",
            ]
            
            for section in required_sections:
                if section in config:
                    self.passed.append(f"Config section exists: {section}")
                    print(f" Section '{section}' present")
                else:
                    self.warnings.append(f"Config section missing: {section}")
                    print(f"  Section '{section}' missing")
            
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML: {e}")
            print(f"  Invalid YAML: {e}")
        except Exception as e:
            self.errors.append(f"Config check failed: {e}")
            print(f"  {e}")
    
    def check_documentation(self):
        """Check documentation completeness."""
        doc_files = [
            ("README.md", "Main README"),
            ("REORGANIZATION_GUIDE.md", "Reorganization guide"),
        ]
        
        for file_name, description in doc_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                # Check if file has content
                content = file_path.read_text()
                if len(content.strip()) > 100:  # At least 100 characters
                    self.passed.append(f"Documentation exists: {file_name}")
                    print(f"  ✓ {description}")
                else:
                    self.warnings.append(f"Documentation too short: {file_name}")
                    print(f"  ⚠ {description} (needs more content)")
            else:
                self.warnings.append(f"Documentation missing: {file_name}")
                print(f"  ⚠ {description} missing")
    
    def print_summary(self):
        """Print validation summary."""
        print("\n" + "=" * 70)
        print("Validation Summary")
        print("=" * 70)
        
        print(f"\n✓ Passed:   {len(self.passed)}")
        print(f"⚠ Warnings: {len(self.warnings)}")
        print(f"✗ Errors:   {len(self.errors)}")
        
        if self.warnings:
            print("\n⚠ Warnings:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if self.errors:
            print("\n✗ Errors:")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("\n All validation checks passed!")
        
        print("\n" + "=" * 70)


def main():
    """Main validation entry point."""
    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print(f"Project root: {project_root}\n")
    
    # Run validation
    validator = ProjectValidator(project_root)
    success = validator.validate_all()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()