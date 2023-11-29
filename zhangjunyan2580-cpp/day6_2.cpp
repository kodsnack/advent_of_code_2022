#include <iostream>

int b[256], c;
std::string str;

inline void push(char ch) { !b[ch]++ && ++c; }
inline void pop(char ch) { !--b[ch] && --c; }

int main() {
    std::cin >> str;
    for (int i = 0; i < 13; ++i) push(str[i]);
    for (int i = 13; i < (int) str.size(); ++i) {
        push(str[i]);
        if (c == 14) { std::cout << i + 1 << std::endl; return 0; }
        pop(str[i - 13]);
    }
    return 0;
}