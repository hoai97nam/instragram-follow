from tqdm import tqdm

from . import limits
from . import delay

def unfollow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    if not self.check_user(user_id):
        return True
    if limits.check_if_bot_can_unfollow(self):
        delay.unfollow_delay(self)
        if super(self.__class__, self).unfollow(user_id):
            self.logger.info("Unfollow user: %d" % user_id)
            self.total_unfollowed += 1
            return True
    else:
        self.logger.info("Out of unfollows for today.")
    return False

def unfollow_users(self, user_ids):
    self.logger.info("Going to unfollow %d users." % len(user_ids))
    total_unfollowed = 0
    for user_id in tqdm(user_ids):
        if not self.unfollow(user_id):
            delay.error_delay(self)
            while not self.unfollow(user_id):
                delay.error_delay(self)
    self.logger.info("DONE: Total unfollowed %d users. " % total_unfollowed)
    return True

def unfollow_everyone(self):
    your_following = self.get_user_following(self.user_id)
    self.unfollow_users(your_following)
