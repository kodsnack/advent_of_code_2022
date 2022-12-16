package main

import (
	_ "embed"
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

func main() {
	input = strings.TrimSpace(input)

	type valve struct {
		flowRate  int
		connected []string
	}
	valves := make(map[string]valve)

	for _, row := range strings.Split(input, "\n") {
		parts := strings.Split(row, " ")
		name := parts[1]
		flowRate := intsInString(row)[0]
		valv := strings.Split(row, "to")
		aa := strings.TrimPrefix(valv[1], " valves ")
		aa = strings.TrimPrefix(aa, " valve ")
		vv := strings.Split(aa, ", ")
		valves[name] = valve{flowRate, vv}
	}

	openValveIdx := make(map[string]int)
	idx := 0
	for k, v := range valves {
		if v.flowRate > 0 {
			openValveIdx[k] = idx
			idx++
		}
	}
	type qi struct {
		open    [16]bool
		ats     [2]string
		minute  int
		flow    int
		sumflow int
	}

	open := [16]bool{}
	for k := range valves {
		if valves[k].flowRate > 0 {
			open[openValveIdx[k]] = true
		}
	}

	Q := []qi{{ats: [2]string{"AA", "AA"}, minute: 1}}

	var largestFlow int
	var maxminute = 0

	seen := make(map[string]map[[16]bool]int)

	withFlowCount := 0
	for _, v := range valves {
		if v.flowRate > 0 {
			withFlowCount++
		}
	}

nextQ:
	for {
		if len(Q) == 0 {
			break
		}
		q := Q[0]
		Q = Q[1:]

		if q.minute > maxminute {
			fmt.Println("minute", q.minute, len(Q))
			maxminute = q.minute
		}

		if q.minute > 26 {
			largestFlow = max(largestFlow, q.sumflow)
			continue
		}

		at := q.ats[0] + "-" + q.ats[1]
		if seens, ok := seen[at]; !ok {
			seen[at] = make(map[[16]bool]int)
		} else {
			for k, v := range seens {
				if v >= q.sumflow {
					if isSubset(q.open, k) {
						continue nextQ
					}
				}
			}
		}

		seen[at][q.open] = q.sumflow

		openCount := 0
		for _, v := range q.open {
			if v {
				openCount++
			}
		}

		allOpen := openCount == withFlowCount

		type cando struct {
			at      string
			newOpen string
			addFlow int
		}

		var candos [2][]cando

		for idx := range [2]int{0, 1} {
			var moves []cando

			at := q.ats[idx]
			atOpen := q.open[openValveIdx[at]]

			// stay
			moves = append(moves, cando{at: at})
			candos[idx] = moves

			// move only if we can gain something
			if !allOpen {
				// open valve
				if !atOpen && valves[at].flowRate > 0 {
					moves = append(moves, cando{
						at:      at,
						newOpen: at,
						addFlow: valves[at].flowRate,
					})
				}
				// go to connected
				if atOpen || valves[at].flowRate == 0 {
					for _, v := range valves[at].connected {
						moves = append(moves, cando{at: v})
					}
				}
			}

			candos[idx] = moves
		}

		// all combos
		for _, you := range candos[0] {
			for _, ele := range candos[1] {
				if you.newOpen != "" && you.newOpen == ele.newOpen {
					continue
				}
				open := q.open
				if you.newOpen != "" {
					open[openValveIdx[you.newOpen]] = true
				}
				if ele.newOpen != "" {
					open[openValveIdx[ele.newOpen]] = true
				}

				// sort ats ===== speed
				var at [2]string
				if you.at < ele.at {
					at = [2]string{you.at, ele.at}
				} else {
					at = [2]string{ele.at, you.at}
				}

				Q = append(Q, qi{
					ats:     at,
					minute:  q.minute + 1,
					flow:    q.flow + you.addFlow + ele.addFlow,
					sumflow: q.sumflow + q.flow,
					open:    open,
				})
			}
		}
	}

	fmt.Println(largestFlow)
}

// if all values in a are set in b
func isSubset(a, b [16]bool) bool {
	for k, v := range a {
		if v && !b[k] {
			return false
		}
	}
	return true
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func intsInString(s string) []int {
	re := regexp.MustCompile(`-?\d+`)
	matches := re.FindAllString(s, -1)
	res := make([]int, len(matches))
	for i, m := range matches {
		res[i], _ = strconv.Atoi(m)
	}
	return res
}
