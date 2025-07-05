import numpy as np
import random
import math
import time
start_time = time.time()
#可以认为2-opt算法是取一个两个点，然后翻转包括这两个点之间的路径。
class two_opt(object):
    def __init__(self,num_pop,num_city,data):
        self.num_pop = num_pop
        self.num_city = num_city
        self.location = data
        self.dis_mat = self.compute_dismat(num_city)
        self.pop = self.init_pop(num_pop, num_city)
    #根据二维坐标计算距离矩阵
    def compute_dismat(self,num_city):
        matrix=np.zeros((num_city,num_city))
        for i in range(num_city):
            for j in range(num_city):
                if i==j:
                    matrix[i,j]=np.inf
                else:
                    matrix[i,j]=math.sqrt((self.location[i][0]-self.location[j][0])**2+(self.location[i][1]-self.location[j][1])**2)
        return matrix.copy()
    #种群初始化，这里采用随机生成，而不是最近邻算法
    def init_pop(self,num_pop,num_city):
        pop=[]
        for i in range(num_pop):
            pop.append(np.array(random.sample(range(num_city),num_city)))
        return pop
    #计算单条路径的长度
    def path_length(self,path):
        sum=self.dis_mat[path[-1]][path[0]]
        for i in range(len(path)-1):
            sum=sum+self.dis_mat[path[i]][path[i+1]]
        return sum
    #计算种群适应度函数
    def compute_fitness(self,fruits,dis_mat):
        score=[]
        for fruit in fruits:
            length = self.path_length(fruit)
            score.append(1.0 / length)
        return np.array(score)
    #主函数执行2-opt算法并输出最优解
    def main(self):
        fitness=self.compute_fitness(self.pop,self.dis_mat)
        sort_index = np.argsort(-fitness).copy()#如果fitness不是数组，那么np.argsort就无效。
        best_path = self.pop[sort_index[0]].copy()
        best_fitness =fitness[sort_index[0]]
        print('初始解最短路径长度为：%.2f' % (1/best_fitness))
        for i in range(self.num_pop):#对初试解的每个解都用2-opt算法优化到无法再优化的地步。
            improved = True
            best=self.pop[i].copy()
            best_dist = self.path_length(best)
            while improved:
                improved = False
                #best_dist=self.path_length(best)
                for j in range(1,self.num_city-1):
                    for k in range(j+1,self.num_city):
                        new = self.dis_mat[best[j-1],best[k]]+self.dis_mat[best[j],best[(k+1)%self.num_city]]
                        old = self.dis_mat[best[j-1],best[j]]+self.dis_mat[best[k],best[(k+1)%self.num_city]]
                        if new < old:
                            best[j:k + 1] = best[j:k + 1][::-1]  # 如果k+1=num_city，那么best[k+1:]就会等于一个空列表。
                            best_dist = best_dist - old + new
                            improved = True
                            break  # 退出内层循环
                    if improved:
                        break  # 退出外层循环
            print(f"第{i}个个体优化后的路径长度为：{best_dist:.2f}")
            self.pop[i]=best.copy()
        fitness=self.compute_fitness(self.pop,self.dis_mat)
        sort_index = np.argsort(-fitness).copy()#如果fitness不是数组，那么np.argsort就无效。
        best_path = self.pop[sort_index[0]].copy()
        best_fitness =fitness[sort_index[0]]
        print(f"最终的最优路径为:{best_path}")
        print('最终的最短路径长度为：%.2f' % (1/best_fitness))










# 读取数据
def read_tsp(path):
    lines = open(path, 'r').readlines()
    assert 'NODE_COORD_SECTION\n' in lines
    index = lines.index('NODE_COORD_SECTION\n')
    data = lines[index + 1:-1]
    tmp = []
    for line in data:
        line = line.strip().split(' ')
        if line[0] == 'EOF':
            continue
        tmpline = []
        for x in line:
            if x == '':
                continue
            else:
                tmpline.append(float(x))
        if tmpline == []:
            continue
        tmp.append(tmpline)
    data = tmp
    return data
data = read_tsp(r'D:\Users\qwy\Desktop\tsp算例\st70.tsp\st70.tsp')
data = np.array(data)
data = data[:, 1:]
model=two_opt(num_pop=100,num_city=data.shape[0],data=data.copy())
model.main()
end_time = time.time()
print("代码运行时间：", end_time - start_time, "秒")
