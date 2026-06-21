#!/usr/bin/env python3
"""
AI Bounty Hunter - Main Orchestrator
Coordinates bounty scraping, solution generation, review, and submission
"""

import sys
import json
from datetime import datetime
import logging

from bounty_scraper import BountyScraper
from ai_agent import AIAgent, SolutionGenerator
from review_dashboard import ReviewDashboard
from auto_submitter import AutoSubmitter, PaymentTracker

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BountyHunterOrchestrator:
    def __init__(self):
        self.scraper = BountyScraper()
        self.agent = AIAgent()
        self.solution_gen = SolutionGenerator(self.agent)
        self.dashboard = None
        self.submitter = None
        self.tracker = PaymentTracker()

    def run_full_cycle(self):
        """Run complete bounty hunting cycle"""
        print("\n" + "="*60)
        print("🤖 AI BOUNTY HUNTER - FULL CYCLE")
        print("="*60 + "\n")

        # Step 1: Scrape bounties
        print("📡 STEP 1: Scraping bounties from platforms...")
        bounties = self.scraper.scrape_all()
        self.scraper.save_bounties()
        print(f"✅ Found {len(bounties)} bounties\n")

        if not bounties:
            print("❌ No bounties found. Exiting.")
            return

        # Step 2: Generate solutions
        print("🤔 STEP 2: Generating solutions with AI...")
        solutions = self.solution_gen.generate_batch(bounties)
        self.solution_gen.save_solutions(solutions)
        print(f"✅ Generated {len(solutions)} solutions\n")

        # Step 3: Review solutions
        print("👁️  STEP 3: Review solutions")
        self.dashboard = ReviewDashboard()
        print(f"ℹ️  You have {len(self.dashboard.solutions)} solutions to review")
        print("💡 Type 'yes' to approve, 'no' to reject, 'skip' to skip\n")

        review_summary = self.dashboard.review_all()
        self.dashboard.save_approvals()
        
        approved = review_summary.get('approved', 0)
        print(f"\n✅ Review complete! {approved} solutions approved\n")

        # Step 4: Prepare submissions
        print("📋 STEP 4: Preparing submissions...")
        self.dashboard.export_approved_for_submission()
        self.submitter = AutoSubmitter()
        
        if not self.submitter.approved_solutions:
            print("❌ No approved solutions to submit.")
            return

        print(f"✅ {len(self.submitter.approved_solutions)} solutions ready for submission\n")

        # Step 5: Display submissions
        print("📤 STEP 5: Display submissions for posting")
        self.submitter.display_all_submissions()
        self.submitter.save_submission_log()

        # Step 6: Show summary
        print("📊 STEP 6: Summary")
        self.display_summary()

    def display_summary(self):
        """Display cycle summary"""
        print("\n" + "="*60)
        print("CYCLE SUMMARY")
        print("="*60 + "\n")

        print("✅ Completed Steps:")
        print("  1. ✓ Scraped bounties from platforms")
        print("  2. ✓ Generated AI solutions")
        print("  3. ✓ You reviewed and approved solutions")
        print("  4. ✓ Formatted for submission")
        print("  5. ✓ Generated submission instructions\n")

        print("🚀 NEXT STEPS:")
        print("  1. Review the displayed submissions above")
        print("  2. Copy each submission_body")
        print("  3. Go to bounty platform (Gitcoin, IssueHunt, etc.)")
        print("  4. Paste into submission form/comment")
        print("  5. Click submit")
        print("  6. Track payment status in payment_tracker.json\n")

        print("📊 Files Generated:")
        print("  - bounties.json: All scraped bounties")
        print("  - solutions.json: AI-generated solutions")
        print("  - approvals.json: Your approval decisions")
        print("  - ready_to_submit.json: Approved solutions")
        print("  - submission_log.json: Formatted submissions")
        print("  - payment_tracker.json: Payment tracking\n")

    def run_scraper_only(self):
        """Just scrape bounties"""
        print("\n📡 Scraping bounties...")
        bounties = self.scraper.scrape_all()
        self.scraper.save_bounties()
        print(f"✅ Found {len(bounties)} bounties")
        print("💾 Saved to bounties.json")

    def run_generation_only(self):
        """Just generate solutions for existing bounties"""
        print("\n🤔 Generating solutions...")
        
        try:
            with open("bounties.json", "r") as f:
                bounties = json.load(f)
        except FileNotFoundError:
            print("❌ bounties.json not found. Run scraper first.")
            return

        solutions = self.solution_gen.generate_batch(bounties)
        self.solution_gen.save_solutions(solutions)
        print(f"✅ Generated {len(solutions)} solutions")
        print("💾 Saved to solutions.json")

    def run_review_only(self):
        """Just review existing solutions"""
        print("\n👁️  Opening review dashboard...")
        
        self.dashboard = ReviewDashboard()
        if not self.dashboard.solutions:
            print("❌ solutions.json not found. Generate solutions first.")
            return

        review_summary = self.dashboard.review_all()
        self.dashboard.save_approvals()
        self.dashboard.export_approved_for_submission()
        
        print(f"\n✅ Approved: {review_summary['approved']}")
        print("💾 Saved to approvals.json and ready_to_submit.json")

    def run_submission_display(self):
        """Display formatted submissions"""
        print("\n📤 Displaying submissions...")
        
        self.submitter = AutoSubmitter()
        if not self.submitter.approved_solutions:
            print("❌ No approved solutions found. Review solutions first.")
            return

        self.submitter.display_all_submissions()
        self.submitter.save_submission_log()


def main():
    """Main entry point"""
    orchestrator = BountyHunterOrchestrator()

    print("\n🎯 AI BOUNTY HUNTER - Choose mode:\n")
    print("1. Full cycle (scrape → generate → review → display)")
    print("2. Scrape only")
    print("3. Generate solutions only")
    print("4. Review solutions only")
    print("5. Display submissions only")
    print("6. Show earnings")
    print("0. Exit\n")

    choice = input("Select (0-6): ").strip()

    if choice == "1":
        orchestrator.run_full_cycle()
    elif choice == "2":
        orchestrator.run_scraper_only()
    elif choice == "3":
        orchestrator.run_generation_only()
    elif choice == "4":
        orchestrator.run_review_only()
    elif choice == "5":
        orchestrator.run_submission_display()
    elif choice == "6":
        orchestrator.tracker.display_earnings()
    elif choice == "0":
        print("Goodbye!")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
