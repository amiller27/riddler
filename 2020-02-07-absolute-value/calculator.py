def branch(s, n_open):
    if '|' not in s: return {eval(s)}

    results = set()
    if n_open > 0: results.update(branch(s.replace('|', ')', 1), n_open - 1))
    if n_open < s.count('|'): results.update(branch(s.replace('|', 'abs(' if s[0] == '|' else '*abs(', 1), n_open + 1))

    return results

print(len(branch('|-1|-2|-3|-4|-5|-6|-7|-8|-9|', 0)))
