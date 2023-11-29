#include "pystrlib.hpp"
#include <iostream>
#include <vector>
#include <stack>

std::string S[20];
int c;

int main() {
    {
        std::vector<std::string> lines;
        std::string line;
        while (std::getline(std::cin, line)) {
            if (line[1] == '1') break;
            else lines.push_back(line);
        }
        c = lib::rstrip(line).back() & 15;
        for (auto it = lines.rbegin(); it != lines.rend(); ++it)
            for (int i = 0; i < c; ++i)
                if (i * 4 + 1 < (int) it->size() && it->at(i * 4 + 1) != ' ')
                    S[i].push_back(it->at(i * 4 + 1));
        std::getline(std::cin, line);
    }
    {
        std::string line;
        while (std::getline(std::cin, line)) {
            std::vector<std::string> p = lib::split(line, " ");
            int f = std::stoi(p[3]) - 1, t = std::stoi(p[5]) - 1, c = std::stoi(p[1]);
            S[t] += S[f].substr(S[f].size() - c), S[f] = S[f].substr(0, S[f].size() - c);
        }
    }
    for (int i = 0; i < c; ++i) putchar(S[i].back());
    return 0;
}