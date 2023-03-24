import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
xar = []
yar = []
def animate(i):
    pullData = open("sampleText.txt","r").read()
    dataArray = pullData.split('\n')
    if len(dataArray[i])>1:
        x,y = dataArray[i].split(',')
        xar.append(int(x))
        yar.append(int(y))
    ax1.clear()
    print(xar,yar)
    ax1.plot(xar,yar,color="red")
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()