import math
grid = []

while True:
	l = list(input())
	if len(l) > 0 and l[-1] == "\r":
		l.pop()
	l = "".join(l)
	if l == "":
		break
	grid.append(l)

moves = input().strip()

H = len(grid)
W = max(len(l) for l in grid)

# 全面の面積を数えて、1面の面積から、1面の大きさsを計算
count = 0
for l in grid:
	count += sum(1 if c != " " else 0 for c in l)

if count % 6 != 0:
	raise Exception

s = round(math.sqrt(count // 6))
if (s ** 2) * 6 != count:
	raise Exception(f"{s}^2 != {count}")

# ベクトルの加減算
def add(*v):
	return tuple(sum(d) for d in zip(*v))

def sub(v1, v2):
	return tuple(a - b for a, b in zip(v1, v2))

def rev(v):
	return tuple(-a for a in v)

# ベクトルの回転
def rotate_l(dx, dy):
	return dy, -dx

def rotate_r(dx, dy):
	return -dy, dx

# 入力を平面ではなく、平面の裏側にそれぞれキューブが張り付いているものと考える。
# それぞれのキューブは、平面上の(x, y)座標で区別出来る。以降、キューブと言った場合はこの(x, y)座標の事とする。
# この状態から題意通りに折り畳むと、頂点は3つのキューブが重なった状態、それ以外の辺は2個のキューブが重なった状態になる。

# 折り畳んだ後の各面の各辺について、その辺の(1x1x1立方体上の点の辺の始点, 終点): 
# (始点キューブ, 終点キューブへの向きベクトル, 反転したかどうかのフラグ)、というdictを作りたい。
# (一意にするため、立方体上の座標は、始点 < 終点になるよう記録。反転した場合はフラグを立てる)
edges = {}

# 最上段左端のキューブを基点にする。
y = 0
for i in range(len(grid[0])):
	if grid[0][i] != " ":
		x = i
		break

# あくまで、平面上を6面、DFSで探索する。
# 現在探索中の面の左上隅の(x, y)座標と、そのキューブの隅が1x1x1の立方体上のどの座標に該当するかを示すpと、
# 平面上のx軸、y軸、z軸の空間上でのベクトル(z軸は画面こっち向き)の組み合わせが、探索中のstateとして必要。
queue = [(x, y, (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, -1))]

# 探索済みの面の左上隅の座標を覚えておくset
visited = {(x, y)}
while queue:
	# 現在の状況をpop
	x, y, p, vx, vy, vz = queue.pop()
	
#	print(x, y)
	
	# 現在の面の4隅のキューブのリスト
	cube_ps = [(x, y), (x + s - 1, y), (x + s - 1, y + s - 1), (x, y + s - 1)]
	
	# 現在の面の4隅の立方体上の座標
	axis_ps = [p, add(p, vx), add(p, vy, vx), add(p, vy)]
	
	# 立方体上の辺→キューブの端点, キューブ上の辺の向き
	dx = 1
	dy = 0
	for i in range(4):
		c1 = cube_ps[i]
		c2 = cube_ps[(i + 1) % 4]
		a1 = axis_ps[i]
		a2 = axis_ps[(i + 1) % 4]
		# 一意にするため、立方体上の座標が小さい方を先に。
		if a1 > a2:
			# 逆転させる場合は、座標を入れ替え、ベクトルを反転し、反転フラグを立てる
			a1, a2 = a2, a1
			c1, c2 = c2, c1
			tdx = -dx
			tdy = -dy
			r = True
		else:
			tdx = dx
			tdy = dy
			r = False
		at = (a1, a2)
		ct = (c1, (tdx, tdy), r)
		if at in edges:
			edges[at].append(ct)
		else:
			edges[at] = [ct]
		dx, dy = rotate_r(dx, dy)
	
	# 現在の面と、右左下上の面の繋がりを順に探索
	for d, dx, dy in (("R", s, 0), ("L", -s, 0), ("D", 0, s), ("U", 0, -s)):
		# そっちの面の左上のキューブの座標(nx, ny)を求める
		nx = x + dx
		ny = y + dy
		# そっちに面が有るかどうかチェック
		if ny >= 0 and nx >= 0 and ny < H and nx < len(grid[ny]) and grid[ny][nx] != " " and (nx, ny) not in visited:
			# あれば、そっちの面基準になるように回した空間ベクトル(nvx, nvy, nvz)を求める
			if d == "R":
				nvx = rev(vz)
				nvy = vy
				nvz = vx
				np = add(p, vx)
			elif d == "L":
				nvx = vz
				nvy = vy
				nvz = rev(vx)
				np = sub(p, nvx)
			elif d == "D":
				nvx = vx
				nvy = rev(vz)
				nvz = vy
				np = add(p, vy)
			else: # d == "U"
				nvx = vx
				nvy = vz
				nvz = rev(vy)
				np = sub(p, nvy)
			# 探索済みをチェックして、キューに隣の面を追加
			visited.add((nx, ny))
			queue.append((nx, ny, np, nvx, nvy, nvz))

#print(nodes)

#print("e")
#for x in edges.items():
#	print(x)

# 今(x, y)に居て、(dx, dy)方向に移動しようとしている、というときに、その移動は面の境界を越えて(nx, ny)に移動し向きは(ndx, ndy)になる、
# という場合に限って、その結びつきを、(x, y, dx, dy): ((nx, ny), (ndx, ndy))として記録しておくdictにする。
warps = {}

for ap, cp in edges.items():
	# 各立方体の辺について、キューブ上の辺2本ずつが登録されているはず。
	if len(cp) != 2:
		raise Exception
	
	# キューブ上の辺のデータ(始点, 終点座標へのベクトル, 反転したか)を取り出し。
	(cp1, cd1, cr1), (cp2, cd2, cr2) = cp
	
	# 反転した場合は、その面へは、終点方向へ向かって右から入って左に出る。反転してない場合はその逆。
	# それぞれ、out、inのベクトルとして向きを計算しておく
	if cr1:
		co1 = rotate_r(*cd1)
		ci1 = rotate_l(*cd1)
	else:
		co1 = rotate_l(*cd1)
		ci1 = rotate_r(*cd1)
	if cr2:
		co2 = rotate_r(*cd2)
		ci2 = rotate_l(*cd2)
	else:
		co2 = rotate_l(*cd2)
		ci2 = rotate_r(*cd2)
#	print(cp)
	
	# 始点から終点へ順に各キューブ間のワープを登録
	for i in range(s):
#		print(cp1, cp2)
		if (*cp1, *co1) in warps:
			raise Exception
		warps[(*cp1, *co1)] = (cp2, ci2)
		if (*cp2, *co2) in warps:
			raise Exception
		warps[(*cp2, *co2)] = (cp1, ci1)
		cp1 = add(cp1, cd1)
		cp2 = add(cp2, cd2)

#for l in warps.items():
#	print(l)

print(x, y)

# (x, y)から、(dx, dy)だけ動くとどこへ行くかを返す。詰まってて移動出来ないときはNone
def move(x, y, dx, dy):
#	print((x, y), (dx, dy))
	if (x, y, dx, dy) in warps:
		# warpsのテーブルにある状況の時はワープする
#		print("wf", (x, y))
		(x, y), (dx, dy) = warps[(x, y, dx, dy)]
#		print("wt", (x, y))
	elif dy == 0:
		# それ以外は普通に移動
		x += dx
#		print("mx", (x, y))
	else:
		y += dy
#		print("my", (x, y))
	# ここまでの仕組み上、はみ出る場合は必ずwarpしてるので座標のチェックなどは不要
	if grid[y][x] == " ":
		raise Exception
	elif grid[y][x] == "#":
		# 壁ならNone
		return None
	else:
		return (x, y, dx, dy)

# デバッグ用に、向きの数値→矢印キャラ
arrows = ">v<^"

# 最後に必要なので、向き→数値のテーブル
dirs = {
	(1, 0): 0,
	(0, 1): 1,
	(-1, 0): 2,
	(0, -1): 3
}

# 開始の(x, y)を求める(2回目。面倒くさいのでコピペ)
y = 0
for i in range(len(grid[0])):
	if grid[0][i] == ".":
		x = i
		break

# 最初の移動方向
dx = 1
dy = 0

# デバッグ用に移動経路
path = {(x, y): arrows[dirs[(dx, dy)]]}

# ただの経路探索
i = 0
while True:
	# 移動回数を読み取り
	l = 0
	while i < len(moves) and moves[i] in "0123456789":
		l *= 10
		l += int(moves[i])
		i += 1
	
	# 回数だけ移動
	for j in range(l):
		# 移動しようとして、できればする、壁に当たってて出来なければ終了。
		n = move(x, y, dx, dy)
		if n == None:
			break
		else:
			x, y, dx, dy = n
		
		# デバッグ用に移動経路を覚えておく
		path[(x, y)] = arrows[dirs[(dx, dy)]]
		
#		for p, l in enumerate(grid):
#			print(*(arrows[dirs[(dx, dy)]] if q == x and p == y else c for q, c in enumerate(l)), sep = "")
#		print()
	
	# まだ続きがあれば、回転
	if i < len(moves):
		t = moves[i]
		# 左右回転。
		if t == "L":
			dx, dy = rotate_l(dx, dy)
		else:
			dx, dy = rotate_r(dx, dy)
		# 続きがあれば続ける(必ず移動で終わるという仕様は見当たらなかったので念のため)
		if i < len(moves):
			i += 1
		else:
			break
	else:
		break

#	print("t", (x, y), (dx, dy))
#	for p, l in enumerate(grid):
#		print(*(path[(q, p)] if (q, p) in path else c for q, c in enumerate(l)), sep = "")
#	print()


# デバッグ用に移動経路を表示
for p, l in enumerate(grid):
	print(*(path[(q, p)] if (q, p) in path else c for q, c in enumerate(l)), sep = "")
print()

# デバッグ用に最終的な座標を表示
print(y + 1, x + 1, dirs[(dx, dy)])

# 答え
print(1000 * (y + 1) + 4 * (x + 1) + dirs[(dx, dy)])
