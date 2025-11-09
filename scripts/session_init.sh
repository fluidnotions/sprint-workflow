#!/bin/bash

# Claude Code Session Initialization Hook
# Creates directories and reports status

# Use PWD as fallback when CLAUDE_PROJECT_DIR not set
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"

# Get project name from directory
PROJECT_NAME=$(basename "$PROJECT_DIR")

STATUS_LINES=()

# Create tasks directory if it doesn't exist
if [ ! -d "$PROJECT_DIR/tasks" ]; then
    mkdir -p "$PROJECT_DIR/tasks" 2>/dev/null
    STATUS_LINES+=("Created tasks directory")
fi

# Create worktrees directory if it doesn't exist
if [ ! -d "$PROJECT_DIR/worktrees" ]; then
    mkdir -p "$PROJECT_DIR/worktrees" 2>/dev/null
    STATUS_LINES+=("Created worktrees directory")
fi

# Create sprint-plans directory with project subdirectory in thoughts if thoughts exists
if [ -L "$PROJECT_DIR/thoughts" ] || [ -d "$PROJECT_DIR/thoughts" ]; then
    if [ ! -d "$PROJECT_DIR/thoughts/sprint-plans/$PROJECT_NAME" ]; then
        mkdir -p "$PROJECT_DIR/thoughts/sprint-plans/$PROJECT_NAME" 2>/dev/null
        STATUS_LINES+=("Created sprint-plans/$PROJECT_NAME directory")
    fi
fi

# Check for active sprint
if ls $PROJECT_DIR/*_todos.md 1> /dev/null 2>&1; then
    LATEST_TODO=$(ls -t $PROJECT_DIR/*_todos.md | head -1)
    STATUS_LINES+=("Active sprint: $(basename $LATEST_TODO)")
fi

# Check for active worktrees
if command -v git &> /dev/null && [ -d "$PROJECT_DIR/.git" ]; then
    WORKTREE_COUNT=$(git worktree list 2>/dev/null | grep -c "$PROJECT_DIR/worktrees" || echo "0")
    if [ $WORKTREE_COUNT -gt 0 ]; then
        STATUS_LINES+=("Active worktrees: $WORKTREE_COUNT")
    fi
fi

# Build status message
if [ ${#STATUS_LINES[@]} -eq 0 ]; then
    STATUS_MESSAGE="Sprint workflow environment ready"
else
    STATUS_MESSAGE=$(printf '%s; ' "${STATUS_LINES[@]}")
    STATUS_MESSAGE="${STATUS_MESSAGE%; }"
fi

# Output proper JSON format for SessionStart hook
cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "message": "$STATUS_MESSAGE"
  }
}
EOF

exit 0
