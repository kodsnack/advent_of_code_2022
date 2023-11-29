#include <iostream>
#include <array>
#include "pystrlib.hpp"

struct Monkey {
    Monkey() = default;
    Monkey(Monkey &&) = default;
    std::vector<int> items;
    int update_op, update_value;
    int divisor, true_monkey, false_monkey;
};
std::vector<Monkey> monkeys;
std::vector<int> inspect_count;
int n;

#define ADD 0
#define SUB 1
#define MUL 2

inline void apply(int &v, int op, int value) {
    if (value == -1)
        switch (op) {
            case ADD: v <<= 1; break;
            case SUB: v = 0; break;
            case MUL: v *= v; break;
        }
    else
        switch (op) {
            case ADD: v += value; break;
            case SUB: v -= value; break;
            case MUL: v *= value; break;
        }
}

void round() {
    for (int i = 0; i < n; ++i) {
        Monkey &monkey = monkeys[i];
        inspect_count[i] += monkey.items.size();
        for (int &v : monkey.items) {
            apply(v, monkey.update_op, monkey.update_value); v /= 3;
            monkeys[(v % monkey.divisor) ? monkey.false_monkey : monkey.true_monkey].items.push_back(v);
        }
        monkey.items.clear();
    }
}

int main() {
    freopen("day11.txt", "r", stdin);
    {
        std::array<std::string, 6> monkey;
        std::string _;
        auto get = [](std::array<std::string, 6> &monkey) -> bool {
            bool result;
            for (int i = 0; i < 6; ++i) result = (bool) std::getline(std::cin, monkey[i]);
            return result;
        };
        while (get(monkey)) {
            Monkey c_monkey;
            std::vector<std::string> vec = lib::split(std::get<2>(lib::partition(monkey[1], ": ")), ", ");
            for (const std::string &str : vec) c_monkey.items.push_back(std::stoi(str));
            vec = lib::split(std::get<2>(lib::partition(monkey[2], " = ")), " ");
            c_monkey.update_op = vec[1] == "+" ? ADD :
                                 vec[1] == "-" ? SUB :
                                                 MUL;
            c_monkey.update_value = vec[2] == "old" ? -1 : std::stoi(vec[2]);
            c_monkey.divisor = std::stoi(std::get<2>(lib::partition(monkey[3], "by ")));
            c_monkey.true_monkey = std::stoi(std::get<2>(lib::partition(monkey[4], "monkey ")));
            c_monkey.false_monkey = std::stoi(std::get<2>(lib::partition(monkey[5], "monkey ")));
            std::getline(std::cin, _);
            monkeys.push_back(std::move(c_monkey));
        }
    }
    n = monkeys.size(); inspect_count.resize(n);
    for (int i = 0; i < 20; ++i) round();
    int m1 = 0, m2 = 0;
    for (int v : inspect_count)
        if (v > m1) m2 = m1, m1 = v;
        else if (v > m2) m2 = v;
    std::cout << m1 * m2 << std::endl;
    return 0;
}