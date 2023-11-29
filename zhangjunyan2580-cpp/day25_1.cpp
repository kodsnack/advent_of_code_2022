#include <iostream>

std::string line;
long long sum = 0;
int w[105], l;

constexpr char ch[6] = { '0', '1', '2', '=', '-', '0' };

int main() {
    while (std::cin >> line) {
        long long n = 0;
        for (char ch : line) {
            int k;
            switch (ch) {
                case '=': k = -2; break;
                case '-': k = -1; break;
                case '0': k = 0; break;
                case '1': k = 1; break;
                case '2': k = 2; break;
            }
            n = n * 5 + k;
        }
        sum += n;
    }
    while (sum) w[l++] = sum % 5, sum /= 5;
    for (int i = 0; i < l; ++i)
        if (w[i] >= 3) { ++w[i + 1]; if (i == l - 1) ++l; }
    for (int i = l - 1; i >= 0; --i) std::cout << ch[w[i]];
    return 0;
}