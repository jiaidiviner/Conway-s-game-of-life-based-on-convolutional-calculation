import argparse
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.ndimage import convolve


def process_image(path, threshold=127):
    image = Image.open(path)
    width, height = image.size
    print(f"您输入的图片大小为：宽{width}个像素，高{height}个像素，共计{width * height}个像素点")

    # 转换为灰度图
    grayscale_img = image.convert('L')
    print("已成功转换为灰度图")

    # 转换为 NumPy 数组
    array_grayscale_img = np.array(grayscale_img)
    print("已成功转换为灰度值数组")

    # 二值化处理，使用阈值
    binary_img = np.where(array_grayscale_img > threshold, 255, 0)
    print(f"已成功使用阈值 {threshold} 进行二值化处理")

    processed_info = [binary_img, width, height]
    return processed_info


def animate(frameNum, img, grid, kernel):
    # 使用卷积计算邻居总和
    neighbor_count = convolve(grid // 255, kernel, mode='constant', cval=0)

    # 应用生命游戏规则
    newGrid = np.where((grid == 255) & ((neighbor_count == 2) | (neighbor_count == 3)), 255, 0)
    newGrid = np.where((grid == 0) & (neighbor_count == 3), 255, newGrid)

    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,


def main():
    parser = argparse.ArgumentParser(description="这是一个有趣的生命游戏，你输入照片，会转化成灰度图，然后进行生命游戏")
    parser.add_argument('picture_path', type=str, help="请输入图片路径")
    parser.add_argument('--interval', type=int, default=50, help="在这里调节帧速率")
    parser.add_argument('--threshold', type=int, default=127, help="灰度图二值化的阈值，默认为 127")
    args = parser.parse_args()

    # 处理图片
    processed_info = process_image(args.picture_path, threshold=args.threshold)
    grid = processed_info[0]
    width = processed_info[1]
    height = processed_info[2]

    # 生成8邻域的核
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    fig, ax = plt.subplots()
    img = ax.imshow(grid, cmap='gray', interpolation='nearest')

    # 创建动画
    ani = animation.FuncAnimation(fig, animate, fargs=(img, grid, kernel), frames=50, interval=args.interval,
                                  save_count=50)
    plt.show()


if __name__ == '__main__':
    main()
#python conway.py "C:\Users\jiaid\Pictures\apple co.png" --interval 100 --threshold 150
