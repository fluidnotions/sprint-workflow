"""State schema definitions for LangGraph sprint workflow.

This module defines all TypedDict schemas that represent the state
flowing through the LangGraph state machine.
"""

from typing import TypedDict, List, Optional, Literal, Dict, Any


class JobSpec(TypedDict, total=False):
    """Specification for a single job in the sprint.

    A job is a code-colocated grouping of todos that modify the same
    codebase areas, minimizing merge conflicts during parallel development.
    """

    # Identity
    name: str
    """Unique job identifier (e.g., 'auth-system', 'api-endpoints')"""

    task_file: str
    """Path to the task specification file"""

    # Git & Worktree
    worktree: str
    """Path to the git worktree for this job"""

    repo_root: str
    """Git repository root directory"""

    branch: str
    """Git branch name for this job"""

    # Todos & Planning
    todos: List[str]
    """List of todo items from the sprint plan"""

    story_points: int
    """Complexity estimate in story points"""

    # Execution State
    status: Literal["pending", "implementing", "verifying", "verified", "failed"]
    """Current execution status"""

    retry_count: int
    """Number of verification retry attempts"""

    error_message: Optional[str]
    """Error message if job failed"""

    # Implementation Details
    files_to_modify: List[str]
    """List of files this job will create/modify"""

    dependencies: List[str]
    """Other jobs this depends on"""


class RepoInfo(TypedDict):
    """Information about a git repository.

    Tracks repository configuration for multi-repo sprint scenarios.
    """

    path: str
    """Absolute path to repository root"""

    has_remote: bool
    """Whether repository has a remote origin configured"""

    branches: List[str]
    """List of branch names in this repository"""

    default_branch: str
    """Default branch name (e.g., 'main', 'master')"""


class ErrorRecord(TypedDict):
    """Record of an error that occurred during sprint execution."""

    job: str
    """Job name where error occurred"""

    phase: str
    """Workflow phase where error occurred"""

    error: str
    """Error message"""

    timestamp: str
    """ISO timestamp of error"""

    report_path: Optional[str]
    """Path to detailed error report file"""


class SprintWorkflowState(TypedDict, total=False):
    """Complete state for the LangGraph sprint workflow.

    This state flows through all nodes in the workflow graph, accumulating
    data at each phase until the sprint is complete.

    The workflow phases are:
    1. init - Initialize sprint with theme and features
    2. planning - Parallel PM/UX/Engineering planning
    3. gap_analysis - Architecture validation with feedback loops
    4. prd_generation - Generate Sprint PRD
    5. job_creation - Analyze code co-location and create jobs
    6. job_validation - Validate job specifications
    7. worktree_setup - Create git worktrees
    8. implementation - Parallel job execution
    9. verification - Test and quality checks with retry loops
    10. branch_mgmt - Update branches, resolve conflicts
    11. merging - Create PRs and auto-merge
    12. complete - Sprint finished
    """

    # ========================================================================
    # INPUT - User-provided sprint configuration
    # ========================================================================

    sprint_theme: str
    """High-level theme for the sprint (e.g., 'LangGraph Migration')"""

    project_name: str
    """Project name (usually basename of working directory)"""

    features: List[str]
    """List of features to implement in this sprint"""

    pool_size: int
    """Number of parallel agents/workers (default: 3)"""

    # ========================================================================
    # PHASE TRACKING
    # ========================================================================

    phase: Literal[
        "init",
        "planning",
        "gap_analysis",
        "prd_generation",
        "job_creation",
        "job_validation",
        "worktree_setup",
        "implementation",
        "verification",
        "branch_mgmt",
        "merging",
        "complete",
        "error"
    ]
    """Current workflow phase"""

    # ========================================================================
    # PLANNING PHASE OUTPUTS
    # ========================================================================

    pm_output: Optional[Dict[str, Any]]
    """Product Manager output: user stories, acceptance criteria, priorities"""

    ux_output: Optional[Dict[str, Any]]
    """UX Designer output: user flows, UI components, accessibility"""

    engineering_output: Optional[Dict[str, Any]]
    """Senior Engineer output: technical architecture, risks, approach"""

    synthesis_output: Optional[Dict[str, Any]]
    """Synthesized planning from PM + UX + Engineering"""

    # ========================================================================
    # GAP ANALYSIS & VALIDATION
    # ========================================================================

    gap_analysis: Optional[Dict[str, Any]]
    """Gap analysis results: issues found, recommendations"""

    retry_counts: Dict[str, int]
    """Retry counters for feedback loops (gap_analysis, job_validation, etc.)"""

    # ========================================================================
    # SPRINT ARTIFACTS
    # ========================================================================

    sprint_prd_path: Optional[str]
    """Path to generated Sprint PRD document"""

    todos_path: Optional[str]
    """Path to generated todos file"""

    # ========================================================================
    # JOB SPECIFICATIONS
    # ========================================================================

    jobs: List[JobSpec]
    """List of all jobs in the sprint"""

    jobs_implementing: List[str]
    """Job names currently being implemented"""

    jobs_verifying: List[str]
    """Job names currently being verified"""

    jobs_verified: List[str]
    """Job names that have been verified"""

    jobs_failed: List[str]
    """Job names that failed verification"""

    # ========================================================================
    # REPOSITORY & GIT
    # ========================================================================

    repos: List[RepoInfo]
    """List of git repositories involved in the sprint"""

    worktrees: List[Dict[str, str]]
    """List of created worktrees with paths and branches"""

    branch_status: List[Dict[str, Any]]
    """Status of branch updates and conflict resolution"""

    merge_status: List[Dict[str, Any]]
    """Status of PR creation and merging"""

    # ========================================================================
    # ERROR HANDLING & TRACKING
    # ========================================================================

    errors: List[ErrorRecord]
    """List of all errors encountered during sprint"""

    # ========================================================================
    # METADATA
    # ========================================================================

    started_at: str
    """ISO timestamp when sprint started"""

    completed_at: Optional[str]
    """ISO timestamp when sprint completed"""

    checkpoints: List[str]
    """List of checkpoint names for resumability"""

    status_messages: List[str]
    """Log messages for user visibility"""


# Type aliases for convenience
WorkflowPhase = Literal[
    "init",
    "planning",
    "gap_analysis",
    "prd_generation",
    "job_creation",
    "job_validation",
    "worktree_setup",
    "implementation",
    "verification",
    "branch_mgmt",
    "merging",
    "complete",
    "error"
]

JobStatus = Literal["pending", "implementing", "verifying", "verified", "failed"]
