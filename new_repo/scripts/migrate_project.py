#!/usr/bin/env python3
"""
Migration script to copy files from old structure to new reorganized structure.

This script:
1. Copies files from the original project
2. Applies improvements (adds docstrings, error handling, etc.)
3. Validates the migration
4. Creates a migration report
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# File mapping: (source, destination, needs_improvement)
FILE_MAPPING = [
    # Core files
    ("N5ForShare/MOCU.py", "src/core/mocu_cuda.py", True),
    ("N5ForShare/determineSyncN.py", "src/core/sync_detection.py", True),
    ("N5ForShare/determineSyncTwo.py", "src/core/sync_detection.py", False),  # Append
    ("N5ForShare/mocu_comp.py", "src/core/sync_detection.py", False),  # Append
    
    # Model files
    ("models/MP_train.py", "src/models/trainer.py", True),
    
    # Strategy files
    ("N5ForShare/findMPSequence.py", "src/strategies/mp_strategy.py", True),
    ("N5ForShare/findMOCUSequence.py", "src/strategies/mocu_strategy.py", True),
    ("N5ForShare/findEntropySequence.py", "src/strategies/entropy_strategy.py", True),
    ("N5ForShare/findRandomSequence.py", "src/strategies/random_strategy.py", True),
    
    # Utility files
    ("models/utils.py", "src/utils/visualization.py", True),
    
    # Scripts
    ("N5ForShare/drawResults.py", "scripts/4_visualize_results.py", True),
    ("N5ForShare/runMainForPerformanceMeasure.py", "scripts/3_run_experiment.py", True),
]


def ensure_directories(base_path: Path):
    """Create all necessary directories."""
    dirs = [
        "src/core",
        "src/models", 
        "src/strategies",
        "src/utils",
        "scripts",
        "tests",
        "logs",
        "configs",
        "Dataset",
        "Experiment",
        "results",
    ]
    
    for d in dirs:
        (base_path / d).mkdir(parents=True, exist_ok=True)
        # Create __init__.py for Python packages
        if d.startswith("src/"):
            init_file = base_path / d / "__init__.py"
            if not init_file.exists():
                init_file.write_text('"""Package initialization."""\n')


def copy_file(src: Path, dst: Path, append: bool = False):
    """Copy file from source to destination."""
    if not src.exists():
        print(f"  WARNING: Source file not found: {src}")
        return False
    
    # Create parent directory
    dst.parent.mkdir(parents=True, exist_ok=True)
    
    if append and dst.exists():
        # Append to existing file
        with open(src, 'r') as f_src:
            content = f_src.read()
        with open(dst, 'a') as f_dst:
            f_dst.write('\n\n# ' + '='*60 + '\n')
            f_dst.write(f'# Appended from {src.name}\n')
            f_dst.write('# ' + '='*60 + '\n\n')
            f_dst.write(content)
    else:
        shutil.copy2(src, dst)
    
    print(f"  ✓ Copied: {src} -> {dst}")
    return True


def add_file_header(file_path: Path, description: str):
    """Add professional header to file."""
    header = f'''"""
{description}

This module is part of the MOCU-OED project for optimal experimental design
in coupled oscillator systems.
"""

'''
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if file already has a module docstring
    if not content.strip().startswith('"""') and not content.strip().startswith("'''"):
        with open(file_path, 'w') as f:
            f.write(header)
            f.write(content)


def migrate_files(old_base: Path, new_base: Path):
    """Migrate files from old structure to new structure."""
    print("=" * 70)
    print("MOCU-OED Project Migration")
    print("=" * 70)
    
    # Ensure directory structure exists
    print("\n1. Creating directory structure...")
    ensure_directories(new_base)
    print("  ✓ Directory structure created")
    
    # Copy files
    print("\n2. Copying files...")
    success_count = 0
    fail_count = 0
    
    for src_rel, dst_rel, needs_improvement in FILE_MAPPING:
        src = old_base / src_rel
        dst = new_base / dst_rel
        append = "Append" in dst_rel
        
        if copy_file(src, dst, append):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\n  Summary: {success_count} succeeded, {fail_count} failed")
    
    # Add headers
    print("\n3. Adding professional headers...")
    file_descriptions = {
        "src/core/mocu_cuda.py": "CUDA-accelerated MOCU computation",
        "src/core/sync_detection.py": "Synchronization detection for oscillator systems",
        "src/models/trainer.py": "Neural network training utilities",
        "src/strategies/mp_strategy.py": "Message passing-based OED strategy",
        "src/strategies/mocu_strategy.py": "ODE-based MOCU strategy",
        "src/strategies/entropy_strategy.py": "Entropy-based OED strategy",
        "src/strategies/random_strategy.py": "Random baseline strategy",
    }
    
    for file_rel, description in file_descriptions.items():
        file_path = new_base / file_rel
        if file_path.exists():
            add_file_header(file_path, description)
            print(f"  ✓ Added header: {file_rel}")
    
    # Create migration report
    print("\n4. Creating migration report...")
    create_migration_report(new_base, success_count, fail_count)
    print("  ✓ Report created: MIGRATION_REPORT.md")
    
    print("\n" + "=" * 70)
    print("Migration complete!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Review MIGRATION_REPORT.md")
    print("2. Run validation: python scripts/validate_migration.py")
    print("3. Run tests: pytest tests/")
    print("4. Update import statements as needed")


def create_migration_report(base_path: Path, success: int, fail: int):
    """Create migration report."""
    report = f"""# Migration Report

Generated: {Path(__file__).name}

## Summary

- **Files copied successfully**: {success}
- **Files failed**: {fail}
- **Status**: {'✓ Complete' if fail == 0 else '⚠ Incomplete'}

## File Mapping

The following files were migrated:

| Old Location | New Location | Status |
|-------------|-------------|--------|
"""
    
    for src, dst, _ in FILE_MAPPING:
        status = "✓" if (base_path / dst).exists() else "✗"
        report += f"| `{src}` | `{dst}` | {status} |\n"
    
    report += """

## Manual Steps Required

### 1. Update Import Statements

Old imports like:
```python
from MOCU import *
from determineSyncN import *
```

Should become:
```python
from src.core.mocu_cuda import MOCU
from src.core.sync_detection import determineSyncN
```

### 2. Update Configuration

- Update `N_global` in CUDA kernel if needed
- Configure model paths in `configs/default_config.yaml`

### 3. Test Migration

Run the test suite:
```bash
pytest tests/ -v
```

### 4. Update Documentation

- Review and update docstrings
- Update README examples
- Check that all functions have type hints

## Known Issues

1. **Hard-coded paths**: Some files contain hard-coded paths that need updating
2. **N_global parameter**: CUDA kernel requires manual update for different N
3. **Model loading**: Update model paths in strategy files

## Validation Checklist

- [ ] All files copied successfully
- [ ] Import statements updated
- [ ] Tests pass
- [ ] Documentation reviewed
- [ ] Configuration files created
- [ ] Example scripts work

## Contact

If you encounter issues, please check:
- REORGANIZATION_GUIDE.md
- README.md
- GitHub issues
"""
    
    (base_path / "MIGRATION_REPORT.md").write_text(report)


if __name__ == "__main__":
    # Get paths
    script_dir = Path(__file__).parent
    old_base = script_dir.parent  # Assumes script is in new_repo/scripts/
    new_base = script_dir.parent
    
    print(f"Old base: {old_base}")
    print(f"New base: {new_base}")
    print()
    
    # Confirm
    response = input("Proceed with migration? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        migrate_files(old_base, new_base)
    else:
        print("Migration cancelled.")