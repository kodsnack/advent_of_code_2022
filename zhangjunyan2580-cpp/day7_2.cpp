#include <iostream>
#include <unordered_map>
#include "pystrlib.hpp"

struct Node {
    std::unordered_map<std::string, int> son;
    int size, p;
} tr[100000];

int now, cnt;

void new_node(int parent, std::string name, int size) {
    tr[parent].son[name] = ++cnt;
    tr[cnt].p = parent;
    tr[cnt].size = size;
}

int ans = 0x3f3f3f3f;

void dfs(int k) {
    if (tr[k].son.empty()) return;
    for (const auto &[x, y] : tr[k].son) dfs(y), tr[k].size += tr[y].size;
}

void dfs2(int k) {
    if (!tr[k].son.empty() && tr[1].size - tr[k].size <= 40000000 && tr[k].size < ans) ans = tr[k].size;
    for (const auto &[x, y] : tr[k].son) dfs2(y);
}

int main() {
    freopen("day7.txt", "r", stdin);
    now = 1; cnt = 1;
    {
        std::string line;
        while (std::getline(std::cin, line)) {
            std::vector<std::string> arg = lib::split(line, " ");
            if (arg[0] == "$") {
                if (arg[1] == "cd") {
                    if (arg[2] == "..") now = tr[now].p;
                    else if (arg[2] == "/") now = 1;
                    else now = tr[now].son[arg[2]];
                }
            } else {
                if (arg[0] == "dir") new_node(now, arg[1], 0);
                else new_node(now, arg[1], std::stoi(arg[0]));
            }
        }
    }
    dfs(1);
    dfs2(1);
    std::cout << ans << std::endl;
    return 0;
}