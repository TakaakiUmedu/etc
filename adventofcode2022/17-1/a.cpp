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

class grid{
	vector<uint8_t> field;
	int x;
public:
	grid(): x(0){}
	void add_line(const string& s){
		uint8_t l = 0;
		int i = 0;
		for(const auto c: s){
			if(c == '#'){
				l |= 1 << i;
			}
			i ++;
		}
		field.insert(field.begin(), l);
	}
	size_t height(){
		return field.size();
	}
	grid move_left() const{
		grid ret;
		for(const auto v: field){
			if((v & 1) != 0){
				return ret;
			}
		}
		for(auto& v: field){
			ret.field.push_back(v >> 1);
		}
		ret.x = x - 1;
		return ret;
	}
	grid move_right() const{
		grid ret;
		for(const auto v: field){
			if((v & (1 << 6)) != 0){
				return ret;
			}
		}
		for(auto& v: field){
			ret.field.push_back(v << 1);
		}
		ret.x = x + 1;
		return ret;
	}
	void print() const{
		for(const auto j: range(field.size() - 1, -1, -1)){
			const auto v = field[j];
			for(const auto i: range(7)){
				cout << ((v & (1 << i)) == 0 ? '.' : '#');
			}
			cout << endl;
		}
	}
	bool check(const grid& g, int offset) const{
		for(const auto j: range(g.field.size() - 1, -1, -1)){
			const auto i = j + offset;
			if(i >= 0 && i < field.size()){
				const auto l1 = field[i];
				const auto l2 = g.field[j];
				if((l1 & l2) != 0){
					return false;
				}
			}
		}
		return true;
	}
	void copy(const grid& g, int offset){
		for(const auto j: range(g.field.size() - 1, -1, -1)){
			const auto i = j + offset;
			while(i >= field.size()){
				field.push_back(0);
			}
			field[i] |= g.field[j];
		}
	}
	bool valid() const{
		return field.size() > 0;
	}
};

int main(void){
	vector<grid> blocks;
	{
		grid b0, b1, b2, b3, b4;
		b0.add_line("..####.");
		blocks.push_back(move(b0));
		
		b1.add_line("...#...");
		b1.add_line("..###..");
		b1.add_line("...#...");
		blocks.push_back(move(b1));
		
		b2.add_line("....#..");
		b2.add_line("....#..");
		b2.add_line("..###..");
		blocks.push_back(move(b2));
		
		b3.add_line("..#...");
		b3.add_line("..#...");
		b3.add_line("..#...");
		b3.add_line("..#...");
		blocks.push_back(move(b3));
		
		b4.add_line("..##...");
		b4.add_line("..##...");
		blocks.push_back(move(b4));
	}
	
	for(const auto& b: blocks){
		b.print();
		cout << endl;
	}
//	return 1;
	grid field;
	field.add_line("#######");
//	field.add_line("");
//	field.add_line("");
	
	const auto N = read<int64_t>();
	const auto moves = read<string>();
	int j = 0;
	int k = 0;
	
	for(const auto i: range(N)){
//		print(i);
		grid b = blocks[k % blocks.size()];
		k ++;
//		if(k >= blocks.size()){
//			k = 0;
//		}
		int offset = field.height() + 3;
		while(true){
			const auto m = moves[j % moves.size()];
			j ++;
//			if(j >= moves.size()){
//				j = 0;
//			}
			const auto nb = m == '<' ? b.move_left() : b.move_right();
			if(nb.valid() && field.check(nb, offset)){
				b = move(nb);
			}
			if(field.check(b, offset - 1)){
				offset --;
			}else{
				field.copy(b, offset);
				break;
			}
		}
	}
	field.print();
	
	cout << field.height() - 1 << endl;
/*
	const auto N = read<int64_t>();
	const auto [N, M] = read_tuple<int64_t, int64_t>();
	for(auto i: range(N)){
		auto [A, B, C] = read_tuple<int64_t, int64_t, int64_t>();
	}
	auto S_vec = read_vec<int64_t>(N);
*/
	
	return 0;
}
