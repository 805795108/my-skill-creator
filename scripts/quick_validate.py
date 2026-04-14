#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import sys
import os
import re
import yaml
from pathlib import Path

def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Define allowed properties
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (kebab-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Validate compatibility field if present (optional)
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."

    # Content quality checks (warnings, don't fail validation)
    warnings = []

    if description:
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in description)
        has_english = any(c.isascii() and c.isalpha() for c in description)
        if not (has_chinese and has_english):
            warnings.append("Description 建议中英双语，提升跨语言触发率")

        trigger_keywords = ["use when", "trigger", "use this", "当", "使用", "触发"]
        if not any(kw in description.lower() for kw in trigger_keywords):
            warnings.append("Description 缺少触发场景描述（建议包含 'Use when...' 或 '当...时使用'）")

        if len(description) < 50:
            warnings.append(f"Description 较短（{len(description)} 字符），可能触发覆盖不足")

    # SKILL.md body quality checks
    body = content[match.end():].strip()

    body_lines = len(body.splitlines())
    if body_lines > 500:
        warnings.append(f"SKILL.md 正文 {body_lines} 行，超过建议的 500 行上限，可能影响 Agent 注意力分配")

    has_examples = ("✅" in body and "❌" in body) or ("示例" in body and "```" in body)
    if not has_examples:
        warnings.append("SKILL.md 缺少具体示例（建议用 ✅/❌ 对比或 before/after 示例）")

    error_patterns = [r"如果.*失败", r"如果.*错误", r"if.*fail", r"fallback"]
    has_error_recovery = any(re.search(p, body, re.IGNORECASE) for p in error_patterns)
    if not has_error_recovery:
        warnings.append("SKILL.md 缺少错误恢复路径（建议写明「如果 X 失败，做 Y」）")

    verify_keywords = ["检查", "自检", "校验", "checklist", "verify"]
    if not any(kw in body.lower() for kw in verify_keywords):
        warnings.append("SKILL.md 缺少输出校验步骤（建议在末尾加自检清单）")

    first_20_lines = "\n".join(body.splitlines()[:20])
    boundary_keywords = ["不处理", "不适用", "不覆盖", "not for", "does not handle", "不需要此"]
    if not any(kw in first_20_lines.lower() for kw in boundary_keywords):
        warnings.append("SKILL.md 开头缺少触发边界说明（建议用 2-3 行声明「本 Skill 不处理的场景」）")

    refs_dir = skill_path / "references"
    if refs_dir.is_dir():
        for f in refs_dir.rglob("*.md"):
            line_count = len(f.read_text().splitlines())
            if line_count > 500:
                warnings.append(
                    f"references/{f.relative_to(refs_dir)} 超过 500 行"
                    f"（{line_count} 行），建议拆分或加目录索引"
                )

    if warnings:
        return True, "Skill is valid! Warnings:\n" + "\n".join(f"  - {w}" for w in warnings)

    return True, "Skill is valid!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)