//#include <atcoder/segtree>
//#include <atcoder/lazysegtree>
//#include <atcoder/fenwicktree>
//#include <atcoder/modint>
//#include <atcoder/dsu>

#include <map>
#include <set>
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
#include <tuple>
#include <limits>
#ifdef USE_PYTHON_LIKE_PRINT
// https://github.com/TakaakiUmedu/python_like_print
#include "print.hpp"
#else
template<char SEP = ' ', char END = '\n', class... A> inline void print(A&& ...){}
template<char SEP = ' ', char END = '\n', class... A> inline void printe(A&& ...){}
template<char SEP = ' ', char END = '\n', class... A> inline void printo(A&& ...){}
#define define_print(...)
#define define_print_with_names(...)
#define define_to_tuple(...)
#endif

using namespace std;

template<typename T = int> class range{
	class iter{
		T _v, _d;
	public:
		inline iter(T v, T d): _v(v), _d(d){}
		inline iter operator ++(){ _v += _d; return *this; }
		inline iter operator ++(int){ const auto v = _v; _v += _d; return iter(v, _d); }
		inline operator T() const{ return _v; }
		inline T operator*() const{ return _v; }
		inline bool operator!=(T e) const{ return _d == 0 ? _v != e : (_d >= 0 ? _v < e : _v > e); }
	};
	const iter _i; const T _e;
public:
	template<typename S = int> inline range(S s, T e, T d = 1): _i(s, d), _e(e){}
	inline range(T e): range(0, e){}
	inline iter begin() const{ return _i; }
	inline T end() const{ return _e; }
};

template<typename T, typename B = decltype(declval<T>().rbegin()), typename E = decltype(declval<T>().rend())> class reversed{
	T& _c;
public:
	reversed(T& c): _c(c){}
	auto begin(){ return _c.rbegin(); }
	auto end(){ return _c.rend(); }
};

template<typename T> inline T read_int(){
	conditional_t<is_signed_v<T>, int64_t, uint64_t> v; cin >> v;
	if(numeric_limits<T>::max() < v || numeric_limits<T>::min() > v){ throw runtime_error("overflow occured in read_int"); }
	return static_cast<T>(v);
}
template<typename T> inline T read(){ if constexpr(is_integral_v<T>){ return read_int<T>(); }else{ T v; cin >> v; return v; } }
template<size_t N, typename... T> inline void read_tuple_elem(tuple<T...>& v){
	if constexpr(N < sizeof...(T)){ get<N, T...>(v) = read<std::tuple_element_t<N, tuple<T...>>>(); read_tuple_elem<N + 1, T...>(v); }
}
template<typename... T> inline tuple<T...> read_tuple(){ tuple<T...> v; read_tuple_elem<0, T...>(v); return v; }
template<typename T> inline vector<T> read_vec(size_t N){ vector<T> values(N); for(const auto i: range(N)) cin >> values[i]; return values; }

template<typename V> inline auto compose(V value){
	return value;
}

template<typename V, typename... R> inline auto compose(V value, V max, R... r...){
	return compose(r...) * max + value;
}

template<typename T> inline auto decompose(T value){
	return make_tuple(value);
}

template<typename T, typename... R> inline auto decompose(T value, T max, R... r...){
	return tuple_cat(make_tuple(value % max), decompose(value / max, r...));
}

inline auto open(int32_t M, int32_t v, int32_t s){
	if(v < M && (s & (1 << v)) == 0){
		return s | (1 << v);
	}else{
		return 0;
	}
}

inline auto update(int32_t N, int32_t M, vector<int32_t>& flows_tmp, int32_t &best, int32_t T, vector<int32_t>& queue, vector<int32_t>& amounts, int32_t v1, int32_t v2, int32_t s, int32_t a, int32_t t){
	if(v1 > v2){
		swap(v1, v2);
	}
	const auto x = compose(v1, N, v2, N, s);
//	if(x >= amounts.size()){
//		print("e", x, amounts.size(), v1, v2, s);
//		exit(1);
//	}
	if(amounts[x] < a){
		const auto b = a + (T - t) * flows_tmp[s];
		if(b >= best){
			amounts[x] = a;
			queue.push_back(x);
//				push_heap(queue.begin(), queue.end());
			if(a > best){
				best = a;
			}
		}
	}
};




int main(void){
	const auto [N, M, Tt, S] = read_tuple<int32_t, int32_t, int32_t, int32_t>();
	const auto T = Tt - 4;
	auto flows = read_vec<int32_t>(M);

	vector<vector<int32_t>> graph;
	for(auto i: range(N)){
		const auto n = read<int32_t>();
		graph.push_back(read_vec<int32_t>(n));
	}
	
	int32_t best = 0;
	
	vector<int32_t> flows_tmp;
	for(const auto i: range(1 << M)){
		int32_t f = 0;
		for(const auto j: range(M)){
			if((i & (1 << j)) == 0){
				f += flows[j];
			}
		}
		flows_tmp.push_back(f);
	}
//	print(flows_tmp);


	vector<int32_t> amounts((1 << M) * N * N, -1);
	vector<int32_t> queue;
	update(N, M, flows_tmp, best, T, queue, amounts, S, S, 0, 0, 0);
	
	for(const auto t: range(T)){
		print(t);
		vector<int32_t> amounts_tmp((1 << M) * N * N, -1);
		vector<int32_t> queue_tmp;
		for(const auto& x: queue){
			const auto& [v1, v2, s] = decompose(x, N, N);
			const auto a = amounts[x];
			{
				const auto s1 = open(M, v1, s);
				if(s1 != 0){
					const auto a1 = a + (T - t - 1) * flows[v1];
					for(const auto n: graph[v2]){
						update(N, M, flows_tmp, best, T, queue_tmp, amounts_tmp, v1, n, s1, a1, t + 1);
					}
					const auto s3 = open(M, v2, s1);
					if(s3 != 0){
						const auto a3 = a1 + (T - t - 1) * flows[v2];
						update(N, M, flows_tmp, best, T, queue_tmp, amounts_tmp, v1, v2, s3, a3, t + 1);
					}else{
						update(N, M, flows_tmp, best, T, queue_tmp, amounts_tmp, v1, v2, s1, a1, t + 1);
					}
				}
			}
			{
				const auto s2 = open(M, v2, s);
				if(s2 != 0){
					const auto a2 = a + (T - t - 1) * flows[v2];
					for(const auto n: graph[v1]){
						update(N, M, flows_tmp, best, T, queue_tmp, amounts_tmp, n, v2, s2, a2, t + 1);
					}
				}
			}
			for(const auto n1: graph[v1]){
				for(const auto n2: graph[v2]){
					update(N, M, flows_tmp, best, T, queue_tmp, amounts_tmp, n1, n2, s, a, t + 1);
				}
			}
		}
		amounts = move(amounts_tmp);
		queue = move(queue_tmp);
	}
	
/*	
	
	push(S, S, 0, 0, 0);
*/	
	
	int32_t top_value = 0;
	for(const auto v: amounts){
		if(v >= 0){
			top_value = max(top_value, v);
		}
	}
	print(top_value);

//	print(best);
	
	return 0;
}
