import praw
import time
import os

# location of files with submission and comment id's already voted on
submissions_path = 'submissions.txt'
comments_path = 'comments.txt'

# users to upvote posts for
user_list = ['MammothQueen', 'Mammoth_King']

clear = lambda: os.system('clear')

def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit('robomammoth', user_agent = 'web:robomammoth:v0.1 (by MammothKing)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    check_messages(reddit)
    return reddit
    
def check_messages(reddit):
    messages = reddit.inbox.all()
    for message in messages:
        if message.dest.name == reddit.user.me():
            subject = message.subject.lower()
            body = message.body.lower()
            key = 'stop'
            if key in subject or key in body:
                author = message.author.name
                if author in user_list:
                    user_list.remove(author)

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
            user.message('Courtesy Call From RoboMammoth', 'Hello fellow mammoth! You have recieved an upvote!')
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
            user.message('Courtesy Call From RoboMammoth', 'Hello fellow mammoth! You have recieved an upvote!')
        else:
            print('Already Voted On Comment ID: {}'.format(comment.id))

def find_mammoth_submissions(reddit):
    subreddit = reddit.subreddit('all').new(limit=2000)
    for submission in subreddit:
        process_submissions(submission)

def process_submissions(submission):
    keywords = ['mammoth', 'woolly', 'prehistoric', 'tusk', 'tiger', 'elephant', 'hairy', 'giant', 'sabre', 'toothed', 'fangs', 'hunted', 'meat']
    normalized_title = submission.title.lower()
    for keyword in keywords:
        if keyword in normalized_title:
            print(submission.title)

def main():
    reddit = authenticate()
    while True:
        find_mammoth_submissions(reddit)

        for user in user_list:
            redditor = reddit.redditor(user)
            run_upvoter(redditor)

        print('\nWaiting 60 seconds...\n')

        time.sleep(60)

if __name__ == '__main__':
    main()
