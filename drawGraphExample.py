import matplotlib.pyplot as plt

# 데이터
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# 그래프 그리기
plt.plot(x, y, marker='o', linestyle='-', color='b')

# 제목과 레이블 설정
plt.title('Simple Line Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# 그래프 보여주기
plt.show()