package main

import (
	_ "embed"
	"fmt"
	"math"
	"regexp"
	"strconv"
	"strings"
	"time"
)

//go:embed input.txt
var input string

type valve struct {
	flowRate  int
	connected []string
}

func main() {
	input = strings.TrimSpace(input)

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

	t0 := time.Now()
	fmt.Println("part1", part1(valves, openValveIdx), time.Since(t0))
	fmt.Println("part2", part2(valves, openValveIdx), time.Since(t0))
}

type move struct {
	at      string
	newOpen string
	addFlow int
}

func moves(open uint16, at string, valves map[string]valve, openValveIdx map[string]int) []move {
	var res []move
	var allTrue uint16 = math.MaxUint16
	isOpen := open&(1<<openValveIdx[at]) > 0
	if open == allTrue {
		res = append(res, move{at: at})
	} else {
		if !isOpen && valves[at].flowRate > 0 {
			res = append(res, move{at, at, valves[at].flowRate})
		}
		if isOpen || valves[at].flowRate == 0 {
			for _, v := range valves[at].connected {
				res = append(res, move{at: v})
			}
		}
	}
	return res
}

func part1(valves map[string]valve, openValveIdx map[string]int) int {
	type qi struct {
		open    uint16
		at      string
		minute  int
		flow    int
		sumflow int
	}

	Q := []qi{{at: "AA", minute: 1}}
	var largestFlow int
	seen := make(map[string]map[uint16]int)

nextQ:
	for {
		if len(Q) == 0 {
			break
		}
		q := Q[0]
		Q = Q[1:]

		if q.minute > 30 {
			largestFlow = max(largestFlow, q.sumflow)
			continue
		}

		if seens, ok := seen[q.at]; !ok {
			seen[q.at] = make(map[uint16]int)
		} else {
			for k, v := range seens {
				if v >= q.sumflow {
					if k == q.open || k&q.open > 0 {
						continue nextQ
					}
				}
			}
		}
		seen[q.at][q.open] = q.sumflow

		moves := moves(q.open, q.at, valves, openValveIdx)
		for _, m := range moves {
			o := q.open
			if m.newOpen != "" {
				o = o | (1 << openValveIdx[m.newOpen])
			}
			Q = append(Q, qi{
				at:      m.at,
				open:    o,
				minute:  q.minute + 1,
				flow:    q.flow + m.addFlow,
				sumflow: q.sumflow + q.flow,
			})
		}
	}

	return largestFlow
}

func part2(valves map[string]valve, openValveIdx map[string]int) int {
	type qi struct {
		open    uint16
		ats     [2]string
		minute  int
		flow    int
		sumflow int
	}

	Q := []qi{{ats: [2]string{"AA", "AA"}, minute: 1}}
	var largestFlow int
	seen := make(map[[2]string]map[uint16]int)

nextQ:
	for {
		if len(Q) == 0 {
			break
		}
		q := Q[0]
		Q = Q[1:]

		if q.minute > 26 {
			largestFlow = max(largestFlow, q.sumflow)
			continue
		}

		if seens, ok := seen[q.ats]; !ok {
			seen[q.ats] = make(map[uint16]int)
		} else {
			for k, v := range seens {
				if v >= q.sumflow {
					if k == q.open || k&q.open > 0 {
						continue nextQ
					}
				}
			}
		}
		seen[q.ats][q.open] = q.sumflow

		var candos [2][]move
		for idx := 0; idx < 2; idx++ {
			candos[idx] = moves(q.open, q.ats[idx], valves, openValveIdx)
		}

		for _, you := range candos[0] {
			for _, ele := range candos[1] {
				if you.newOpen != "" && you.newOpen == ele.newOpen {
					continue
				}
				open := q.open
				if you.newOpen != "" {
					open |= 1 << openValveIdx[you.newOpen]
				}
				if ele.newOpen != "" {
					open |= 1 << openValveIdx[ele.newOpen]
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

	return largestFlow
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
