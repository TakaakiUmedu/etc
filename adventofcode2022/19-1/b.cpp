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

template<typename T, typename V, typename... R> class composer{
	const composer<T, R...> next;
	const V m;
public:
	composer(V max, R... r): m(max), next(r...){}
	inline T compose(V value, R... r) const{
		return value + next.compose(r...) * m;
	}
	inline auto decompose(T value) const{
		return std::tuple_cat(std::make_tuple(value % m), next.decompose(value / m));
	}
	inline T max() const{
		return m * next.max();
	}
};

template<typename T, typename V> class composer<T, V>{
	const V m;
public:
	composer(V max): m(max){}
	inline T compose(V value) const{
		return value;
	}
	inline auto decompose(T value) const{
		return std::make_tuple(value);
	}
	inline T max() const{
		return m;
	}
};

inline tuple<int64_t, int64_t, int64_t, int64_t> add(const tuple<int64_t, int64_t, int64_t, int64_t>& a, const tuple<int64_t, int64_t, int64_t, int64_t>& b){
	return make_tuple(get<0>(a) + get<0>(b), get<1>(a) + get<1>(b), get<2>(a) + get<2>(b), get<3>(a) + get<3>(b));
}

inline tuple<int64_t, int64_t, int64_t, int64_t> sub(const tuple<int64_t, int64_t, int64_t, int64_t>& a, const tuple<int64_t, int64_t, int64_t, int64_t>& b){
	return make_tuple(get<0>(a) - get<0>(b), get<1>(a) - get<1>(b), get<2>(a) - get<2>(b), get<3>(a) - get<3>(b));
}

int main(void){
	const auto N = read<int64_t>();
	
	vector<vector<tuple<tuple<int64_t, int64_t, int64_t, int64_t>, int64_t>>> blueprint_table;
	for(auto i: range(N)){
		vector<tuple<tuple<int64_t, int64_t, int64_t, int64_t>, int64_t>> blueprints;
		auto n = read<int64_t>();
		for(auto j: range(n)){
			auto S_tuple = read_tuple<int64_t, int64_t, int64_t, int64_t>();
			auto d = read<int64_t>();
			blueprints.push_back({S_tuple, d});
		}
		blueprint_table.push_back(blueprints);
	}
	
	const composer<int32_t, int64_t, int64_t, int64_t, int64_t> composer1(25, 25, 25, 25);
	const composer<int64_t, int64_t, int64_t, int64_t, int64_t> composer2(1000, 1000, 1000, 1000);
	
	int64_t total = 0;
	int64_t t = 1;
	for(const auto& blueprint: blueprint_table){
		set<tuple<int32_t, int64_t>> states;
		states.insert({composer1.compose(1, 0, 0, 0), 0});
		for(const auto i: range(24)){
			set<tuple<int32_t, int64_t>> new_states;
			cout << "[" << i << "]: " << states.size() << endl;
			for(const auto& [robots, items]: states){
				const auto rt = composer1.decompose(robots);
				const auto it = composer2.decompose(items);
//				print(rt, it);
				const auto new_it = add(it, rt);
				new_states.insert(make_tuple(robots, composer2.compose(get<0>(new_it), get<1>(new_it), get<2>(new_it), get<3>(new_it))));
				for(const auto& [recepie, d]: blueprint){
					const auto new_it2 = sub(it, recepie);
					if(get<0>(new_it2) >= 0 && get<1>(new_it2) >= 0 && get<2>(new_it2) >= 0 && get<3>(new_it2) >= 0){
						const auto new_it3 = add(new_it2, rt);
						auto new_rt = rt;
						if(d == 0){
							get<0>(new_rt) ++;
						}else if(d == 1){
							get<1>(new_rt) ++;
						}else if(d == 2){
							get<2>(new_rt) ++;
						}else{
							get<3>(new_rt) ++;
						}
						new_states.insert(make_tuple(composer1.compose(get<0>(new_rt), get<1>(new_rt), get<2>(new_rt), get<3>(new_rt)), composer2.compose(get<0>(new_it3), get<1>(new_it3), get<2>(new_it3), get<3>(new_it3))));
					}
				}
			}
			
			states = move(new_states);
		}
		int64_t m = 0;
		for(const auto& [robots, items]: states){
			const auto it = composer2.decompose(items);
			m = max(m, get<3>(it));
		}
		cout << m << endl;
		total += m * t;
		t ++;
	}
	cout << total << endl;
	return 0;
}
