#include <iostream>

int b[256], c;
std::string str;

inline void push(char ch) { !b[ch]++ && ++c; }
inline void pop(char ch) { !--b[ch] && --c; }

int main() {
    std::cin >> str;
    push(str[0]); push(str[1]); push(str[2]);
    for (int i = 3; i < (int) str.size(); ++i) {
        push(str[i]);
        if (c == 4) { std::cout << i + 1 << std::endl; return 0; }
        pop(str[i - 3]);
    }
    return 0;
}