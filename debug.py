

from matplotlib import pyplot as plt
import numpy


from logger import Logger
from database import Database


logger=Logger()
users_ive_followed_from_database= Database("users_ive_followed_from")



# orientate_twitter_window(logger)

# plt.imshow(numpy.asarray(screenshot()))
# plt.show()


print("start")
username_to_add="tsaetsdsdfg"
users_ive_followed_from_database.add_username_to_database(username_to_add)
print("end")