package main

import (
	_ "embed"
	"fmt"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

func main() {
	fmt.Println(play(false))
	fmt.Println(play(true))
}

func play(part2 bool) int {
	input = strings.TrimSpace(input)

	var nums []int
	var origNums []int

	set := make(map[int]bool)

	mapped := make(map[int]int)

	for idx, row := range strings.Split(input, "\n") {
		n, _ := strconv.Atoi(row)

		if part2 {
			n = n * 811589153
		}

		n2 := n*1000 + idx
		if set[n2] {
			panic("dupe")
		}
		set[n2] = true
		mapped[n2] = n

		nums = append(nums, n2)
		origNums = append(origNums, n2)
	}

	times := 1
	if part2 {
		times = 10
	}

	for t := 0; t < times; t++ {
		for _, v := range origNums {
			// rotate until v is at the front
			for i := 0; i < len(nums); i++ {
				nums = append(nums, nums[0])
				nums = nums[1:]

				if nums[0] == v {
					break
				}
			}

			// remove v
			nums = nums[1:]

			// rotate v steps
			steps := mod(mapped[v], len(nums))
			for i := 0; i < steps; i++ {
				nums = append(nums, nums[0])
				nums = nums[1:]
			}

			// add v
			nums = append(nums, v)
		}
	}

	zero := 0
	for k, v := range nums {
		if mapped[v] == 0 {
			zero = k
			break
		}
	}

	a := nums[(zero+1000)%len(nums)]
	b := nums[(zero+2000)%len(nums)]
	c := nums[(zero+3000)%len(nums)]

	a = mapped[a]
	b = mapped[b]
	c = mapped[c]

	return a + b + c
}

func mod(a, b int) int {
	return (a%b + b) % b
}
