#include <iostream>

int total, maxv1, maxv2, maxv3;
std::string line;

int main() {
    while (std::getline(std::cin, line)) {
        if (line == "") {
            if (total > maxv1) maxv3 = maxv2, maxv2 = maxv1, maxv1 = total;
            else if (total > maxv2) maxv3 = maxv2, maxv2 = total;
            else if (total > maxv3) maxv3 = total;
            total = 0;
        } else total += std::stoi(line);
    }
    std::cout << maxv1 + maxv2 + maxv3 << std::endl;
}