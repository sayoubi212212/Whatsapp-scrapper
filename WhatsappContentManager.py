from Consts import *
import datetime
from WhatsappPageCrawler import *
from ContentManager import *
from Env import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class WhatsappContentManager(ContentManager):
    def __init__(self, contact):
        self.crawler = WhatsappPageCrawler(WHATSAPP_WEB_URL, contact)
        self.working_dir = BASE_WORKING_DIR + r"whatsapp\\"
        self.contact = contact

    def searchData(self, *args):
        # recieves (start_time, end_time) to search between.

        pickle_file_path = self.working_dir + self.contact + ".pickle"
        if not os.path.exists(pickle_file_path):
            raise RuntimeError("No data has been fetched yet")
        try:
            for sample in Env.pickleIterator(pickle_file_path):
                print(sample)
        except:
            raise RuntimeError("Cannot access pickle file data")


    def startAutolFetch(self, interval):
        self.crawler.startAutolFetch(interval)

    def stopAutoFetch(self):
        self.crawler.stopAutolFetch()

    def analyzeTimeFrames(self):
        # prints time frames that represent the user's login pattern

        pickle_file_path = self.working_dir + self.contact + ".pickle"
        dtime = []
        status = []

        # fetch all sampled data
        for sample in Env.pickleIterator(pickle_file_path):
            dtime.append(sample[0])
            status.append(sample[1])

        # analyze
        l = len(dtime)
        spanStart = None  # stores every span's start datetime
        spanEnd = None  # stores every span's end datetime
        isInSpan = False
        isPreviousTrue = False
        totalDuration = datetime(1, 1, 1, 0, 0)

        for i in range(l):
            if status[i]:
                if isInSpan == False:  # if the user is logged in, we check if we are already in a time span
                    spanStart = dtime[i]
                    spanEnd = dtime[i]
                    isInSpan = True
                else:     # if we are already in a time span, the current time could be the span end
                    spanEnd = dtime[i]
                isPreviousTrue = True
            else:  # user offline
                isInSpan = False
                if isPreviousTrue:  # checks if we just ended a time span
                    isPreviousTrue = False
                    if spanStart is spanEnd:
                        print("user was briefly logged in at {}".format(str(spanStart).split(".")[0]))
                    else:
                        duration = spanEnd - spanStart
                        totalDuration += duration
                        print("user was logged in at {} for {}".format(str(spanStart).split(".")[0],
                                                                       str(duration).split(".")[0]))
        if (status[-1]):
            if (spanStart is spanEnd):
                print("user was briefly logged in at {}".format(str(spanStart).split(".")[0]))
            else:
                duration = spanEnd - spanStart
                totalDuration += duration
                print("user was logged in at {} for {}".format(str(spanStart).split(".")[0],
                                                               str(duration).split(".")[0]))
        print("total login time: {} , measured from {} to {}".format(totalDuration.time(), dtime[0], dtime[-1]))

    def showGraph(self):
        # shows a pyplot graph
        pickle_file_path = self.working_dir + self.contact + ".pickle"
        datetimes = []
        status = []

        # fetch all sampled data

        for sample in Env.pickleIterator(pickle_file_path):
            datetimes.append(sample[0])
            status.append(sample[1])

        # prepare string formatted datetimes
        datetimes_strings = [i.strftime('%H:%m:%S') for i in datetimes]

        # plot the graph
        fig = plt.figure()
        fig.suptitle(self.contact, fontsize=20)
        plt.xlabel('time')
        plt.ylabel('status')
        ax = fig.add_subplot(111)
        plt.plot(datetimes, status)
        plt.xticks(datetimes[0::60])  # show one sample in a hundred in the graph's axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%m:%S'))
        fig.autofmt_xdate()  # rotate the x axis values
        plt.show()
