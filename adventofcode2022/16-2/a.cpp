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

inline auto open(int32_t M, int32_t v, int32_t s){
	if(v < M && (s & (1 << v)) == 0){
		return s | (1 << v);
	}else{
		return 0;
	}
}

inline auto update(vector<int32_t>& amounts, int32_t x, int32_t a){
	if(amounts[x] < a){
		amounts[x] = a;
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
	
	vector<int32_t> amounts(N * (1 << M), -1);
	update(amounts, S + 0 * N, 0);
	
	for(const auto t: range(T)){
		print(t);
		vector<int32_t> amounts_tmp(N * (1 << M), -1);
		for(const auto v: range(N)){
			for(const auto s: range(1 << M)){
				const auto a = amounts[v + s * N];
				if(a >= 0){
					for(const auto n: graph[v]){
						update(amounts_tmp, n + s * N, a);
					}
					const auto s1 = open(M, v, s);
					if(s1 != 0){
						const auto a1 = a + (T - t - 1) * flows[v];
						update(amounts_tmp, v + s1 * N, a1);
					}
				}
			}
		}
		amounts = move(amounts_tmp);
	}
	
	vector<int32_t> amounts_folded(1 << M, -1);
	
	for(const auto s: range(1 << M)){
		for(const auto v: range(N)){
			amounts_folded[s] = max(amounts_folded[s], v + s * N);
		}
	}
	
	vector<int32_t> amounts_sum((1 << M), -1);

	for(const auto s1: range(1 << M)){
		int32_t a = amounts_folded[s1];
		for(auto s2 = s1; s2 != 0; s2 = (s2 - 1) & s1){
			a = max(a, amounts_folded[s2]);
		}
		amounts_sum[s1] = a;
	}
	
	int32_t top_value = 0;
	for(const auto s1: range(1 << M)){
		const auto a1 = amounts_folded[s1];
		if(a1 >= 0){
			const auto s2 = ((1 << M) - 1) ^ s1;
			const auto a2 = amounts_sum[s2];
			if(a2 >= 0){
				top_value = max(top_value, a1 + a2);
			}
		}
	}
	print(top_value);
	
	return 0;
}
