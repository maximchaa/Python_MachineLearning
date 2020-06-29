import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation


T = 280

FFMpegWriter = manimation.writers['ffmpeg']

writer = FFMpegWriter(fps=25)

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()

writer.setup(fig, "video.avi" , 300)

# Создаём сетку
#x = np.arange(0, 30, 0.1)
x=np.loadtxt("X.txt")


for t in range(80, T):
# Выводим номер кадра на экран для удобства
    print('Drawing frame %d...' % (t))

# Заводим функцию на сетке
    #y = (-1)**t*np.sin(x*t/T)
    y=np.loadtxt("Y"+str(t)+".txt")
# Рисуем
    plt.plot(x, y)
    plt.title("T = %f" % (t))

# Сохраняем кадр
    writer.grab_frame()

# Очищаем рисунок для следующей итерации
    plt.clf()
