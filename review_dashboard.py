#!/usr/bin/env python3
"""
Review Dashboard - Allows user to review and approve solutions before submission
"""

import json
import os
from typing import Dict, List
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReviewDashboard:
    def __init__(self, solutions_file="solutions.json"):
        self.solutions_file = solutions_file
        self.solutions = self._load_solutions()
        self.approvals = {}

    def _load_solutions(self) -> List[Dict]:
        """Load generated solutions"""
        if os.path.exists(self.solutions_file):
            with open(self.solutions_file, "r") as f:
                return json.load(f)
        return []

    def display_solution(self, index: int) -> None:
        """Display a solution for review"""
        if index >= len(self.solutions):
            print("Invalid solution index")
            return

        solution = self.solutions[index]
        
        print(f"\n{'='*60}")
        print(f"SOLUTION {index + 1} of {len(self.solutions)}")
        print(f"{'='*60}\n")
        
        print(f"Title: {solution.get('title')}")
        print(f"Bounty ID: {solution.get('bounty_id')}")
        print(f"Status: {solution.get('status')}\n")
        
        print("ANALYSIS:")
        print("-" * 60)
        analysis = solution.get("analysis", {})
        print(f"Requirements: {', '.join(analysis.get('requirements', []))}")
        print(f"Estimated Effort: {analysis.get('estimated_effort')}")
        print(f"\nApproach:\n{analysis.get('approach', 'N/A')}")
        
        print("\nSOLUTION TEMPLATE:")
        print("-" * 60)
        print(solution.get("solution_template", "N/A"))
        
        print("\nSUBMISSION FORMAT:")
        print("-" * 60)
        submission = solution.get("submission_format", {})
        print(f"Format: {submission.get('format')}")
        print(f"Fields: {', '.join(submission.get('fields', []))}")
        
        print(f"\n{'='*60}\n")

    def review_solution(self, index: int) -> bool:
        """Get user approval for a solution"""
        self.display_solution(index)
        
        while True:
            response = input("Do you approve this solution? (yes/no/skip): ").strip().lower()
            
            if response == "yes":
                self.approvals[index] = {
                    "approved": True,
                    "timestamp": datetime.now().isoformat(),
                    "notes": input("Any notes? (optional): ").strip()
                }
                return True
            elif response == "no":
                self.approvals[index] = {
                    "approved": False,
                    "timestamp": datetime.now().isoformat(),
                    "reason": input("Why not? (optional): ").strip()
                }
                return False
            elif response == "skip":
                return None
            else:
                print("Please enter 'yes', 'no', or 'skip'")

    def review_all(self) -> Dict:
        """Review all solutions"""
        print(f"\nStarting review of {len(self.solutions)} solutions...\n")
        
        for i in range(len(self.solutions)):
            self.review_solution(i)
            print(f"\nProgress: {i + 1}/{len(self.solutions)}\n")
        
        return self._get_approval_summary()

    def _get_approval_summary(self) -> Dict:
        """Get summary of approvals"""
        approved = sum(1 for a in self.approvals.values() if a.get("approved"))
        rejected = sum(1 for a in self.approvals.values() if not a.get("approved"))
        
        return {
            "total_reviewed": len(self.approvals),
            "approved": approved,
            "rejected": rejected,
            "approvals": self.approvals
        }

    def display_dashboard(self) -> None:
        """Display dashboard summary"""
        print(f"\n{'='*60}")
        print("BOUNTY HUNTER DASHBOARD")
        print(f"{'='*60}\n")
        
        print(f"Total Solutions Generated: {len(self.solutions)}")
        print(f"Solutions Reviewed: {len(self.approvals)}")
        
        if self.approvals:
            summary = self._get_approval_summary()
            print(f"Approved: {summary['approved']}")
            print(f"Rejected: {summary['rejected']}")
        
        print(f"\n{'='*60}\n")

    def save_approvals(self, filename="approvals.json"):
        """Save approval decisions"""
        with open(filename, "w") as f:
            json.dump(self.approvals, f, indent=2)
        logger.info(f"Saved approvals to {filename}")

    def export_approved_for_submission(self, filename="ready_to_submit.json"):
        """Export approved solutions ready for submission"""
        approved_solutions = [
            (idx, self.solutions[idx]) 
            for idx in self.approvals 
            if self.approvals[idx].get("approved")
        ]
        
        submission_ready = {
            "total": len(approved_solutions),
            "solutions": [sol for _, sol in approved_solutions],
            "created_at": datetime.now().isoformat()
        }
        
        with open(filename, "w") as f:
            json.dump(submission_ready, f, indent=2)
        
        logger.info(f"Exported {len(approved_solutions)} approved solutions to {filename}")
        return submission_ready


if __name__ == "__main__":
    # Test dashboard
    dashboard = ReviewDashboard()
    
    if dashboard.solutions:
        dashboard.display_dashboard()
        print("\nStarting review process...")
        print("Type 'yes' to approve, 'no' to reject, 'skip' to skip\n")
        
        summary = dashboard.review_all()
        dashboard.save_approvals()
        dashboard.export_approved_for_submission()
        
        print("\nReview Complete!")
        print(f"Approved: {summary['approved']}")
        print(f"Rejected: {summary['rejected']}")
        print(f"\nApproved solutions saved to: ready_to_submit.json")
    else:
        print("No solutions to review. Run bounty_scraper.py and ai_agent.py first.")
