#!/usr/bin/env python
# coding: utf-8

# In[42]:


import math
import xlrd
import csv
import openpyxl
import matplotlib.pyplot as plt

label = []          #ラベル
ave_list = []       #平均値リスト
min_max = []        #平均値リスト各々の最低温度と最高温度・そのポインタのリスト
all_min_max = []    #平均値リスト全体の最低温度と最大温度
diff_temp = []      #各々の最低温度 - 全体の最低温度
min_max_100 = []    #list_100中の全体の最小最大リスト
list_100 = []       #平均値リスト各々の最低温度から100データ抜き出したリスト
list_100_a = []     #diff_temp適応後
min_max_master = [] #diff_temp適応後の最小値最大値
normalize_100 = []  #正規化リスト

min_lb = 30015      #ラベルの最低温度

#------------------------------------------------------------------------------------
#ラベルの作成
def make_Label():
    label.append(0)
    for i in range(0, 101):
        label.append(min_lb + 10*i)

#先頭行にラベルの挿入
def insert_Label(filename):
    with open(filename + ".csv", "r") as f:
        r = csv.reader(f)
        orig = list(r)
    
    with open(filename + "_out.csv", "w", newline='') as f:
        w = csv.writer(f)
        w.writerow(label)
        w.writerows(orig)
#------------------------------------------------------------------------------------
#平均の計算・保存とマスターcsvの作成
def calc_Average(filename):
    temp = []                   #マスターcsvに平均値追加後データを書き込むための一時リスト
    ave_list_elements = []      #平均値リストの配列要素(1次元)
    with open(filename + "_out.csv", "r") as f:
        r = csv.reader(f)
        for row in r:
            ave = 0
            counter = 0
            if row[1] == str(min_lb):
                continue;
            for i in range(1, len(label) - 1):
                ave += label[i] * int(row[i])
                counter += int(row[i])
            ave /= counter
            row[len(label)] = ave
            temp.append(row)
            
            ave_list_elements.append(ave)
            
        #平均値リストにデータ追加(2次元)
        ave_list.append(ave_list_elements)
    
    with open(filename + "_master.csv", "w", newline='') as f:
        w = csv.writer(f)
        w.writerow(label)
        w.writerows(temp)
#------------------------------------------------------------------------------------    
#正規化リストの作成
def normalization():
    
    #最小値最大値を求める
    def min_Max():
        
        for i in range(0, len(ave_list)):
            for j in range(0, len(ave_list[i])):
                if j == 0:
                    #最小値最大値
                    mini = ave_list[i][j]
                    maxi = ave_list[i][j]
                    #最小値最大値のポインタ
                    mini_p = j
                    maxi_p = j

                if ave_list[i][j] < mini:
                    mini = ave_list[i][j]
                    mini_p = j
                if ave_list[i][j] > maxi:
                    maxi = ave_list[i][j]
                    maxi_p = j
            
            #データ列ごとの最小最大値リストへの追加と全体の最小最大値を求める
            min_max.append([mini, maxi, mini_p, maxi_p])
            
        all_mini = min_max[0][0]
        all_maxi = min_max[0][1]
        for j in min_max:  
            if all_mini > j[0]:
                all_mini = mini
            if all_maxi < j[1]:
                all_maxi = maxi
        
        all_min_max.append(all_mini)
        all_min_max.append(all_maxi)
        
        #各々の最低温度と全体の最低温度の差を求める
        for j in min_max:
            diff_temp.append(j[0]- all_min_max[0])
        #最小値から100データ分の最大値探索
        mini_100 = ave_list[0][min_max[0][2]]
        maxi_100 = ave_list[0][min_max[0][2]]
        mini_100_p = 0
        maxi_100_p = 0
        for i in range(0, len(min_max)):
            for k in range(min_max[i][2], min_max[i][2] + 100):
                if ave_list[i][k] > maxi_100:
                    maxi_100 = ave_list[i][k]
                    maxi_100_p = i
                if ave_list[i][k] < mini_100:
                    mini_100 = ave_list[i][k]
                    mini_100_p = i
                    
        min_max_100.append(mini_100)
        min_max_100.append(maxi_100)
        min_max_100.append(mini_100_p)
        min_max_100.append(maxi_100_p)
    
    #diff_tempの適応と最大値を求め直す
    def diff_Adapt():
        
        counter = -1
        for l in ave_list:
            counter += 1
            temp_before = []
            temp_after = []
            for i in range(min_max[counter][2], min_max[counter][2] + 100):
                #100データ抜き出し保存
                temp_before.append(l[i])
                temp_after.append(l[i] - diff_temp[counter])
                
            list_100.append(temp_before)
            list_100_a.append(temp_after)
            
        maxi_after = list_100_a[0][0]
        for m in list_100_a:
            for n in range(0, len(m)):
                if m[n] > maxi_after:
                    maxi_after = m[n]
                    
        min_max_master.append(min_max_100[0])
        min_max_master.append(maxi_after)
    
    #正規化
    def extract_100(mm):
        
        for l in list_100_a:
            temp_normalized = []
            for i in l:
                #正規化
                temp_normalized.append((i - mm[0])/(mm[1]- mm[0]))
                
            normalize_100.append(temp_normalized)
            
        #デバッグ用
        #print("正規化")
        #print(normalize_100)
        #print("diff_temp適応の確認")
        #print(list_100[2][0])
        #print(list_100_a[2][0])
        print("最小値最大値")
        print(min_max)
        print("100データ内の最小最大")
        print(min_max_100)
        print("diff_temp適応後の最小最大")
        print(min_max_master)
        print("各々の最低温度 - 全体の最低温度")
        print(diff_temp)
    
    min_Max()
    diff_Adapt()
    extract_100(min_max_master)
    
