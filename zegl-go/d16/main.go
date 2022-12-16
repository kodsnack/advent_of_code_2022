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

func part1(valves map[string]valve, openValveIdx map[string]int) int {
	type qi struct {
		open    [16]bool
		at      string
		minute  int
		flow    int
		sumflow int
	}

	Q := []qi{{at: "AA", minute: 1}}

	var largestFlow int
	var allTrue uint16 = math.MaxUint16

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

		bm := bitmap(q.open)
		if seens, ok := seen[q.at]; !ok {
			seen[q.at] = make(map[uint16]int)
		} else {
			for k, v := range seens {
				if v >= q.sumflow {
					if k == bm || k&bm > 0 {
						continue nextQ
					}
				}
			}
		}
		seen[q.at][bm] = q.sumflow

		open := q.open[openValveIdx[q.at]]

		if bm == allTrue {
			// stay put
			Q = append(Q, qi{
				at:      q.at,
				open:    q.open,
				minute:  q.minute + 1,
				flow:    q.flow,
				sumflow: q.sumflow + q.flow,
			})
		} else {
			if !open && valves[q.at].flowRate > 0 {
				opens := q.open
				opens[openValveIdx[q.at]] = true
				Q = append(Q, qi{
					at:      q.at,
					open:    opens,
					minute:  q.minute + 1,
					flow:    q.flow + valves[q.at].flowRate,
					sumflow: q.sumflow + q.flow,
				})
			}

			// if at open valve, go to connected valves
			if open || valves[q.at].flowRate == 0 {
				for _, v := range valves[q.at].connected {
					opens := q.open
					Q = append(Q, qi{
						at:      v,
						open:    opens,
						minute:  q.minute + 1,
						flow:    q.flow,
						sumflow: q.sumflow + q.flow,
					})
				}
			}
		}
	}

	return largestFlow
}

func part2(valves map[string]valve, openValveIdx map[string]int) int {
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

	var allTrue uint16 = math.MaxUint16

	Q := []qi{{ats: [2]string{"AA", "AA"}, minute: 1}}

	var largestFlow int
	var maxminute = 0

	seen := make(map[[2]string]map[uint16]int)

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
			maxminute = q.minute
		}

		if q.minute > 26 {
			largestFlow = max(largestFlow, q.sumflow)
			continue
		}

		bm := bitmap(q.open)
		if seens, ok := seen[q.ats]; !ok {
			seen[q.ats] = make(map[uint16]int)
		} else {
			for k, v := range seens {
				if v >= q.sumflow {
					if k == bm || k&bm > 0 {
						continue nextQ
					}
				}
			}
		}
		seen[q.ats][bm] = q.sumflow

		type cando struct {
			at      string
			newOpen string
			addFlow int
		}

		var candos [2][]cando

		for idx := 0; idx < 2; idx++ {
			var moves []cando

			at := q.ats[idx]
			atOpen := q.open[openValveIdx[at]]

			// move only if we can gain something
			if bm == allTrue {
				// stay
				moves = append(moves, cando{at: at})
			} else {
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
				// both can not open same valve, skip combo
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

	return largestFlow
}

func bitmap(in [16]bool) uint16 {
	var res uint16
	for i := range in {
		if in[i] {
			res |= 1 << i
		}
	}
	return res
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
