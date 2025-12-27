#!/usr/local/bin/python3
"""
Script to convert markdown CV to JSON format
Author: Yuan Chen
"""

import os
import re
import json
import yaml
import argparse
from datetime import datetime, date
import glob
import pandas as pd


def main():
    """Main function to parse arguments and run the conversion."""
    parser = argparse.ArgumentParser(description='Convert markdown CV to JSON format')
    parser.add_argument('--output', '-o', required=True, help='Output JSON file')
    parser.add_argument('--config', '-c', help='Jekyll _config.yml file')

    args = parser.parse_args()
    # print(f'args:\n{args}')
    # Get repository root (parent directory of the input file's directory)
    repo_root = os.getcwd()
    # print(f'repo_root: {repo_root}')
    create_cv_json(args.config, repo_root, args.output)


def create_cv_json(config_file, repo_root, output_file):
    """Create a JSON CV from markdown and other repository data."""

    # Parse config file
    config = parse_config(config_file)  # just loads config.yml as json in memory

    # Extract author information
    author_info = extract_author_info(config)  # collects random assortment of info...

    # Create the JSON structure
    cv_json = {
        "basics": author_info,
        "work": parse_work_experience('_data/work_exp.json'),
        "skills": parse_skills('_data/skills.json'),
        "education": parse_education('_data/education.json'),
        "languages": [],
        "interests": [],
        "references": []
    }

    # Add projects
    cv_json["projects"] = parse_projects(os.path.join(repo_root, "_projects"))

    # Add portfolio
    # cv_json["portfolio"] = parse_portfolio(os.path.join(repo_root, "_portfolio"))

    # Extract languages and interests from config if available
    if 'languages' in config:
        cv_json["languages"] = config.get('languages', [])

    if 'interests' in config:
        cv_json["interests"] = config.get('interests', [])

    # Write the JSON to a file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(cv_json, file, indent=2, cls=DateTimeEncoder)

    print(f"Successfully generated {output_file}")


