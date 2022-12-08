package main

import (
	_ "embed"
	"fmt"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

type xy [2]int

func main() {
	input = strings.TrimSpace(input)

	world := make(map[xy]int)

	var maxx, maxy int
	for x, row := range strings.Split(input, "\n") {
		for y, ch := range row {
			num, _ := strconv.Atoi(string(ch))
			world[xy{x, y}] = num
			maxy = max(maxy, y)
		}
		maxx = max(maxx, x)
	}

	DX := []int{1, -1, 0, 0}
	DY := []int{0, 0, 1, -1}

	var visible int
	for x := 0; x <= maxx; x++ {
	ys:
		for y := 0; y <= maxy; y++ {
			if x == 0 || x == maxx || y == 0 || y == maxy {
				visible++
				continue
			}

			this := world[xy{x, y}]

			for k := 0; k < 4; k++ {
				for i := 1; i < maxx; i++ {
					dx, dy := DX[k], DY[k]
					p := xy{x + dx*i, y + dy*i}
					if world[p] >= this {
						break
					}
					if p[0] == 0 || p[0] == maxx || p[1] == 0 || p[1] == maxy {
						visible++
						continue ys
					}
				}
			}
		}
	}

	fmt.Println(visible)

	var highscore int
	for pos, this := range world {
		score := []int{}
		for k := 0; k < 4; k++ {
			for i := 1; i < maxx; i++ {
				dx, dy := DX[k], DY[k]
				p := xy{pos[0] + dx*i, pos[1] + dy*i}
				if p[0] == 0 || p[0] == maxx || p[1] == 0 || p[1] == maxy || world[p] >= this {
					score = append(score, i)
					break
				}
			}
		}
		highscore = max(highscore, mul(score...))
	}
	fmt.Println(highscore)
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
