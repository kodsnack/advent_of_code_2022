#include <iostream>

constexpr int kachi[3][3] = { { 3, 0, 6 }, { 6, 3, 0 }, { 0, 6, 3 } };
int ans = 0;

int main() {
    {
        std::string line;
        while (std::getline(std::cin, line))
            ans += kachi[line[2] - 'X'][line[0] - 'A'] + line[2] - 'W';
    }
    std::cout << ans << std::endl;
    return 0;
}