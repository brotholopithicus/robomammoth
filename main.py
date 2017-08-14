from urllib.parse import urlparse

import praw
import time

# location of file where id's of already visited comments are maintained
submissions_path = 'submissions.txt'
comments_path = 'comments.txt'

# users to upvote posts for
user_list = ['MammothQueen', 'Mammoth_King']

def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit('robomammoth', user_agent = 'web:robomammoth:v0.1 (by MammothKing)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

def run_upvoter(user):
    print('\nUpvoting Submissions From {}\n'.format(user))

    submissions = list(user.submissions.new())
    comments = list(user.comments.new())

    if not len(submissions):
        print('No Submissions From {}\n'.format(user))
    if not len(comments):
        print('No Comments From {}\n'.format(user))

    for submission in submissions:
        file_obj_r = open(submissions_path, 'r')
        if submission.id not in file_obj_r.read().splitlines():
            print('Unique Submission ID! Upvoting Submission ID: {}!'.format(submission.id))
            file_obj_r.close()
            file_obj_w = open(submissions_path, 'a+')
            file_obj_w.write(submission.id + '\n')
            file_obj_w.close()
            submission.upvote()
        else:
            print('Already Voted On Submission ID: {}'.format(submission.id))

    print('\nUpvoting Comments From: {}\n'.format(user))

    for comment in comments:
        file_obj_r = open(comments_path, 'r')
        if comment.id not in file_obj_r.read().splitlines():
            print('Unique Comment ID! Upvoting Comment ID: {}!'.format(comment.id))
            file_obj_r.close()
            file_obj_w = open(comments_path, 'a+')
            file_obj_w.write(comment.id + '\n')
            file_obj_w.close()
            comment.upvote()
        else:
            print('Already Voted On Comment ID: {}'.format(comment.id))

def main():
    reddit = authenticate()
    while True:
        for user in user_list:
            redditor = reddit.redditor(user)
            run_upvoter(redditor)
        print('Waiting 60 seconds...\n')
        time.sleep(60)
main()
