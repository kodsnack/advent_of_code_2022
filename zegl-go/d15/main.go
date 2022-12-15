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

	var inputs [][]int
	for _, row := range strings.Split(input, "\n") {
		nums := intsInString(row)
		inputs = append(inputs, nums)
	}

	fmt.Println(part1(inputs))
	fmt.Println(part2(inputs))
}

const searchSpace = 4000000 // part 2

func rowRanges(inputs [][]int, y int, part2 bool) [][2]int {
	var ranges [][2]int

	for _, nums := range inputs {
		sensorX, sensorY := nums[0], nums[1]
		beaconX, beaconY := nums[2], nums[3]

		delta := abs(sensorX-beaconX) + abs(sensorY-beaconY)

		minY := sensorY - delta
		maxY := sensorY + delta

		if minY <= y && y <= maxY {
			dist := abs(sensorY - y)
			width := delta - dist
			mi := sensorX - width
			ma := sensorX + width

			if part2 {
				if mi < 0 && ma > searchSpace {
					return nil
				}
				if ma < 0 || mi > searchSpace {
					continue
				}
				mi = max(mi, 0)
				ma = min(ma, searchSpace)
			}

			ranges = append(ranges, [2]int{mi, ma})
		}
	}

	return mergeRanges(ranges)
}

func part1(inputs [][]int) int {
	ranges := mergeRanges(rowRanges(inputs, 2000000, false))
	return ranges[0][1] - ranges[0][0]
}

func part2(inputs [][]int) int {
	for y := 0; y <= searchSpace; y++ {
		ranges := rowRanges(inputs, y, true)
		if len(ranges) == 2 {
			x := ranges[0][1] + 1
			return x*4000000 + y
		}
	}
	return -1
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