def parse_config(config_file):
    """Parse the Jekyll _config.yml file for additional information."""
    if not os.path.exists(config_file):
        return {}

    with open(config_file, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config


def extract_author_info(config):
    """Extract author information from the config file."""
    author_info = {
        "name": config.get('name', ''),
        "email": "",
        "phone": "(816) 721-4245",
        "website": config.get('url', ''),
        "summary": "",
        "location": {
            "address": "",
            "postalCode": "",
            "city": ""
        },
        "profiles": []
    }

    # Extract author details if available
    if 'author' in config:
        author = config.get('author', {})

        # Override name if author name is available
        if author.get('name'):
            author_info['name'] = author.get('name')

        # Add email
        if author.get('email'):
            author_info['email'] = author.get('email')

        # Add location
        if author.get('location'):
            author_info['location']['city'] = author.get('location', '')

        # Add employer as part of summary
        if author.get('employer') != 'Seeking Employment':
            author_info['summary'] = f"Currently employed at {author.get('employer')}"
        else:
            author_info['summary'] = f"Currently seeking employment"

        # Use actual CV summary instead of website author summary...
        author_info[
            'summary'] = 'Goal-oriented software engineering professional with 4+ years of progressive experience supporting federal research and development projects for various Sponsor Agencies with The MITRE Corporation. Prior to MITRE, I developed and supported EHR systems with Oracle. Driven by a natural affinity for programmatic problem-solving, I am seeking to contribute to impactful projects and initiatives. Kansas City-based developer proficient in health data interoperability, steering complex technical conversations with stakeholders, and posessing clear communication skills.'
        # if author.get('bio'):
        #     if author_info['summary']:
        #         author_info['summary'] += f". {author.get('bio')}"
        #     else:
        #         author_info['summary'] = author.get('bio')

        # Add social profiles
        profiles = []

        # Academic profiles
        # if author.get('googlescholar'):
        #     profiles.append({
        #         "network": "Google Scholar",
        #         "username": "",
        #         "url": author.get('googlescholar')
        #     })

        # if author.get('orcid'):
        #     profiles.append({
        #         "network": "ORCID",
        #         "username": "",
        #         "url": author.get('orcid')
        #     })

        # if author.get('researchgate'):
        #     profiles.append({
        #         "network": "ResearchGate",
        #         "username": "",
        #         "url": author.get('researchgate')
        #     })

        # Social media profiles
        if author.get('github'):
            profiles.append({
                "network": "GitHub",
                "username": author.get('github'),
                "url": f"https://github.com/{author.get('github')}"
            })

        if author.get('linkedin'):
            profiles.append({
                "network": "LinkedIn",
                "username": author.get('linkedin'),
                "url": f"https://www.linkedin.com/in/{author.get('linkedin')}"
            })

        author_info['profiles'] = profiles

    return author_info


def parse_education(education_file):
    """Parse education section from markdown."""
    education_df = pd.read_json(education_file)
    education_entries = []
    for thing in education_df.itertuples():
        education_entries.append({
            "institution": thing.institution,
            "area": thing.area,
            "studyType": thing.studyType,
            "startDate": thing.startDate,
            "endDate": thing.endDate,
            "courses": thing.courses
        })
    return education_entries


def parse_work_experience(work_file):
    """Parse work experience section from markdown."""
    work_entries = []
    work_exp_df = pd.read_json(work_file)
    for job in work_exp_df.itertuples():
        company = job.company
        position = job.position
        startDate = job.startDate
        endDate = job.endDate
        summary = job.summary
        highlights = job.highlights
        link = job.link
        work_entries.append({
            "company": company,
            "position": position,
            "startDate": startDate,
            "endDate": endDate,
            "summary": summary,
            "link": link,
            "highlights": highlights,
        })



    return work_entries


def parse_skills(skills_file):
    """Parse skills section from markdown."""

    # Extract skill categories
    # categories = re.findall(r'(?:^|\n)(\w+.*?):\s*(.*?)(?=\n\w+.*?:|\Z)', skills_text, re.DOTALL)
    # print(categories)
    # for category, skills in categories:
    # Extract individual skills
    # skill_list = [s.strip() for s in re.split(r',|\n', skills) if s.strip()]
    skills_df = pd.read_json(skills_file)
    skills_entries = []
    for skill in skills_df.itertuples():
        skills_entries.append({
            "name": skill.name,
            "level": skill.level,
            "keywords": skill.keyword
        })

    return skills_entries


def parse_projects(pub_dir):
    """Parse projects from the _projects directory."""
    projects = []

    if not os.path.exists(pub_dir):
        return projects

    for pub_file in sorted(glob.glob(os.path.join(pub_dir, "*.md"))):
        with open(pub_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Extract front matter
        front_matter_match = re.match(r'^---\s*(.*?)\s*---', content, re.DOTALL)
        if front_matter_match:
            front_matter = yaml.safe_load(front_matter_match.group(1))

            # Extract publication details
            pub_entry = {
                "name": front_matter.get('title', ''),
                "publisher": front_matter.get('venue', ''),
                "releaseDate": front_matter.get('date', ''),
                "website": front_matter.get('paperurl', ''),
                "summary": front_matter.get('excerpt', '')
            }

            projects.append(pub_entry)

    return projects


def parse_portfolio(portfolio_dir):
    """Parse portfolio items from the _portfolio directory."""
    portfolio = []

    if not os.path.exists(portfolio_dir):
        return portfolio

    for portfolio_file in sorted(glob.glob(os.path.join(portfolio_dir, "*.md"))):
        with open(portfolio_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Extract front matter
        front_matter_match = re.match(r'^---\s*(.*?)\s*---', content, re.DOTALL)
        if front_matter_match:
            front_matter = yaml.safe_load(front_matter_match.group(1))

            # Extract portfolio details
            portfolio_entry = {
                "name": front_matter.get('title', ''),
                "category": front_matter.get('collection', 'portfolio'),
                "date": front_matter.get('date', ''),
                "url": front_matter.get('permalink', ''),
                "description": front_matter.get('excerpt', '')
            }

            portfolio.append(portfolio_entry)

    return portfolio


# Custom JSON encoder to handle date objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


if __name__ == '__main__':
    main()
