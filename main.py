import csv
import argparse

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("panel_path")
    parser.add_argument("slack_path")
    args = parser.parse_args()
    panel_path = args.panel_path
    slack_path = args.slack_path
    panel_file = open(panel_path, encoding='utf-8', newline='')
    slack_file = open(slack_path, encoding='utf-8', newline='')
    panel_csv = csv.reader(panel_file, delimiter='\"')
    slack_csv = csv.reader(slack_file, delimiter='\"')

if __name__ == "__main__":
    init()