#------------------------------------------------------------------------------------
#ユークリッド距離
def euclid(test, basic):
    squares = [(test[i] - basic[i]) ** 2 for i in range(0, len(test))]
    sum_of_sqrt = math.sqrt(sum(squares))
    return 1/(1 + sum_of_sqrt)

#------------------------------------------------------------------------------------
#ピアソンの積率相関係数(PCC)
def pearson(test, basic):
    n = len(test)
    test_mean = sum([test[i] for i in range(0, n)]) / n
    basic_mean = sum([basic[i] for i in range(0, n)]) / n
    test_variance = math.sqrt(sum([((test[i] - test_mean) ** 2) for i in range(0, n)]))
    basic_variance = math.sqrt(sum([((basic[i] - basic_mean) ** 2) for i in range(0, n)]))

    covariance = sum([(test[i] - test_mean)*(basic[i] - basic_mean) for i in range(0, n)])

    if test_variance * basic_variance == 0: return 0

    return covariance / (test_variance * basic_variance)
#------------------------------------------------------------------------------------
#デバッグ用グラフ表示
def plot_Graph():
    #x軸のラベル
    label_x = [i for i in range(0, 100)]
    
    plt.plot(label_x, normalize_100[0], marker="o", color = "red", linestyle = "--")
    plt.plot(label_x, normalize_100[1], marker="o", color = "blue", linestyle = "--")
    plt.plot(label_x, normalize_100[2], marker="o", color = "yellow", linestyle = "--")
    plt.plot(label_x, normalize_100[3], marker="o", color = "green", linestyle = "--");
#------------------------------------------------------------------------------------

if __name__ == '__main__':
    #ラベル作成
    make_Label()
    #ラベルを付ける+平均を出して各々master.csvを作成
    insert_Label("dl")
    insert_Label("ds")
    insert_Label("sl")
    insert_Label("ss")
    
    calc_Average("dl")
    calc_Average("ds")
    calc_Average("sl")
    calc_Average("ss")

    #正規化
    normalization()
    
    print("Euclid")
    print("深長 : " + str(euclid(normalize_100[0], normalize_100[1])))
    print("Pearson")
    print("深長 : " + str(pearson(normalize_100[0], normalize_100[1])))
    plot_Graph()


# In[15]:


import math
import xlrd
import csv
import openpyxl
import matplotlib.pyplot as plt

label=[]            #ラベル
ave_list = []       #平均値リスト
min_max = []        #平均値リスト各々の最低温度と最高温度・そのポインタのリスト
all_min_max = []    #平均値リスト全体の最低温度と最大温度
min_max_100 = []    #list_100中の全体の最小最大リスト
list_100 = []       #平均値リスト各々の最低温度から100データ抜き出したリスト
normalize_100 = []  #正規化リスト

min_lb = 30015      #ラベルの最低温度

#------------------------------------------------------------------------------------
#ラベルの作成
def make_Label():
    label.append(0)
    for i in range(0, 101):
        label.append(min_lb + 10*i)

#先頭行にラベルの挿入
def insert_Label(filename):
    with open(filename + ".csv", "r") as f:
        r = csv.reader(f)
        orig = list(r)
    
    with open(filename + "_out.csv", "w", newline='') as f:
        w = csv.writer(f)
        w.writerow(label)
        w.writerows(orig)
#------------------------------------------------------------------------------------
#平均の計算・保存とマスターcsvの作成
def calc_Average(filename):
    temp = []                   #マスターcsvに平均値追加後データを書き込むための一時リスト
    ave_list_elements = []      #平均値リストの配列要素(1次元)
    with open(filename + "_out.csv", "r") as f:
        r = csv.reader(f)
        for row in r:
            ave = 0
            counter = 0
            if row[1] == str(min_lb):
                continue;
            for i in range(1, len(label) - 1):
                ave += label[i] * int(row[i])
                counter += int(row[i])
            ave /= counter
            row[len(label)] = ave
            temp.append(row)
            
            ave_list_elements.append(ave)
            
        #平均値リストにデータ追加(2次元)
        ave_list.append(ave_list_elements)
    
    with open(filename + "_master.csv", "w", newline='') as f:
        w = csv.writer(f)
        w.writerow(label)
        w.writerows(temp)
