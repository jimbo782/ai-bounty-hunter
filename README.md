# 🤖 AI Bounty Hunter

Automated bounty hunting system for beginners. Find, solve, and submit bounties at scale with AI-powered solution generation.

## Features

✅ **Bounty Discovery** - Monitors Gitcoin, IssueHunt, OpenBounty  
✅ **AI Solution Generation** - Auto-generates solutions for beginner tasks  
✅ **Smart Filtering** - Only shows bounties matching your skill level  
✅ **Review Dashboard** - You approve before submission  
✅ **Auto-Formatter** - Formats submissions for each platform  
✅ **Payment Tracking** - Tracks earnings and payment status  

## How It Works

```
1. SCRAPE: Find beginner bounties across platforms
   ↓
2. ANALYZE: AI analyzes requirements and generates solutions
   ↓
3. REVIEW: You review and approve each solution
   ↓
4. FORMAT: System formats for platform submission
   ↓
5. SUBMIT: You copy-paste to bounty platform
   ↓
6. EARN: Track payments and earnings
```

## Installation

```bash
# Clone the repo
git clone https://github.com/jimbo782/ai-bounty-hunter.git
cd ai-bounty-hunter

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Quick Start

### Full Cycle (Recommended)

```bash
python main.py
# Select option 1: Full cycle
# Follow the prompts
```

This will:
1. Scrape all available beginner bounties
2. Generate AI solutions for each
3. Ask you to review and approve
4. Format submissions automatically
5. Display ready-to-submit content

### Individual Steps

```bash
# Just scrape bounties
python main.py  # Select 2

# Generate solutions
python main.py  # Select 3

# Review solutions
python main.py  # Select 4

# Display formatted submissions
python main.py  # Select 5

# Check earnings
python main.py  # Select 6
```

## Workflow

### Step 1: Find Bounties
The scraper looks for open bounties on:
- **Gitcoin** - Open source, documentation, data tasks
- **IssueHunt** - GitHub issues with bounties
- **OpenBounty** - General purpose bounties

Filters:
- Experience level: Beginner
- Minimum amount: $50
- Status: Open
- Categories: Documentation, bugs, code analysis, data, content

### Step 2: Generate Solutions
AI agent analyzes each bounty and generates:
- Task breakdown
- Approach/methodology
- Solution template
- Effort estimate
- Platform-specific formatting

### Step 3: Review Solutions
You review each generated solution:
- Read the analysis
- Review the approach
- Check the solution template
- Approve or reject

**⚠️ Important:** Review carefully! Your reputation depends on solution quality.

### Step 4: Submit
Copy the formatted submission and post to the platform:
- Gitcoin: Submit via PR or platform form
- IssueHunt: Post as GitHub issue comment
- Others: Follow platform guidelines

### Step 5: Track Earnings
Monitor submission status and payments:
```bash
python main.py  # Select 6 for earnings summary
```

## File Structure

```
bounties.json              # Raw bounties from platforms
solutions.json            # AI-generated solutions
approvals.json           # Your approval decisions
ready_to_submit.json     # Approved solutions ready to post
submission_log.json      # Formatted submissions
payment_tracker.json     # Payment status and earnings
config.json             # Platform configuration
```

## Configuration

Edit `config.json` to customize:

```json
{
  "min_bounty_amount": 50,
  "bounty_types": ["documentation", "bug_report", "code_analysis"],
  "platforms": {
    "gitcoin": { "enabled": true },
    "issuehunt": { "enabled": true }
  }
}
```

## API Keys & Setup

### OpenAI API (Required)

```bash
export OPENAI_API_KEY=sk-your-key-here
```

Get your key: https://platform.openai.com/account/api-keys

### GitHub Token (Optional)

```bash
export GITHUB_TOKEN=ghp_your-token-here
```

For auto-submitting to GitHub issues/PRs.

## Tips for Success

1. **Start with documentation bounties** - Easier for beginners
2. **Review solutions carefully** - Your reputation is important
3. **Follow platform guidelines** - Each platform has specific requirements
4. **Submit regularly** - More submissions = more earnings
5. **Track your time** - Know your hourly rate
6. **Update your skills** - Gradually take harder bounties

## Earnings Potential

| Bounty Type | Difficulty | Amount | Time | $/Hour |
|-------------|-----------|--------|------|--------|
| Documentation | Easy | $50-150 | 1-2 hrs | $25-150 |
| Bug Report | Medium | $100-500 | 2-4 hrs | $25-250 |
| Code Analysis | Medium | $150-300 | 2-3 hrs | $50-150 |
| Smart Contract Audit | Hard | $500-5000 | 4-8 hrs | $62-1250 |

## Troubleshooting

### "No bounties found"
- Check your internet connection
- Verify minimum bounty amount in config.json
- Try a different platform

### "API rate limit exceeded"
- Wait a few minutes before running again
- Upgrade your OpenAI plan for higher limits

### "Solution quality is poor"
- The AI needs better requirements. Check the bounty description.
- Consider rejecting and trying a different bounty
- Update the solution manually before submitting

## Ethical Guidelines

✅ **DO:**
- Review every solution before submitting
- Verify solutions actually solve the problem
- Disclose AI assistance if asked
- Maintain high quality standards
- Respect platform rules

❌ **DON'T:**
- Submit low-quality AI outputs
- Claim AI work as your own without disclosure
- Spam or auto-submit without review
- Violate platform terms of service
- Target scam/fake bounties

## Support

For issues or questions:
1. Check existing issues on GitHub
2. Review troubleshooting section above
3. Check platform-specific docs (Gitcoin, IssueHunt)

## Roadmap

- [ ] Multi-platform support (Codementor, Toptal, etc.)
- [ ] Smart contract auditing
- [ ] Real-time bounty notifications
- [ ] Submission history and analytics
- [ ] Revenue tracking and reports
- [ ] API for custom integrations

## License

MIT License - See LICENSE file

## Disclaimer

This tool is designed for legitimate bounty hunting. Users are responsible for:
- Following all platform terms of service
- Submitting honest, quality work
- Respecting intellectual property rights
- Maintaining ethical standards

The creators are not responsible for misuse or violations of platform ToS.

---

**Made with ❤️ by jimbo782**

Start earning with AI today! 🚀
