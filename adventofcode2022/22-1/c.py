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

# 入力を平面ではなく、平面の裏側にそれぞれキューブが張り付いているものと考える。
# それぞれのキューブは、平面上の(x, y)座標で区別出来る。以降、キューブと言った場合はこの(x, y)座標の事とする。
# この状態から題意通りに折り畳むと、頂点は3つのキューブが重なった状態、それ以外の辺は2個のキューブが重なった状態になる。

# 折り畳んだ大きさはs x s x sだけど、面倒くさいので折り畳みつつ縮小して、1x1x1に詰め込む事を考え、
# 縦横高さ1の立方体の点の座標→その頂点を含むキューブのlist、というdictを作りたい。
nodes = {}
for x in (0, 1):
	for y in (0, 1):
		for z in (0, 1):
			nodes[(x, y, z)] = []

# 折り畳んだ後の各面の各辺について、その辺の(始点キューブ, 終点キューブ): その辺から出る方向を示す平面上のベクトル、というdictを作りたい。
edges = {}

# 移動の初期キューブと同じ所を探索のスタートにする。
y = 0
for i in range(len(grid[0])):
	if grid[0][i] == ".":
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
	vs = [(x, y), (x + s - 1, y), (x + s - 1, y + s - 1), (x, y + s - 1)]
	
	# 現在の面の4隅を、空間座標→キューブ、のdictに追加
	nodes[p             ].append(vs[0])
	nodes[add(p, vx)    ].append(vs[1])
	nodes[add(p, vy, vx)].append(vs[2])
	nodes[add(p, vy)    ].append(vs[3])
	
	# 現在の面の4辺を、辺→その辺から出る方向のベクトル、のdictに追加
	dx = 0
	dy = -1
	for i in range(4):
		v1 = vs[i]
		v2 = vs[(i + 1) % 4]
		edges[(v1, v2)] = (dx, dy)
		edges[(v2, v1)] = (dx, dy)
		# (dx, dy)を右90度回転
		dx, dy = -dy, dx
	
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

# ここまで正しければ、全ての座標上の点に3個ずつのキューブが登録されているはず
for l in nodes.values():
	if len(l) != 3:
		raise Exception()

#print(nodes)

#print("e")
#for x in edges.items():
#	print(x)

# キューブv1とキューブv2で結ばれた辺の間のキューブの座標のリスト(端点含む)を求める
def points(v1, v2):
	ret = []
	x, y = v1
	tx, ty = v2
	while True:
		ret.append((x, y))
		if tx == x and ty == y:
			break
		elif x < tx:
			x += 1
		elif x > tx:
			x -= 1
		elif y < ty:
			y += 1
		elif y > ty:
			y -= 1
		else:
			# 垂直が水平でない辺を求める事はあり得ないのでエラー
			raise Exception
	return ret

# 今(x, y)に居て、(dx, dy)方向に移動しようとしている、というときに、その移動は面の境界を越えて(nx, ny)に移動し向きは(ndx, ndy)になる、
# という場合に限って、その結びつきを、(x, y, dx, dy): ((nx, ny), (ndx, ndy))として記録しておくdictにする。
warps = {}

# warpに、キューブの辺e1→辺e2へワープできる、という情報を追加
def add_warps(e1, e2):
	# 移動元の辺、移動先の辺から出て行く場合のベクトルを取っておく
	fdx, fdy = edges[e1]
	tdx, tdy = edges[e2]
	
	# 辺上のキューブを列挙
	fps = points(*e1)
	tps = points(*e2)
	
	# 対応する各キューブ毎にワープを追加
	for (fx, fy), (tx, ty) in zip(fps, tps):
		# 移動元の辺から出て行くベクトル: 移動先の辺から出て行くベクトルの逆、を記録しておけば良い
		warps[(fx, fy, fdx, fdy)] = ((tx, ty), (-tdx, -tdy))


# 1x1x1立方体上の全ての辺について実行。
# まず、あらゆる異なる2点の組み合わせ全てをp1、p2として実行。
keys = list(nodes.keys())
for i in range(len(keys)):
	p1 = keys[i]
	for j in range(i + 1, len(keys)):
		p2 = keys[j]
		# p1とp2の距離が1なら辺(なんかもっと良い方法もありそうだけど手抜き)。
		if sum(abs(a - b) for a, b in zip(p1, p2)) == 1:
#			print(p1, p2)
			# 辺になってる平面上の頂点の組み合わせを記録するためのリスト
			es = []
			# p1に位置するキューブ、p2に位置するキューブ、の組み合わせを全列挙。
			for v1 in nodes[p1]:
				for v2 in nodes[p2]:
					# 2つのキューブの組みがedgesに含まれるなら、同じ面上のキューブの組で正しい辺。
					# (そうでない場合は、上面のキューブと手前面のキューブ、とか異なる面上のキューブの組みになっているはず)
					# (もっと正しい探索方法があるような気がする。辺から探索して対応する辺を探すとか?)
					if (v1, v2) in edges:
						es.append((v1, v2))
			# 上手くいっていれば、1x1x1立方体上の各辺について、平面上の辺2個ずつがヒットしてるはず。
			if len(es) == 2:
				e1, e2 = es
				# 2つの辺は互いに行き来できるのでワープを記録
				add_warps(e1, e2)
				add_warps(e2, e1)
			else:
				raise Exception


for l in warps.items():
	print(l)

print(x, y)

# (x, y)から、(dx, dy)だけ動くとどこへ行くかを返す。詰まってて移動出来ないときはNone
def move(x, y, dx, dy):
	print((x, y), (dx, dy))
	if (x, y, dx, dy) in warps:
		# warpsのテーブルにある状況の時はワープする
#		print("wf", (x, y))
		(x, y), (dx, dy) = warps[(x, y, dx, dy)]
#		print("wt", (x, y))
	elif dy == 0:
		# それ以外は普通に移動
		x += dx
	else:
		y += dy
	# ここまでの仕組み上、はみ出る場合は必ずwarpしてるので座標のチェックなどは不要
	if grid[y][x] == "#":
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
			dx, dy = dy, -dx
		else:
			dx, dy = -dy, dx
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
