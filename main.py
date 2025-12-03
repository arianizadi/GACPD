import os
import sys
from GACPD.GACPD import GACPD

# List of specific PRs to analyze for apache/kafka
pr_numbers = [18287, 13810, 15783, 16558, 17788, 17822, 18835]

token_list = []
token_file = 'tokens.txt'

if not os.path.exists("reports"):
    os.mkdir("reports")

if not os.path.exists("src"):
    os.mkdir("src")

if not os.path.exists("cmp"):
    os.mkdir("cmp")

print(os.getcwd())

with open(token_file, 'r') as f:
    for line in f.readlines():
        token_list.append(line.strip('\n'))

# Setup data for apache/kafka and linkedin/kafka
data = ('kafka_specific_prs', 'apache/kafka', 'linkedin/kafka', token_list, '', '')

# Initialize GACPD
example = GACPD(data)
example.get_single_dates()

# Get git information (only run once per dataset)
print("\nFetching git information...")
example.get_git_information()

# Analyze each PR
print(f"\nAnalyzing {len(pr_numbers)} specific PRs...")
for pr_num in pr_numbers:
    print(f"\n{'='*70}")
    print(f"Analyzing PR #{pr_num}")
    print(f"{'='*70}")
    try:
        example.individual_pr_check(pr_num)
        print(f"✓ Successfully analyzed PR #{pr_num}")
    except Exception as e:
        print(f"✗ Error analyzing PR #{pr_num}: {str(e)}")
        continue

print(f"\n{'='*70}")
print("Analysis complete!")
print(f"{'='*70}")
print(f"\nResults are located in: Results/Repos_results/kafka_specific_prs/[PR_NUM]/[classification]/[filename]/results/index.html")