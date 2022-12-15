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

	var rows [][]int
	for _, row := range strings.Split(input, "\n") {
		nums := intsInString(row)
		rows = append(rows, nums)
	}

	fmt.Println(part1(rows))
	fmt.Println(part2(rows))
}

func part2(rows [][]int) int {
	searchSpace := 4000000

searchYs:
	for y := 0; y <= searchSpace; y++ {
		var ranges [][2]int

		for _, nums := range rows {
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

				if mi < 0 && ma > searchSpace {
					continue searchYs
				}
				if ma < 0 || mi > searchSpace {
					continue
				}
				ranges = append(ranges, [2]int{mi, ma})
			}
		}

		x := 0
		for {
			for range ranges { // lol
				for _, r := range ranges {
					if r[0] <= x && r[1] >= x {
						x = r[1] + 1
					}
					continue
				}
			}
			if x > searchSpace {
				break
			}
			return x*4000000 + y
		}
	}
	return -1
}

func part1(rows [][]int) int {
	exes := make(map[int]bool)
	findY := 2000000
	for _, row := range strings.Split(input, "\n") {
		nums := intsInString(row)

		sensorX, sensorY := nums[0], nums[1]
		beaconX, beaconY := nums[2], nums[3]

		delta := abs(sensorX-beaconX) + abs(sensorY-beaconY)

		minY := sensorY - delta
		maxY := sensorY + delta

		if minY <= findY && findY <= maxY {
			dist := abs(sensorY - findY)
			widthOnY := delta - dist
			for i := sensorX - widthOnY; i <= sensorX+widthOnY; i++ {
				exes[i] = true
			}
		}
	}

	return len(exes) - 1
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
