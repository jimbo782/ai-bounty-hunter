#!/usr/bin/env python3
"""
Auto Submitter - Submits approved solutions to bounty platforms
"""

import json
import os
import requests
from typing import Dict, List
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoSubmitter:
    def __init__(self, approved_file="ready_to_submit.json"):
        self.approved_file = approved_file
        self.approved_solutions = self._load_approved()
        self.submission_logs = []

    def _load_approved(self) -> List[Dict]:
        """Load approved solutions"""
        if os.path.exists(self.approved_file):
            with open(self.approved_file, "r") as f:
                data = json.load(f)
                return data.get("solutions", [])
        return []

    def submit_to_gitcoin(self, solution: Dict) -> Dict:
        """Submit solution to Gitcoin"""
        try:
            # Note: Gitcoin submissions typically require:
            # - Manual submission via PR or platform form
            # - This serves as a template/formatter
            
            submission = {
                "bounty_id": solution.get("bounty_id"),
                "platform": "gitcoin",
                "title": solution.get("title"),
                "submission_body": solution.get("solution_template"),
                "submission_format": solution.get("submission_format"),
                "timestamp": datetime.now().isoformat(),
                "status": "ready_for_manual_submission"
            }
            
            logger.info(f"Formatted submission for Gitcoin: {solution.get('title')}")
            return submission
            
        except Exception as e:
            logger.error(f"Error submitting to Gitcoin: {e}")
            return {"status": "error", "error": str(e)}

    def submit_to_issuehunt(self, solution: Dict) -> Dict:
        """Submit solution to IssueHunt"""
        try:
            # IssueHunt submissions are typically via GitHub issue comments
            # This prepares the submission
            
            submission = {
                "bounty_id": solution.get("bounty_id"),
                "platform": "issuehunt",
                "title": solution.get("title"),
                "comment_body": f"## Solution\n\n{solution.get('solution_template')}",
                "submission_format": solution.get("submission_format"),
                "timestamp": datetime.now().isoformat(),
                "status": "ready_for_manual_submission"
            }
            
            logger.info(f"Formatted submission for IssueHunt: {solution.get('title')}")
            return submission
            
        except Exception as e:
            logger.error(f"Error submitting to IssueHunt: {e}")
            return {"status": "error", "error": str(e)}

    def format_submission(self, solution: Dict) -> Dict:
        """Format submission based on platform"""
        # This would detect the platform and call appropriate method
        # For now, returns formatted submission ready for manual posting
        
        return {
            "bounty_id": solution.get("bounty_id"),
            "title": solution.get("title"),
            "submission_body": solution.get("solution_template"),
            "submission_format": solution.get("submission_format"),
            "status": "formatted_ready_to_post",
            "formatted_at": datetime.now().isoformat(),
            "next_step": "Copy submission_body and post to platform"
        }

    def submit_all(self) -> List[Dict]:
        """Submit all approved solutions"""
        submissions = []
        
        for solution in self.approved_solutions:
            submission = self.format_submission(solution)
            submissions.append(submission)
            self.submission_logs.append(submission)
        
        logger.info(f"Formatted {len(submissions)} submissions")
        return submissions

    def save_submission_log(self, filename="submission_log.json"):
        """Save submission log"""
        log = {
            "total_submitted": len(self.submission_logs),
            "submissions": self.submission_logs,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filename, "w") as f:
            json.dump(log, f, indent=2)
        
        logger.info(f"Saved submission log to {filename}")
        return log

    def display_submission(self, submission: Dict) -> None:
        """Display formatted submission"""
        print(f"\n{'='*60}")
        print(f"SUBMISSION: {submission.get('title')}")
        print(f"{'='*60}\n")
        
        print(f"Bounty ID: {submission.get('bounty_id')}")
        print(f"Platform: {submission.get('submission_format', {}).get('format')}")
        print(f"Status: {submission.get('status')}\n")
        
        print("SUBMISSION BODY:")
        print("-" * 60)
        print(submission.get("submission_body", "N/A"))
        print("-" * 60)
        
        print(f"\nNEXT STEPS:")
        print(f"1. Copy the submission body above")
        print(f"2. Go to bounty platform")
        print(f"3. Paste into submission form/comment")
        print(f"4. Review and submit")
        print(f"\n{'='*60}\n")

    def display_all_submissions(self) -> None:
        """Display all formatted submissions"""
        submissions = self.submit_all()
        
        for i, submission in enumerate(submissions):
            self.display_submission(submission)
            print(f"\nSubmission {i + 1}/{len(submissions)}\n")


class PaymentTracker:
    def __init__(self, tracker_file="payment_tracker.json"):
        self.tracker_file = tracker_file
        self.payments = self._load_payments()

    def _load_payments(self) -> List[Dict]:
        """Load payment records"""
        if os.path.exists(self.tracker_file):
            with open(self.tracker_file, "r") as f:
                return json.load(f)
        return []

    def log_submission(self, bounty_id: str, title: str, amount: float, platform: str):
        """Log a submission"""
        payment = {
            "bounty_id": bounty_id,
            "title": title,
            "amount": amount,
            "platform": platform,
            "status": "submitted",
            "submitted_at": datetime.now().isoformat()
        }
        self.payments.append(payment)
        self.save()

    def update_payment(self, bounty_id: str, status: str):
        """Update payment status (approved, paid, rejected)"""
        for payment in self.payments:
            if payment["bounty_id"] == bounty_id:
                payment["status"] = status
                payment["updated_at"] = datetime.now().isoformat()
                self.save()
                break

    def get_earnings(self) -> Dict:
        """Get total earnings"""
        total = sum(p["amount"] for p in self.payments if p["status"] == "paid")
        pending = sum(p["amount"] for p in self.payments if p["status"] == "submitted")
        approved = sum(p["amount"] for p in self.payments if p["status"] == "approved")
        
        return {
            "total_paid": total,
            "pending": pending,
            "approved": approved,
            "total_potential": total + pending + approved
        }

    def save(self):
        """Save payment records"""
        with open(self.tracker_file, "w") as f:
            json.dump(self.payments, f, indent=2)

    def display_earnings(self):
        """Display earnings summary"""
        earnings = self.get_earnings()
        
        print(f"\n{'='*60}")
        print("EARNINGS SUMMARY")
        print(f"{'='*60}\n")
        
        print(f"Total Paid: ${earnings['total_paid']:.2f}")
        print(f"Approved (awaiting payment): ${earnings['approved']:.2f}")
        print(f"Pending Review: ${earnings['pending']:.2f}")
        print(f"Total Potential: ${earnings['total_potential']:.2f}\n")
        
        print("Recent Submissions:")
        print("-" * 60)
        for payment in self.payments[-5:]:  # Last 5
            print(f"{payment['title']}")
            print(f"  Amount: ${payment['amount']:.2f} | Status: {payment['status']}")
        
        print(f"\n{'='*60}\n")


if __name__ == "__main__":
    submitter = AutoSubmitter()
    submitter.display_all_submissions()
    submitter.save_submission_log()
    
    # Test payment tracker
    tracker = PaymentTracker()
    tracker.display_earnings()
