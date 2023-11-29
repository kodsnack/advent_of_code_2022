#include <iostream>

int total, maxv;
std::string line;

int main() {
    while (std::getline(std::cin, line)) {
        if (line == "") {
            if (total > maxv) maxv = total;
            total = 0;
        } else total += std::stoi(line);
    }
    std::cout << maxv << std::endl;
}