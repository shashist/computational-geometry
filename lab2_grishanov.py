#!/usr/bin/env python
# coding: utf-8

import argparse
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay
from scipy.spatial.distance import cdist
from pylab import rcParams
rcParams['figure.figsize'] = 12, 8

parser = argparse.ArgumentParser()
parser.add_argument('--filename', type=str, default='')
parser.add_argument("--save_fig", action="store_true")
args = parser.parse_args()

if args.filename:
    filename = args.file_name
else:
    filename = input('Enter file name (р_* / п_*): ')

if '.txt' not in filename:
    filename = filename + '.txt'

with open(f'Примеры_Лаб_2_2020/Рыбы+Птицы/{filename}') as f:
    n = int(f.readline())
    points = np.array([[int(i) for i in line.rstrip().split('  ')] for line in f.readlines()])
    m = points[:, 1].min()
    M = points[:, 1].max()
    points[:, 1] = M + m - points[:, 1]

# # 1. Construct Delaunay triangulation
tri = Delaunay(points)

# # 2. Cut off triangle line lens
line_lens_squared = np.vstack((
    ((points[tri.simplices[:, 1]] - points[tri.simplices[:, 0]]) ** 2).sum(1), 
    ((points[tri.simplices[:, 2]] - points[tri.simplices[:, 1]]) ** 2).sum(1), 
    ((points[tri.simplices[:, 0]] - points[tri.simplices[:, 2]]) ** 2).sum(1)
)).T
final_triangles = tri.simplices[line_lens_squared.max(1) < 50]

# # 3. Create hull
edges = np.vstack((
    np.vstack((final_triangles[:, 0], final_triangles[:, 1])).T, 
    np.vstack((final_triangles[:, 1], final_triangles[:, 2])).T, 
    np.vstack((final_triangles[:, 2], final_triangles[:, 0])).T
))
preprocessed_lines = [set((int(edge[0]), int(edge[1]))) for edge in edges]

hull = []
for line in preprocessed_lines:
    if preprocessed_lines.count(line) == 1:
        hull.append(list(line))

# # 4. Get perimeter & area

perimeter = 0
for point in hull:
    perimeter += cdist(points[point], points[point])[1, 0]

area = 0
for (p1, p2, p3) in final_triangles:
    a = ((points[p1] - points[p2]) ** 2).sum(0) ** 0.5
    b = ((points[p2] - points[p3]) ** 2).sum(0) ** 0.5
    c = ((points[p3] - points[p1]) ** 2).sum(0) ** 0.5
    p = (a + b + c) / 2
    area += (p*(p-a)*(p-b)*(p-c)) ** 0.5

print('Perimeter: ', perimeter)
print('Area: ', area)

for point in hull:
    plt.plot(points[point, 0], points[point, 1], 'k-')
plt.plot(points[:,0], points[:,1], 'oc')
plt.title(f'Perimeter: {round(perimeter, 1)}, area: {round(area, 1)}')
if args.save_fig:
    plt.savefig(f'{filename[:-4]}.png')
plt.show()
