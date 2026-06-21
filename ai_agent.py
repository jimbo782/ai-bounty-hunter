#!/usr/bin/env python3
"""
AI Agent - Generates solutions for bounties using Claude/GPT
"""

import json
import os
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# For local testing - replace with actual API calls
class AIAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4"

    def analyze_bounty(self, bounty: Dict) -> Dict:
        """Analyze bounty requirements"""
        return {
            "title": bounty.get("title"),
            "description": bounty.get("description"),
            "requirements": self._extract_requirements(bounty.get("description", "")),
            "estimated_effort": self._estimate_effort(bounty),
            "approach": self._generate_approach(bounty)
        }

    def _extract_requirements(self, description: str) -> List[str]:
        """Extract key requirements from description"""
        requirements = []
        if "documentation" in description.lower():
            requirements.append("Write comprehensive documentation")
        if "code" in description.lower():
            requirements.append("Analyze or write code")
        if "bug" in description.lower():
            requirements.append("Identify and report bugs")
        if "data" in description.lower():
            requirements.append("Analyze or process data")
        return requirements or ["Complete assigned task"]

    def _estimate_effort(self, bounty: Dict) -> str:
        """Estimate effort level"""
        amount = bounty.get("bounty_amount") or bounty.get("reward", 0)
        if amount < 100:
            return "1-2 hours"
        elif amount < 500:
            return "2-4 hours"
        else:
            return "4-8 hours"

    def _generate_approach(self, bounty: Dict) -> str:
        """Generate solution approach"""
        title = bounty.get("title", "").lower()
        
        if "documentation" in title:
            return """
1. Read existing docs and codebase
2. Identify gaps or unclear sections
3. Write clear, concise documentation
4. Add code examples where relevant
5. Format according to project guidelines
6. Submit pull request
"""
        elif "bug" in title:
            return """
1. Understand bug description
2. Set up development environment
3. Reproduce the bug
4. Identify root cause
5. Propose fix
6. Test solution
7. Submit detailed bug report with PoC
"""
        elif "code" in title:
            return """
1. Understand requirements
2. Design solution
3. Write clean, documented code
4. Test thoroughly
5. Follow project style guidelines
6. Submit for review
"""
        else:
            return """
1. Understand requirements thoroughly
2. Plan approach
3. Execute tasks
4. Document findings
5. Submit results
"""

    def generate_solution(self, bounty: Dict) -> Dict:
        """Generate complete solution for bounty"""
        analysis = self.analyze_bounty(bounty)
        
        solution = {
            "bounty_id": bounty.get("id"),
            "title": bounty.get("title"),
            "analysis": analysis,
            "solution_template": self._create_solution_template(bounty),
            "submission_format": self._format_submission(bounty),
            "status": "ready_for_review"
        }
        
        logger.info(f"Generated solution for: {bounty.get('title')}")
        return solution

    def _create_solution_template(self, bounty: Dict) -> str:
        """Create solution template based on bounty type"""
        return f"""
## Solution for: {bounty.get('title')}

### Summary
[Your summary here]

### Approach
[Detailed approach]

### Implementation
[Code/documentation/analysis here]

### Testing
[How you tested/validated]

### Results
[Key findings/deliverables]

### Notes
[Any additional notes]
"""

    def _format_submission(self, bounty: Dict) -> Dict:
        """Format submission according to platform requirements"""
        platform = bounty.get("platform", "gitcoin")
        
        if platform == "gitcoin":
            return {
                "format": "markdown_or_pr",
                "fields": ["title", "description", "pr_url_or_submission"],
                "template": "See _create_solution_template above"
            }
        elif platform == "issuehunt":
            return {
                "format": "github_issue_comment",
                "fields": ["comment_with_solution", "proof_of_work"],
                "template": "Submit as comment on issue"
            }
        else:
            return {
                "format": "custom",
                "fields": ["submission_body"],
                "template": "Follow platform-specific guidelines"
            }


class SolutionGenerator:
    def __init__(self, agent: AIAgent):
        self.agent = agent

    def generate_batch(self, bounties: List[Dict]) -> List[Dict]:
        """Generate solutions for multiple bounties"""
        solutions = []
        for bounty in bounties:
            try:
                solution = self.agent.generate_solution(bounty)
                solutions.append(solution)
            except Exception as e:
                logger.error(f"Error generating solution for {bounty.get('title')}: {e}")
        
        return solutions

    def save_solutions(self, solutions: List[Dict], filename="solutions.json"):
        """Save generated solutions for review"""
        with open(filename, "w") as f:
            json.dump(solutions, f, indent=2)
        logger.info(f"Saved {len(solutions)} solutions to {filename}")


if __name__ == "__main__":
    agent = AIAgent()
    
    # Test with sample bounty
    sample_bounty = {
        "id": "test-001",
        "title": "Write API Documentation",
        "description": "Create comprehensive documentation for the REST API",
        "bounty_amount": 150,
        "platform": "gitcoin"
    }
    
    solution = agent.generate_solution(sample_bounty)
    print(json.dumps(solution, indent=2))
