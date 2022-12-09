package main

import (
	_ "embed"
	"fmt"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

var DX = map[string]int{"U": -1, "D": 1}
var DY = map[string]int{"L": -1, "R": 1}

func main() {
	input = strings.TrimSpace(input)

	var headPos, tailPos xy
	visited := make(map[xy]bool)

	rope := [10]xy{}
	visited2 := make(map[xy]bool)

	for _, row := range strings.Split(input, "\n") {
		parts := strings.Split(row, " ")
		steps, _ := strconv.Atoi(parts[1])
		dx := DX[parts[0]]
		dy := DY[parts[0]]

		visited[tailPos] = true
		for i := 0; i < steps; i++ {
			headPos = xy{headPos[0] + dx, headPos[1] + dy}
			tailPos = keepUp(headPos, tailPos)
			visited[tailPos] = true
		}

		visited2[rope[9]] = true
		for i := 0; i < steps; i++ {
			rope[0] = xy{rope[0][0] + dx, rope[0][1] + dy}
			for h := 0; h < 9; h++ {
				rope[h+1] = keepUp(rope[h], rope[h+1])
			}
			visited2[rope[9]] = true
		}
	}

	fmt.Println(len(visited))
	fmt.Println(len(visited2))
}

var move = map[[2]int][2]int{
	{0, 2}:  {0, 1},
	{0, -2}: {0, -1},
	{2, 0}:  {1, 0},
	{-2, 0}: {-1, 0},
}

func keepUp(headPos, tailPos xy) xy {
	dx := headPos[0] - tailPos[0]
	dy := headPos[1] - tailPos[1]

	if abs(dx) <= 1 && abs(dy) <= 1 {
		return tailPos
	}

	if f, ok := move[[2]int{dx, dy}]; ok {
		tailPos[0] += f[0]
		tailPos[1] += f[1]
		return tailPos
	}

	if dx != 0 && dy != 0 {
		if dx > 0 {
			tailPos[0]++
		} else {
			tailPos[0]--
		}
		if dy > 0 {
			tailPos[1]++
		} else {
			tailPos[1]--
		}
	}

	return tailPos
}

type xy [2]int

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}
