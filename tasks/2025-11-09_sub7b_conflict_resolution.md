# Sub-Task 7B: Conflict Resolution Helpers

## Parent Job
Week 7: Branch Management & Merging

## Story Points
3

## Scope
Implement automatic conflict resolution with heuristics for simple conflicts and flagging for complex ones.

## Can Run in Parallel
YES - Parallel with 7A (branch management), these are helper functions

## Todos
- [ ] Implement auto_resolve_conflicts() helper
- [ ] Handle non-code file conflicts (accept incoming)
- [ ] Apply conflict resolution heuristics for code
- [ ] Implement is_non_code_file() classifier
- [ ] Implement can_auto_resolve_code() checker
- [ ] Implement apply_resolution_heuristics() for code conflicts
- [ ] Flag complex conflicts for manual intervention
- [ ] Add conflict errors to state
- [ ] Write unit tests for conflict resolution
- [ ] Test conflict resolution with simulated conflicts

## Files to Create/Modify
- sprint-workflow/langgraph/nodes/git.py (modify - add conflict resolution)
- sprint-workflow/langgraph/state.py (modify - add conflict_errors field)
- sprint-workflow/tests/langgraph/test_git_nodes.py (modify - add conflict tests)

## Dependencies
- None (helper functions)

## Blocks
- None (can be integrated into 7A when ready)

## Implementation Notes
```python
def auto_resolve_conflicts(conflicts: list) -> bool:
    """Attempt to auto-resolve conflicts."""
    for conflict_file in conflicts:
        # Non-code files: accept incoming
        if is_non_code_file(conflict_file):
            run_command(f"git checkout --theirs {conflict_file}")
            run_command(f"git add {conflict_file}")
            continue

        # Code files: apply heuristics
        if can_auto_resolve_code(conflict_file):
            apply_resolution_heuristics(conflict_file)
            run_command(f"git add {conflict_file}")
        else:
            # Complex conflict - cannot auto-resolve
            return False

    # All conflicts resolved
    run_command("git rebase --continue")
    return True

def is_non_code_file(filepath: str) -> bool:
    """Check if file is non-code (docs, config, etc.)."""
    non_code_extensions = [
        '.md', '.txt', '.json', '.yaml', '.yml',
        '.lock', '.toml', '.ini', '.cfg'
    ]

    _, ext = os.path.splitext(filepath)
    return ext.lower() in non_code_extensions

def can_auto_resolve_code(filepath: str) -> bool:
    """Check if code conflict can be auto-resolved."""
    # Read conflict markers
    with open(filepath, 'r') as f:
        content = f.read()

    # Check for simple conflict patterns
    conflict_sections = re.findall(
        r'<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> .*',
        content,
        re.DOTALL
    )

    for head_section, incoming_section in conflict_sections:
        # Whitespace-only conflict
        if head_section.strip() == incoming_section.strip():
            return True

        # Import conflict (can merge)
        if is_import_conflict(head_section, incoming_section):
            return True

        # Complex logic conflict
        return False

    return True

def apply_resolution_heuristics(filepath: str):
    """Apply auto-resolution heuristics to code file."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Whitespace conflicts: accept incoming
    content = resolve_whitespace_conflicts(content)

    # Import conflicts: merge both sets
    content = merge_import_conflicts(content)

    # Write resolved content
    with open(filepath, 'w') as f:
        f.write(content)

def is_import_conflict(head_section: str, incoming_section: str) -> bool:
    """Check if conflict is in import statements."""
    head_lines = set(head_section.strip().split('\n'))
    incoming_lines = set(incoming_section.strip().split('\n'))

    # Check if all lines look like imports
    import_patterns = [r'^import ', r'^from .* import']

    head_is_imports = all(
        any(re.match(p, line) for p in import_patterns)
        for line in head_lines if line.strip()
    )

    incoming_is_imports = all(
        any(re.match(p, line) for p in import_patterns)
        for line in incoming_lines if line.strip()
    )

    return head_is_imports and incoming_is_imports

def merge_import_conflicts(content: str) -> str:
    """Merge import conflicts by combining both sets."""
    # Find import conflict sections
    # Merge unique imports
    # Replace conflict markers with merged imports
    # Return updated content
    return content  # Placeholder

def resolve_whitespace_conflicts(content: str) -> str:
    """Resolve whitespace-only conflicts."""
    # Accept incoming for whitespace conflicts
    return content  # Placeholder
```

## Success Criteria
- auto_resolve_conflicts() implemented
- Non-code file handling working
- Code conflict heuristics implemented
- Import merging working
- Whitespace conflict resolution working
- Complex conflicts flagged correctly
- Unit tests passing
- Simulated conflicts resolved
- Integration with branch management working
