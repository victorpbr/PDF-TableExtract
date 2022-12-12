from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

poppler_path = r"poppler-22.11.0\Library\bin"


class CoordsGrab:
    def __init__(self, file):
        self.coords = []
        self.cols = []
        self.pages = convert_from_path(file, poppler_path=poppler_path)
        self.fig = plt.figure(1)
        self.ax = self.fig.add_subplot(111)
        self.size = self.pages[0].size
        self.ax.imshow(self.pages[0])
        self.ax.set_title('Select boundary top left corner')
        self.cid = self.ax.figure.canvas.mpl_connect(
            'button_press_event', self)
        plt.show()

    def __call__(self, event):
        ix, iy = event.xdata, event.ydata

        if len(self.coords) < 2:
            self.coords.append((ix, iy))
        else:
            self.cols.append(ix)

        if len(self.coords) == 1:
            self.ax.set_title('Select boundary bottom right corner')

        if len(self.coords) == 2:
            self.ax.set_title(
                'Click on the columns posistions, right click to exit')
            width = self.coords[1][0] - self.coords[0][0]
            height = self.coords[1][1] - self.coords[0][1]
            rect = patches.Rectangle(
                self.coords[0], width, height, linewidth=1, edgecolor='r', facecolor='none')
            self.ax.add_patch(rect)

        if len(self.cols) > 0:
            plt.vlines(x=ix, ymin=self.coords[0][1],
                       ymax=self.coords[1][1], colors='red')

            if event.button == 3:
                self.cols.pop()
                event.canvas.mpl_disconnect(self.cid)
                plt.close(1)

        self.ax.figure.canvas.draw_idle()