#------------------------------------------------------------------------------------    
#正規化リストの作成
def normalization():
    
    #最小値最大値を求める
    def min_Max():
        for i in range(0, len(ave_list)):
            for j in range(0, len(ave_list[i])):
                if j == 0:
                    #最小値最大値
                    mini = ave_list[i][j]
                    maxi = ave_list[i][j]
                    #最小値最大値のポインタ
                    mini_p = j
                    maxi_p = j

                if ave_list[i][j] < mini:
                    mini = ave_list[i][j]
                    mini_p = j
                if ave_list[i][j] > maxi:
                    maxi = ave_list[i][j]
                    maxi_p = j
            
            #データ列ごとの最小最大値リストへの追加と全体の最小最大値を求める
            min_max.append([mini, maxi, mini_p, maxi_p])
            if i == 0:
                all_mini = mini
                all_maxi = maxi
            
            if all_mini < mini:
                all_mini = mini
            if all_maxi > maxi:
                all_maxi = maxi
        
        all_min_max.append(all_mini)
        all_min_max.append(all_maxi)
        #最小値から100データ分の最大値探索
        mini_100 = ave_list[0][min_max[0][2]]
        maxi_100 = ave_list[0][min_max[0][2]]
        for i in range(0, len(min_max)):
            for k in range(min_max[i][2], min_max[i][2] + 100):
                if ave_list[i][k] > maxi_100:
                    maxi_100 = ave_list[i][k]
                if ave_list[i][k] < mini_100:
                    mini_100 = ave_list[i][k]
                    
        min_max_100.append(mini_100)
        min_max_100.append(maxi_100)
        
    #最小値から100データ抜き出す
    def extract_100(mm):
        counter = -1
        for l in ave_list:
            counter += 1
            temp_before = []
            temp_normalized = []
            for i in range(min_max[counter][2], min_max[counter][2] + 100):
                temp_before.append(l[i])
                temp_normalized.append((l[i] - min_max[counter][0])/(mm[1] - min_max[counter][0]))
                
            list_100.append(temp_before)
            normalize_100.append(temp_normalized)
        print("正規化")
        print(normalize_100)
        print("最小値最大値")
        print(min_max)

    min_Max()
    extract_100(min_max_100)
    
#------------------------------------------------------------------------------------
#ユークリッド距離
def distance(test, training):
    squares = [(test[i] - training[i]) ** 2 for i in range(0, len(test))]
    sum_of_sqrt = math.sqrt(sum(squares))
    return 1/(1 + sum_of_sqrt)

#------------------------------------------------------------------------------------
#ピアソンの積率相関係数(PCC)
def pearson(test, training):
    n = len(test)
    test_mean = sum([test[i] for i in range(0, n)]) / n
    training_mean = sum([training[i] for i in range(0, n)]) / n
    test_variance = math.sqrt(sum([((test[i] - test_mean) ** 2) for i in range(0, n)]))
    training_variance = math.sqrt(sum([((training[i] - training_mean) ** 2) for i in range(0, n)]))

    covariance = sum([(test[i] - test_mean)*(training[i] - training_mean) for i in range(0, n)])

    if test_variance * training_variance == 0: return 0

    return covariance / (test_variance * training_variance)
#------------------------------------------------------------------------------------
#デバッグ用グラフ表示
def plot_Graph():
    #x軸のラベル
    label_x = [i for i in range(0, 100)]
        
    plt.plot(label_x, normalize_100[0], marker="o", color = "red", linestyle = "--")
    plt.plot(label_x, normalize_100[1], marker="o", color = "blue", linestyle = "--")
    plt.plot(label_x, normalize_100[2], marker="o", color = "yellow", linestyle = "--")
    plt.plot(label_x, normalize_100[3], marker="o", color = "green", linestyle = "--");
#------------------------------------------------------------------------------------

if __name__ == '__main__':
    #ラベル作成
    make_Label()
    #ラベルを付ける+平均を出して各々master.csvを作成
    insert_Label("dl")
    insert_Label("ds")
    insert_Label("sl")
    insert_Label("ss")
    
    calc_Average("dl")
    calc_Average("ds")
    calc_Average("sl")
    calc_Average("ss")

    #正規化
    normalization()

    print("Euclid")
    print("深長 : " + str(distance(normalize_100[0], normalize_100[1])))
    print("Pearson")
    print("深長 : " + str(pearson(normalize_100[0], normalize_100[1])))
    plot_Graph()


# In[ ]:




