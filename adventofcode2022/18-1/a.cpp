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
	const auto N = read<int64_t>();
	
	vector<tuple<int64_t, int64_t, int64_t>> data;
	int64_t max_x = 0, max_y = 0, max_z = 0;
	for(auto i: range(N)){
		auto [x, y, z] = read_tuple<int64_t, int64_t, int64_t>();
		max_x = max(max_x, x);
		max_y = max(max_y, y);
		max_z = max(max_z, z);
		data.push_back({x, y, z});
	}
	
	vector<vector<vector<bool>>> grid(max_x + 2, vector<vector<bool>>(max_y + 2, vector<bool>(max_z + 2, false)));
	
	for(const auto& [x, y, z]: data){
		grid[x][y][z] = true;
	}
	
	int64_t total = data.size() * 6;
	
	for(const auto x: range(max_x + 1)){
		for(const auto y: range(max_y + 1)){
			for(const auto z: range(max_z + 1)){
				if(grid[x][y][z]){
					if(grid[x + 1][y][z]){
						total -= 2;
					}
					if(grid[x][y + 1][z]){
						total -= 2;
					}
					if(grid[x][y][z + 1]){
						total -= 2;
					}
				}
			}
		}
	}
	
	cout << total << endl;
	
	return 0;
}
