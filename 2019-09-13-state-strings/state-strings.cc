#include <fstream>
#include <iostream>
#include <memory>
#include <sstream>
#include <vector>

struct Node {
    Node(const std::string& abbrv) : abbrv(abbrv) {}

    std::string abbrv;
    std::vector<size_t> succs;
};

auto load_abbrvs(const std::string& filename) {
    std::vector<std::string> result;

    std::ifstream file(filename);
    for (std::string line; std::getline(file, line);) {
        result.push_back(line);
    }

    return result;
}

struct Graph {
    Graph(const std::vector<std::string>& abbrvs) {
        for (const auto& s : abbrvs) {
            nodes.emplace_back(s);
            all_index_list.push_back(all_index_list.size());
        }

        for (auto& curr : nodes) {
            for (size_t next_i = 0; next_i < nodes.size(); next_i++) {
                const auto next = nodes.at(next_i);

                if (curr.abbrv == next.abbrv) continue;

                if (curr.abbrv.at(1) == next.abbrv.at(0)) {
                    curr.succs.emplace_back(next_i);
                }
            }
        }
    }

    size_t max_path();
    size_t max_path(std::vector<size_t>& prefix,
                    std::vector<bool>& closed,
                    const size_t curr_best);

    std::string print(const std::vector<size_t>& path) {
        std::ostringstream ss;
        if (path.size() != 0) ss << nodes[path.front()].abbrv.at(0);
        for (const size_t i : path) {
            ss << nodes[i].abbrv.at(1);
        }
        return ss.str();
    }

    std::vector<Node> nodes;
    std::vector<size_t> all_index_list;
};

size_t Graph::max_path() {
    std::vector<size_t> path;
    std::vector<bool> closed(nodes.size(), false);
    return max_path(path, closed, 0);
}

size_t Graph::max_path(std::vector<size_t>& prefix,
                       std::vector<bool>& closed,
                       const size_t curr_best) {
    // std::cout << "ENTERING!!!!!!!!!!!!!!!!" << std::endl;
    // std::cout << "Prefix: " << print(prefix) << std::endl;
    // std::cout << "curr_best: " << curr_best << std::endl;

    size_t best = prefix.size();

    // std::cout << "best: " << best << std::endl;

    const auto& index_list =
            prefix.size() == 0 ? all_index_list : nodes[prefix.back()].succs;

    for (const size_t j : index_list) {
        // std::cout << "Considering " << j << std::endl;
        if (closed[j]) continue;
        // std::cout << "Accepted" << std::endl;

        prefix.push_back(j);
        closed[j] = true;
        const auto new_path_len =
                max_path(prefix, closed, std::max(best, curr_best));
        // std::cout << "new_path_len: " << new_path_len << std::endl;
        if (new_path_len > curr_best && new_path_len > best) {
            best = new_path_len;

            if (best == prefix.size()) {
                std::cout << "updated best: " << best << std::endl;
                std::cout << print(prefix) << std::endl;
            }
        }
        prefix.pop_back();
        closed[j] = false;
    }

    // std::cout << "RETURNING!!!!!!!!!!!!!!!!" << best << std::endl;
    return best;
}

int main() {
    Graph g(load_abbrvs("abbrevs.txt"));
    std::cout << g.max_path() << std::endl;
}
