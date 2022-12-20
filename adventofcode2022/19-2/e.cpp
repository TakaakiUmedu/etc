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

inline tuple<int64_t, int64_t, int64_t, int64_t> add(const tuple<int64_t, int64_t, int64_t, int64_t>& a, const tuple<int64_t, int64_t, int64_t>& b){
	return make_tuple(get<0>(a) + get<0>(b), get<1>(a) + get<1>(b), get<2>(a) + get<2>(b), get<3>(a));
}

inline tuple<int64_t, int64_t, int64_t, int64_t> sub(const tuple<int64_t, int64_t, int64_t, int64_t>& a, const tuple<int64_t, int64_t, int64_t>& b){
	return make_tuple(get<0>(a) - get<0>(b), get<1>(a) - get<1>(b), get<2>(a) - get<2>(b), get<3>(a));
}

inline void insert(set<tuple<int16_t, int16_t, int16_t, int16_t>>& items, const tuple<int16_t, int16_t, int16_t, int16_t>& it){
	auto p = items.begin();
	while(p != items.end()){
		const auto it2 = *p;
		if(get<0>(it2) > get<0>(it)){
			break;
		}
		if(get<0>(it2) <= get<0>(it) && get<1>(it2) <= get<1>(it) && get<2>(it2) <= get<2>(it) && get<3>(it2) <= get<3>(it)){
			p = items.erase(p);
		}else{
			p ++;
		}
	}
	items.insert(it);
}

int main(void){
	const auto N = read<int64_t>();
	
//	const auto L = 24;
//	const auto X = 100;
	const auto L = 32;
	const auto X = 3;
	
	vector<vector<tuple<tuple<int64_t, int64_t, int64_t>, int64_t>>> blueprint_table;
	for(auto i: range(N)){
		if(i >= X){
			break;
		}
		vector<tuple<tuple<int64_t, int64_t, int64_t>, int64_t>> blueprints;
		auto n = read<int64_t>();
		for(auto j: range(n)){
			auto S_tuple = read_tuple<int64_t, int64_t, int64_t>();
			if(read<int64_t>() != 0){
				print("ERROR");
				return 1;
			}
			auto d = read<int64_t>();
			blueprints.push_back({S_tuple, d});
		}
		blueprint_table.push_back(blueprints);
	}
	
	int64_t total = 1;
	int64_t total2 = 0;
	int64_t t = 1;
	for(const auto& blueprint: blueprint_table){
		cout << "<" << t << ">" << endl;
		map<tuple<int8_t, int8_t, int8_t>, set<tuple<int16_t, int16_t, int16_t, int16_t>>> states;
		states[make_tuple(1, 0, 0)].insert(make_tuple(0, 0, 0, 0));
		for(const auto i: range(L)){
			map<tuple<int8_t, int8_t, int8_t>, set<tuple<int16_t, int16_t, int16_t, int16_t>>> new_states;
			cout << "[" << i << "]: " << states.size() << endl;
			for(const auto& [robots, items_list]: states){
				for(const auto& items: items_list){
	//					print(rt, it);
					const auto new_items = add(items, robots);
					insert(new_states[robots], new_items);
					if(i == L - 1){
						continue;
					}
					for(const auto& [recepie, d]: blueprint){
						const auto new_items2 = sub(items, recepie);
						if(get<0>(new_items2) >= 0 && get<1>(new_items2) >= 0 && get<2>(new_items2) >= 0 && get<3>(new_items2) >= 0){
							auto new_items3 = add(new_items2, robots);
//							int16_t geode = 0;
							auto new_robots = robots;
							if(d == 0){
								get<0>(new_robots) ++;
							}else if(d == 1){
								get<1>(new_robots) ++;
							}else if(d == 2){
								get<2>(new_robots) ++;
							}else{
								get<3>(new_items3) += L - i - 1;
//								get<3>(new_robots) ++;
							}
//							new_states.insert(make_tuple(composer1.compose(get<0>(new_rt), get<1>(new_rt), get<2>(new_rt), get<3>(new_rt)), composer2.compose(get<0>(new_it3), get<1>(new_it3), get<2>(new_it3), get<3>(new_it3))));
							insert(new_states[new_robots], new_items3);
						}
					}
				}
			}
			
			int16_t m = 0;
			for(const auto& [robots, items_list]: states){
				for(auto& items: items_list){
					m = max(m, static_cast<int16_t>(get<3>(items)));
				}
			}
//			int x = 0;
			for(auto& [robots, items_list]: states){
				auto p = items_list.begin();
				while(p != items_list.end()){
					const auto& items = *p;
					const auto m2 = static_cast<int16_t>(get<3>(items) + (L - i) * (L - i + 1) / 2);
					if(m2 < m){
						p = items_list.erase(p);
//						x ++;
					}else{
						p ++;
					}
				}
			}
//			print(x);
			
			states = move(new_states);
		}
		int16_t m = 0;
		for(const auto& [robots, items_list]: states){
			for(const auto& items: items_list){
				m = max(m, get<3>(items));
			}
		}
		cout << m << endl;
		total *= m;
		total2 += m * t;
		t ++;
	}
	cout << total << endl;
	cout << total2 << endl;
	return 0;
}
