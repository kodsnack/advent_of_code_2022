package main

import (
	_ "embed"
	"fmt"
	"regexp"
	"sort"
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

	valveIdx := make(map[string]int)
	idx := 0
	for k := range valves {
		valveIdx[k] = idx
		idx++
	}

	openValveIdx := make(map[string]int)
	idx = 0
	for k, v := range valves {
		if v.flowRate > 0 {
			openValveIdx[k] = idx
			idx++
		}
	}

	fmt.Println(valves)

	type qi struct {
		open [16]bool

		youAt string
		eleAt string

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

	Q := []qi{{youAt: "AA", eleAt: "AA", minute: 1}}

	var largestFlowrate int

	var largestFlow int

	seen := make(map[string]map[[16]bool]int) // [at][open]sumflow

	var maxminute = 0

nextQ:
	for {
		if len(Q) == 0 {
			break
		}
		q := Q[0]
		Q = Q[1:]

		//largestFlow = max(largestFlow, q.sumflow)

		if q.minute > maxminute {
			fmt.Println("minute", q.minute, len(Q))
			maxminute = q.minute
		}

		// fmt.Println(q)

		largestFlowrate = max(largestFlowrate, q.flow)

		if q.minute > 26 {
			largestFlow = max(largestFlow, q.sumflow)
			// fmt.Println("flow", largestFlow)
			// fmt.Println("rate", largestFlowrate)
			continue
		}

		at := q.youAt + "-" + q.eleAt
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

		// bits := asbit(q.open)
		// been here before, with same open valves
		// if seen[at][bits] >= q.sumflow {
		// 	continue
		// }
		// been here with more open valves

		seen[at][q.open] = q.sumflow

		// k := fmt.Sprintf("%s-%s-%v", q.youAt, q.eleAt, q.open) // + strconv.Itoa(q.minute)
		// if best, ok := seen[k]; ok {
		// 	if best >= q.sumflow {
		// 		continue
		// 	}
		// }
		// seen[k] = q.sumflow

		youOpen := q.open[openValveIdx[q.youAt]]
		eleOpen := q.open[openValveIdx[q.eleAt]]

		openCount := 0
		withFlowCount := 0
		for _, v := range q.open {
			if v {
				openCount++
			}
		}
		for _, v := range valves {
			if v.flowRate > 0 {
				withFlowCount++
			}
		}
		allOpen := openCount == withFlowCount

		type cando struct {
			at      string
			newOpen string
			addFlow int
		}

		var youCanDo []cando
		var eleCanDo []cando

		if !allOpen {
			if !youOpen && valves[q.youAt].flowRate > 0 {
				youCanDo = append(youCanDo, cando{
					at:      q.youAt,
					newOpen: q.youAt,
					addFlow: valves[q.youAt].flowRate,
				})
			}

			// if at open valve, go to connected valves
			if youOpen || valves[q.youAt].flowRate == 0 {
				for _, v := range valves[q.youAt].connected {
					youCanDo = append(youCanDo, cando{at: v})
				}
			}
		}

		// stay
		youCanDo = append(youCanDo, cando{at: q.youAt})

		////////

		if !allOpen {
			if !eleOpen && valves[q.eleAt].flowRate > 0 {
				eleCanDo = append(eleCanDo, cando{
					at:      q.eleAt,
					newOpen: q.eleAt,
					addFlow: valves[q.eleAt].flowRate,
				})
			}

			// if at open valve, go to connected valves
			if eleOpen || valves[q.eleAt].flowRate == 0 {
				for _, v := range valves[q.eleAt].connected {
					eleCanDo = append(eleCanDo, cando{at: v})
				}
			}
		}

		// stay
		eleCanDo = append(eleCanDo, cando{at: q.eleAt})

		// all combos
		for _, you := range youCanDo {
			for _, ele := range eleCanDo {
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

				Q = append(Q, qi{
					youAt:   you.at,
					eleAt:   ele.at,
					minute:  q.minute + 1,
					flow:    q.flow + you.addFlow + ele.addFlow,
					sumflow: q.sumflow + q.flow,
					open:    open,
				})
			}
		}
	}

	fmt.Println(largestFlow)

	//fmt.Println(max)
}

func asbit(in [16]bool) uint32 {
	var out uint32
	for i, v := range in {
		if v {
			out |= 1 << uint(i)
		}
	}
	return out
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

func copyStringSlice(in []string) []string {
	out := make([]string, len(in))
	copy(out, in)
	return out
}

func contains(in []string, v string) bool {
	for _, vv := range in {
		if vv == v {
			return true
		}
	}
	return false
}

func key(in map[string]bool) string {
	var keys []string
	for k := range in {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	return strings.Join(keys, ",")
}

func copyopen(in map[string]bool) map[string]bool {
	out := make(map[string]bool)
	for k, v := range in {
		out[k] = v
	}
	return out
}

type xy [2]int

func neighbour4(p xy) []xy {
	DX := []int{1, -1, 0, 0}
	DY := []int{0, 0, 1, -1}
	res := make([]xy, 4)
	for k, dx := range DX {
		res[k] = xy{p[0] + dx, p[1] + DY[k]}
	}
	return res
}

func neighbour8(p xy) []xy {
	res := make([]xy, 0, 8)
	for dx := -1; dx <= 1; dx++ {
		for dy := -1; dy <= 1; dy++ {
			if dx == 0 && dy == 0 {
				continue
			}
			res = append(res, xy{p[0] + dx, p[1] + dy})
		}
	}
	return res
}

func csvInts(s string) []int {
	var res []int
	s = strings.ReplaceAll(s, " ", "")
	for _, ss := range strings.Split(s, ",") {
		num, _ := strconv.Atoi(ss)
		res = append(res, num)
	}
	return res
}

func mul(i ...int) int {
	m := 1
	for _, v := range i {
		m *= v
	}
	return m
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func render(visited map[xy]bool) {
	var minX, minY, maxX, maxY int
	for k := range visited {
		maxX = max(maxX, k[0])
		maxY = max(maxY, k[1])
		minX = min(minX, k[0])
		minY = min(minY, k[1])
	}

	for x := minX; x <= maxX; x++ {
		for y := minY; y <= maxY; y++ {

			if visited[xy{x, y}] {
				fmt.Print("#")
			} else {
				fmt.Print(" ")
			}
		}
		fmt.Println()
	}
}

func lowestCommonDenominator(n []int64) int64 {
	res := n[0]
	for _, v := range n[1:] {
		res = lcm(res, v)
	}
	return res
}

func lcm(a, b int64) int64 {
	return a * b / gcd(a, b)
}

func gcd(a, b int64) int64 {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func sortIntsAsc(n []int64) {
	sort.Slice(n, func(i, j int) bool {
		return n[i] < n[j]
	})
}

func sortIntsDesc(n []int64) {
	sort.Slice(n, func(i, j int) bool {
		return n[i] > n[j]
	})
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
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

func mergeRanges(ranges [][2]int) [][2]int {
	run := func(ranges [][2]int) [][2]int {
		var res [][2]int

	inserts:
		for _, r := range ranges {
			if len(res) == 0 {
				res = append(res, r)
				continue
			}

			// if fits inside any range, skip
			for _, rr := range res {
				if r[0] >= rr[0] && r[1] <= rr[1] {
					continue inserts
				}
			}

			// if overtakes any range, replace
			for i, rr := range res {
				if r[0] <= rr[0] && r[1] >= rr[1] {
					res[i] = r
					continue inserts
				}
			}

			// if overlaps with any range, merge
			for i, rr := range res {
				if r[0] <= rr[1] && r[0] >= rr[0] {
					res[i] = [2]int{min(r[0], rr[0]), max(r[1], rr[1])}
					continue inserts
				}

				if r[1] <= rr[1] && r[1] >= rr[0] {
					res[i] = [2]int{min(r[0], rr[0]), max(r[1], rr[1])}
					continue inserts
				}
			}

			// otherwise, append
			res = append(res, r)
		}

		return res
	}

	// run until no changes
	for {
		old := len(ranges)
		ranges = run(ranges)
		if len(ranges) == old {
			return ranges
		}
	}
}
