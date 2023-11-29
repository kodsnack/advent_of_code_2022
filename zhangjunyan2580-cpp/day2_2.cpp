#include <iostream>

int ans = 0;

int main() {
    {
        std::string line;
        while (std::getline(std::cin, line))
            ans += (line[0] - 'A' + line[2] - 'V') % 3 + (line[2] - 'X') * 3 + 1;
    }
    std::cout << ans << std::endl;
    return 0;
}