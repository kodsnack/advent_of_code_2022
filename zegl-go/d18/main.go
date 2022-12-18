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

	lava := make(map[xyz]bool)

	for _, row := range strings.Split(input, "\n") {
		nums := intsInString(row)
		p := xyz{nums[0], nums[1], nums[2]}
		lava[p] = true
	}

	DX := []int{1, -1, 0, 0, 0, 0}
	DY := []int{0, 0, 1, -1, 0, 0}
	DZ := []int{0, 0, 0, 0, 1, -1}

	var maxx, maxy, maxz int
	for p := range lava {
		maxx = max(maxx, p[0])
		maxy = max(maxy, p[1])
		maxz = max(maxz, p[2])
	}

	maxest := max(maxx, maxy)
	maxest = max(maxest, maxz)

	var sum int
	for p := range lava {
		for d := 0; d < 6; d++ {
			pp := xyz{
				p[0] + DX[d],
				p[1] + DY[d],
				p[2] + DZ[d],
			}
			if _, ok := lava[pp]; !ok {
				sum++
			}
		}
	}

	fmt.Println(sum)

	visible := make(map[xyz]bool)
	visibleOutsides := make(map[xyz]bool)
	seen := make(map[xyz]bool)

	type qi struct {
		pos  xyz
		from xyz
	}

	Q := []qi{{pos: xyz{-1, -1, -1}}}
nextQ:
	for {
		if len(Q) == 0 {
			break
		}
		q := Q[0]
		Q = Q[1:]

		if lava[q.pos] {
			visible[q.pos] = true
			visibleOutsides[q.from] = true
			continue
		}

		for _, v := range q.pos {
			if v < -1 || v > maxest+1 {
				continue nextQ
			}
		}

		if _, ok := seen[q.pos]; ok {
			continue
		}
		seen[q.pos] = true

		for d := 0; d < 6; d++ {
			pp := xyz{
				q.pos[0] + DX[d],
				q.pos[1] + DY[d],
				q.pos[2] + DZ[d],
			}
			Q = append(Q, qi{pos: pp, from: q.pos})
		}
	}

	var sum2 int
	for p := range lava {
		for d := 0; d < 6; d++ {
			pp := xyz{
				p[0] + DX[d],
				p[1] + DY[d],
				p[2] + DZ[d],
			}
			if _, ok := visibleOutsides[pp]; ok {
				sum2++
			}
		}
	}

	fmt.Println(sum2)
}

type xyz [3]int

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
