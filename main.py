import csv
import argparse

# https://stackoverflow.com/a/1165552/2544133
class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect
    def removed(self):
        return self.set_past - self.intersect
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("panel_path")
    parser.add_argument("slack_path")
    args = parser.parse_args()
    panel_path = args.panel_path
    slack_path = args.slack_path
    # https://stackoverflow.com/a/23090697/2544133
    panel_csv = dict()
    slack_csv = dict()
    with open(panel_path, 'r', encoding='utf-8') as panel_file:
        for i, r in enumerate(csv.reader(panel_file)):
            if i == 0:
                continue
            if r[4] == 'czlonek':
                r[4] = 1
            else:
                r[4] = 0
            panel_csv[r[3]] = r[4]
    with open(slack_path, 'r', encoding='utf-8') as slack_file:
        for i, r in enumerate(csv.reader(slack_file)):
            if i == 0:
                continue
            if r[2] == 'Member':
                r[2] = 1
            else:
                r[2] = 0
            slack_csv[r[1]] = r[2]

    print("People who are on Slack, but aren't members")
    slack_person_nonmembers = list()
    for slack_person_email, slack_person_access in slack_csv.items():
        if slack_person_access == 1:
            if not slack_person_email in panel_csv:
                continue
            if panel_csv[slack_person_email] == 0:
                slack_person_nonmembers.append(slack_person_email)
    print(slack_person_nonmembers)

    print("People who are members, but aren't on Slack")
    members_nonslack_person = list()
    for member_email, member_access in panel_csv.items():
        if member_access == 1:
            if not member_email in slack_csv:
                continue
            if slack_csv[member_email] == 0:
                members_nonslack_person.append(member_email)
    print(members_nonslack_person)

    # People who aren't mentioned on one of the lists
    diff_dicts = DictDiffer(panel_csv, slack_csv)

    print("People who are on Slack list but aren't mentioned on panel")
    print(diff_dicts.removed())

    print("People who are on panel but aren't mentioned on Slack list")
    print(diff_dicts.added())


if __name__ == "__main__":
    init()