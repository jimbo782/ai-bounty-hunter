#!/usr/bin/env python3
"""
Bounty Scraper - Monitors Gitcoin, IssueHunt for beginner-friendly bounties
"""

import requests
import json
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BountyScraper:
    def __init__(self, config_path="config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.bounties = []

    def scrape_gitcoin(self) -> List[Dict]:
        """Fetch beginner bounties from Gitcoin"""
        try:
            url = self.config["platforms"]["gitcoin"]["url"]
            params = {
                "experience_level": "beginner",
                "status": "open",
                "ordering": "-bounty_amount"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            bounties = response.json()
            filtered = [
                b for b in bounties 
                if b.get("bounty_amount", 0) >= self.config["min_bounty_amount"]
            ]
            
            logger.info(f"Found {len(filtered)} Gitcoin bounties")
            return filtered
            
        except Exception as e:
            logger.error(f"Error scraping Gitcoin: {e}")
            return []

    def scrape_issuehunt(self) -> List[Dict]:
        """Fetch beginner bounties from IssueHunt"""
        try:
            url = self.config["platforms"]["issuehunt"]["url"]
            params = {
                "difficulty": "easy",
                "status": "open",
                "sort": "-reward"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            bounties = response.json()
            filtered = [
                b for b in bounties 
                if b.get("reward", 0) >= self.config["min_bounty_amount"]
            ]
            
            logger.info(f"Found {len(filtered)} IssueHunt bounties")
            return filtered
            
        except Exception as e:
            logger.error(f"Error scraping IssueHunt: {e}")
            return []

    def filter_by_type(self, bounties: List[Dict]) -> List[Dict]:
        """Filter bounties by accepted types"""
        filtered = []
        for bounty in bounties:
            bounty_type = bounty.get("category", "").lower()
            if any(t in bounty_type for t in self.config["bounty_types"]):
                filtered.append(bounty)
        return filtered

    def scrape_all(self) -> List[Dict]:
        """Scrape all enabled platforms"""
        self.bounties = []
        
        if self.config["platforms"]["gitcoin"]["enabled"]:
            self.bounties.extend(self.scrape_gitcoin())
        
        if self.config["platforms"]["issuehunt"]["enabled"]:
            self.bounties.extend(self.scrape_issuehunt())
        
        self.bounties = self.filter_by_type(self.bounties)
        logger.info(f"Total bounties after filtering: {len(self.bounties)}")
        
        return self.bounties

    def save_bounties(self, filename="bounties.json"):
        """Save bounties to file for processing"""
        with open(filename, "w") as f:
            json.dump(self.bounties, f, indent=2)
        logger.info(f"Saved {len(self.bounties)} bounties to {filename}")


if __name__ == "__main__":
    scraper = BountyScraper()
    bounties = scraper.scrape_all()
    scraper.save_bounties()
    
    # Display summary
    print(f"\n{'='*50}")
    print(f"Found {len(bounties)} beginner bounties")
    print(f"{'='*50}\n")
    
    for bounty in bounties[:5]:  # Show first 5
        print(f"Title: {bounty.get('title', 'N/A')}")
        print(f"Amount: ${bounty.get('bounty_amount') or bounty.get('reward', 'N/A')}")
        print(f"URL: {bounty.get('url', 'N/A')}")
        print("-" * 50)
