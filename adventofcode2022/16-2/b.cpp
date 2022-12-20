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

int main(void){
	const auto [N, M, Tt, S] = read_tuple<int64_t, int64_t, int64_t, int64_t>();
	const auto T = Tt - 4;
	auto flows = read_vec<int64_t>(M);

	vector<vector<int64_t>> graph;
	for(auto i: range(N)){
		const auto n = read<int64_t>();
		graph.push_back(read_vec<int64_t>(n));
	}
	
	const auto to_int = [N, M, T](int64_t v1, int64_t v2, int64_t t, int64_t s){
		if(v1 > v2){
			swap(v1, v2);
		}
		return (((s * T) + t) * N + v1) * N + v2;
	};
	
	const auto to_values = [N, M, T](int64_t x){
		const auto v2 = x % N;
		x /= N;
		const auto v1 = x % N;
		x /= N;
		const auto t = x % T;
		x /= T;
		return make_tuple(v1, v2, t, x);
	};
	
	const auto open = [M](int64_t v, int64_t s){
		if(v < M && (s & (1 << v)) == 0){
			return s | (1 << v);
		}else{
			return 0L;
		}
	};
	
	vector<int64_t> amounts((1 << M) * T * N * N, -1);
	vector<tuple<int64_t, int64_t>> queue;
	
	const auto push = [&amounts, &queue, &to_int](int64_t v1, int64_t v2, int64_t s, int64_t t, int64_t a){
		const auto x = to_int(v1, v2, s, t);
		if(x >= amounts.size()){
			print("error", x, v1, v2, s, t);
			exit(0);
		}
		if(amounts[x] == -1 || amounts[x] < a){
			amounts[x] = a;
			queue.push_back({a, x});
			push_heap(queue.begin(), queue.end());
		}
	};
	
	push(S, S, 0, 0, 0);
	print(amounts.size());
	
	while(queue.size() > 0){
		pop_heap(queue.begin(), queue.end());
		const auto [a, v] = *queue.rbegin();
		queue.pop_back();
		if(amounts[v] != a){
			continue;
		}
		const auto [v1, v2, t, s] = to_values(v);
		const auto t1 = t + 1;
		if(t1 >= T){
			continue;
		}
		{
			const auto s1 = open(v1, s);
			if(s1 != 0){
				const auto a1 = a + (T - t1) * flows[v1];
				push(v1, v2, t1, s1, a1);
				for(const auto n: graph[v2]){
					push(v1, n, t1, s1, a1);
				}
				const auto s3 = open(v2, s1);
				if(s3 != 0){
					const auto a3 = a1 + (T - t1) * flows[v2];
					push(v1, v2, t1, s3, a3);
				}
			}
		}
		{
			const auto s2 = open(v2, s);
			if(s2 != 0){
				const auto a2 = a + (T - t1) * flows[v2];
				for(const auto n: graph[v1]){
					push(n, v2, t1, s2, a2);
				}
			}
		}
		for(const auto n1: graph[v1]){
			for(const auto n2: graph[v2]){
				push(n1, n2, t1, s, a);
			}
		}
	}
	
	int64_t top_value = 0;
	for(const auto v: amounts){
		if(v >= 0){
			top_value = max(top_value, v);
		}
	}
	print(top_value);
	
	return 0;
}
