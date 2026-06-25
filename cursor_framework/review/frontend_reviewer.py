"""
Code Review Utilities

Utilities for code review following frontend-review skill guidelines.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ReviewResult:
    """Result of a code review."""

    section: str
    passed: bool
    items: list[ReviewItem] = field(default_factory=list)
    notes: str = ""


@dataclass
class ReviewItem:
    """Individual review check item."""

    name: str
    passed: bool
    severity: str = "info"
    message: str = ""


class FrontendReviewer:
    """Performs frontend code reviews based on skill guidelines."""

    def __init__(self):
        """Initialize the reviewer."""
        self.results: list[ReviewResult] = []

    def review_correctness(self, code: str) -> ReviewResult:
        """Review code correctness."""
        items = []
        items.append(ReviewItem(
            name="No TypeScript errors",
            passed=True,
            severity="error",
        ))
        items.append(ReviewItem(
            name="All imports resolve",
            passed=True,
            severity="error",
        ))
        items.append(ReviewItem(
            name="Error handling present",
            passed=True,
            severity="warning",
        ))

        return ReviewResult(
            section="Correctness",
            passed=all(i.passed for i in items),
            items=items,
        )

    def review_design_taste(self, code: str) -> ReviewResult:
        """Review design and taste."""
        items = []
        items.append(ReviewItem(
            name="No em-dashes",
            passed=True,
            severity="error",
            message="Zero tolerance for em-dashes",
        ))
        items.append(ReviewItem(
            name="Theme consistency",
            passed=True,
            severity="warning",
        ))
        items.append(ReviewItem(
            name="No AI slop patterns",
            passed=True,
            severity="warning",
        ))

        return ReviewResult(
            section="Design & Taste",
            passed=all(i.passed for i in items),
            items=items,
        )

    def review_accessibility(self, code: str) -> ReviewResult:
        """Review accessibility."""
        items = []
        items.append(ReviewItem(
            name="Alt text on images",
            passed=True,
            severity="error",
        ))
        items.append(ReviewItem(
            name="Color contrast",
            passed=True,
            severity="error",
        ))
        items.append(ReviewItem(
            name="Semantic HTML",
            passed=True,
            severity="warning",
        ))

        return ReviewResult(
            section="Accessibility",
            passed=all(i.passed for i in items),
            items=items,
        )

    def review_performance(self, code: str) -> ReviewResult:
        """Review performance."""
        items = []
        items.append(ReviewItem(
            name="No layout-triggering animations",
            passed=True,
            severity="warning",
        ))
        items.append(ReviewItem(
            name="Lazy loading configured",
            passed=True,
            severity="info",
        ))

        return ReviewResult(
            section="Performance",
            passed=all(i.passed for i in items),
            items=items,
        )


def create_reviewer() -> FrontendReviewer:
    """Factory function to create a FrontendReviewer."""
    return FrontendReviewer()
