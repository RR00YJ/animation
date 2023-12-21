import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle
import pandas as pd
import numpy as np
import tkinter.filedialog

filetypes = [("CSV (コンマ区切り)", "*.csv")]
data_path = tkinter.filedialog.askopenfilename(filetypes=filetypes, title="ファイルをひらく")

# CSVファイルを読み込む
data = pd.read_csv(data_path)

# タイムスタンプを相対時間に変換
data['Time'] = data['Time'] - data['Time'].iloc[0]

# Y値を反転させる
data['Y'] = max(data['Y']) - data['Y']

# 描画用の図を準備
fig, ax = plt.subplots()
ax.set_xlim(0, max(data['X']) + 1)
ax.set_ylim(0, max(data['Y']) + 1)
drawing_lines = []
erasing_lines = []
eraser_radius = 5

# アニメーションの状態を管理するフラグ
drawing = False
erasing = False

def animate(i):
    global current_line, drawing_lines, erasing_lines, drawing, erasing
    row = data.iloc[i]
    x, y, action = row['X'], row['Y'], row['Action']

    if action in ['start-drawing', 'change-to-pen']:
        drawing = True
        erasing = False
        current_line = [(x, y)]
        drawing_lines.append(current_line)
    elif action == 'move-drawing' and drawing:
        current_line.append((x, y))
    elif action == 'start-erasing':
        drawing = False
        erasing = True
        current_line = [(x, y)]
        erasing_lines.append(current_line)
    elif action == 'move-erasing' and erasing:
        current_line.append((x, y))
    elif action == 'allclear':
        drawing_lines.clear()
        erasing_lines.clear()
        current_line = []
    elif action == 'savenote':
        return []

    # 描画を実施
    ax.lines.clear()
    for line in drawing_lines:
        ax.plot(*zip(*line), color='black')
    for line in erasing_lines:
        ax.plot(*zip(*line), color='white')  # 消しゴムの軌跡を背景色で描画

    return ax.lines  # ここでリストを返す

# 'savenote' アクションまでのフレーム数を決定する
frames_to_animate = data.index[data['Action'] == 'savenote'].tolist()
if frames_to_animate:
    frames_to_animate = frames_to_animate[0] + 1
else:
    frames_to_animate = len(data)

# アニメーションを作成
ani = FuncAnimation(fig, animate, frames=frames_to_animate, init_func=lambda: [], blit=False, repeat=False)

# アニメーションを保存
output_path = 'path' # 保存先を指定
ani.save(output_path, writer=PillowWriter(fps=30))
