# encoding=utf-8
"""
Devl env: python3, matplotlib;
Developer: zengyue;
Encoding: utf-8.
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
class Draw():
    """Function: Draw line chart, bar chart, column chart, cumulative distribution function chart."""
    def __init__(self, figType='eps', font_family='Times New Roman', font_size=26, fig_size = (7.2,4.6), line_width=2, 
        fig_left=0.18, fig_right=0.98, fig_bottom=0.18, fig_top=0.92, agg_fig=False, show_fig=True, show_grid=True,
        show_title=False):
        self.figType = figType
        self.colors = ['red', 'green', 'blue', 'c', 'm','yellow', 'black', 'white']     # the line colors
        self.mecs = self.colors     # the edge color of markers
        self.mfcs = 'white'     # the interner color of markers
        self.edge_color = 'white'
        #self.markers = ['/', '//', 'x', '\\\\', '\\']     #markers on each line
        self.markers = ['o', 'x', '^', '.', '*', '-', '+', 'x', 'O']  # markers on each line
        self.hatchs = self.markers  #hatches
        self.line_style = ['-', '-.', ':', '--', '-:']
        self.locations = ['best','upper right','upper left','lower left','lower right','right','center left','center right','lower center','upper center','center']

        self.font_size = font_size
        self.fig_size = fig_size
        self.fig_top = fig_top
        self.fig_bottom = fig_bottom
        self.fig_left = fig_left
        self.fig_right = fig_right
        self.line_width = line_width

        #setting default paramenters
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = self.font_size
        plt.rcParams['figure.figsize'] = self.fig_size
        plt.rcParams['lines.linewidth'] = self.line_width

        # paramenters
        plt.rcParams['figure.subplot.top'] = self.fig_top
        plt.rcParams['figure.subplot.bottom'] = self.fig_bottom
        plt.rcParams['figure.subplot.left'] = self.fig_left
        plt.rcParams['figure.subplot.right'] = self.fig_right
        print(self.fig_top,self.fig_bottom,self.fig_left,self.fig_right)

        # show or not
        self.show_fig = show_fig
        self.show_grid = show_grid
        self.show_title = show_title

        # enable execution on systems without a GUI graphical interface
        if agg_fig:
            plt.switch_backend('agg')

    def barChart(self, xData, yData, xLim, yLowErrors, yUpErrors, barLabels, figName, xLabel, yLabel, bar_width, xLowBound=0, xUpBound=100, 
        yLowBound=0, yUpBound=1,scale=1,legLoc='default',numColumn=1,loc="best"):

        # paramenters
        plt.rcParams['figure.subplot.top'] = self.fig_top
        plt.rcParams['figure.subplot.bottom'] = self.fig_bottom
        plt.rcParams['figure.subplot.left'] = self.fig_left
        plt.rcParams['figure.subplot.right'] = self.fig_right

        # scale or not
        if scale == 10:
            plt.text(50, yUpBound+0.2, r'× 10$^{1}$')
            print('scale',scale)
        if scale == 100:
            print('scale',scale)
            plt.text(50, yUpBound+0.2, r'× 10$^{2}$')
        if scale == 1000:
            print('scale',scale)
            plt.text(50, yUpBound+0.2, r'× 10$^{3}$')

        len_data = len(yData)

        for i in range(0, len_data):
            Y_error = [np.array(yLowErrors[i]),np.array(yUpErrors[i])]
            plt.bar(xData+(i-1.5)*bar_width,yData[i],yerr=Y_error,width = bar_width,facecolor = self.colors[i], edgecolor = self.edge_color,
                align="center",label=barLabels[i],hatch=self.hatchs[i])

        plt.xlim(xLowBound, xUpBound)
        plt.ylim(yLowBound, yUpBound)

        plt.xlabel(xLabel)  
        plt.ylabel(yLabel)

        plt.xticks(xData,xLim)  
        plt.yticks()

        plt.legend(ncol=numColumn,loc=loc,fontsize=self.font_size-4)

        plt.grid(self.show_grid)
        plt.savefig(figName+"."+self.figType)

        if self.show_fig:
            plt.show()

        plt.close()

    def barChartExample(self):
        xData = np.array([10, 20, 30, 40, 50])
        yDatas = [[42.98, 34.31, 34.01, 29.69, 33.14], [47.5, 35.97, 33.85, 28.74, 32.33],
                  [96.98, 99.33, 102.42, 92.38, 97.99], [83.31, 69.87, 73.55, 63.21, 69.17]]
        yLowErrors = [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]
        yUpErrors = [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]
        x_step = xData[1] - xData[0]
        barLabels = ['SBD', 'Heuristic', 'RABA', 'Static Backup']
        self.barChart(xData=xData, yData=yDatas, yLowErrors=yLowErrors, yUpErrors=yUpErrors, xLim=xData,
                          barLabels=barLabels, figName="fig-3", xLabel="Number of Servers", yLabel="Resource Cost",
                          bar_width=1.5, xLowBound=x_step / 2, xUpBound=max(xData) + x_step / 2, yLowBound=0,
                          yUpBound=1.6 * max(map(max, yDatas)), scale=0, legLoc="default", numColumn=2,
                          loc='upper left')

    def cdfChart(self, xData, yData, lineLabels, figName, xLabel, yLabel='CDF', xLowBound=0, xUpBound=100, yLowBound=0, yUpBound=1, width = 1.5, paramInput=False, numColumn=1, paramLen=2,loc="best"):

        #ax = plt.gca()
        #ax.set_xscale('log')
        for i in range(0, len(xData)):
            # insert start value
            xData[i].insert(0,0)
            yData[i].insert(0,0)

            # insert end value
            xData[i].append(xUpBound)
            yData[i].append(1)

        for i in range(0, len(xData)):
            if paramInput:
                plt.plot(xData[i], yData[i], linestyle=self.line_style[i % paramLen], color=self.colors[i // paramLen], drawstyle='steps-post', linewidth=3, label=lineLabels[i])
            else:
                plt.plot(xData[i], yData[i], linestyle=self.line_style[i], color=self.colors[i], drawstyle='steps-post', linewidth=3, label=lineLabels[i])

        #plt.xlim(xLowBound, xUpBound)
        plt.ylim(yLowBound, yUpBound)

        plt.xlabel(xLabel)
        plt.ylabel(yLabel)

        plt.xticks()
        plt.yticks()

        plt.legend(ncol=numColumn,loc=loc,fontsize=self.font_size-4)
        plt.grid(self.show_grid)

        plt.savefig(figName + "." + self.figType)

        if self.show_fig:
            plt.show()
        plt.close()

    def cdfExample(self):
        # CDF chart example
        lineLabels = ['ALG-1', 'ALG-2']
        xDatas = [[1, 2, 3, 4, 5, 6, 7], [2, 3, 4, 5, 6, 7, 8]]
        yDatas = []
        for i in range(0, len(xDatas)):
            yData = []
            for j in range(1, len(xDatas[i])+1):
                yData.append(j/len(xDatas[i]))
            yDatas.append(yData)
        print("ydatas:",yDatas)

        self.cdfChart(xDatas, yDatas, lineLabels=lineLabels, figName="Fig-Default", xLabel="Downtime", yLabel='CDF',
                         xLowBound=0, xUpBound=max(map(max, xDatas)), yLowBound=0, yUpBound=1)

    def errorbarChart(self, xData, yDatas, yUpErrors, yLowErrors, lineLabels, figName="fig-1", xLabel="xLabel",
                  yLabel="yLabel", xLowBound=1.0,
                  xUpBound=100.0, yLowBound=1.0, yUpBound=100.0, title_name="Default title", xTicks=[]):

        # data number
        len_data = len(yDatas)
        xData = np.array(xData)
        fmts = ["ro-", "g^-."]

        for i in range(0, len_data):
            Y_error = [np.array(yLowErrors[i]), np.array(yUpErrors[i])]
            plt.errorbar(xData, yDatas[i], yerr=Y_error, xlolims=True, label=lineLabels[i], fmt=fmts[i],
                         marker=self.markers[i], markersize=10, ecolor=self.colors[i], elinewidth=3, mfc="w",
                         mec=self.colors[i], capsize=4, capthick=3)

        # set x axis and y axis(font and range)
        if len(xTicks) > 0:
            plt.xticks(xTicks)
        plt.yticks()
        plt.xlim(xLowBound, xUpBound)
        plt.ylim(yLowBound, yUpBound)

        # set x label, y label and legend
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.legend(loc='upper left')

        # show grid or not
        plt.grid(self.show_grid)

        # show titile or not
        if self.show_title:
            plt.title(title_name)

        # save figure
        plt.savefig(figName + "." + self.figType)

        # show figure
        if self.show_fig:
            plt.show()

        plt.close()

    def errorbarExample(self):
        #error bar example
        xData = [2,3,4,5,6,7]
        yDatas = [[2.20191, 3.07318, 4.76338, 7.48920, 7.89779, 11.10754], [2.20191, 3.07318, 4.74192, 7.47178, 7.84663, 10.96752]]
        yUpErrors = [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]
        yLowErrors = [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]
        lineLabels = ['Heuristic Algorithm','Optimal Solution']
        xStep = xData[1] - xData[0]
        yMulti = 1.2

        self.errorbarChart(xData=xData, yDatas=yDatas, yUpErrors=yUpErrors, yLowErrors=yLowErrors, lineLabels=lineLabels, figName="fig-2", xLowBound=min(xData)-xStep/4, xUpBound=max(xData)+xStep/4, yLowBound=0, yUpBound=yMulti*max(map(max, yDatas)),xTicks=xData)

if __name__=='__main__':
    # initial the Draw
    #new_Draw = Draw(agg_fig=False, fig_size = (7.2,4.6), fig_left=0.15, fig_right=0.98, fig_bottom=0.18, fig_top=0.92)
    #new_Draw.barChartExample()
    #new_Draw = Draw(agg_fig=False, fig_size=(7.2, 4.6), fig_left=0.15, fig_right=0.98, fig_bottom=0.18, fig_top=0.92)
    #new_Draw.cdfExample()
    new_Draw = Draw(agg_fig=False, fig_size=(7.2, 4.8), fig_left=0.15, fig_right=0.98, fig_bottom=0.18, fig_top=0.92)
    new_Draw.errorbarExample()