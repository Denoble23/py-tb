

import numpy
from matplotlib import pyplot as plt

from pytb.client import screenshot
from pytb.configuration import load_user_settings
from pytb.database import Database
from pytb.logger import Logger

logger = Logger()
users_ive_followed_from_database = Database("users_ive_followed_from")
user_settings = load_user_settings()
launcher_path = user_settings["launcher_path"]

# orientate_edge_window(logger)

plt.imshow(numpy.asarray(screenshot(region=[0, 0, 1400, 2000])))
plt.show()
