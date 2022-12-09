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
	input = strings.TrimSpace(input)
	path := []string{}
	sizes := make(map[string]int)
	knownDirs := make(map[string]bool)

	for _, row := range strings.Split(input, "\n") {
		parts := strings.Split(row, " ")
		if parts[0] == "$" {
			if strings.HasPrefix(parts[1], "cd") {
				if row == "cd /" {
					path = []string{}
				} else if parts[2] == ".." {
					path = path[:len(path)-1]
				} else {
					path = append(path, parts[2])
				}
				knownDirs[strings.Join(path, "/")] = true
			}
		} else {
			size, _ := strconv.Atoi(parts[0])
			sizes[strings.Join(path, "/")+"/"+parts[1]] = size
		}
	}

	// p1
	sum := 0

	// p2
	smallest := 9999999999
	totalUsed := 0
	for _, v := range sizes {
		totalUsed += v
	}
	free := 70000000 - totalUsed
	needed := 30000000 - free

	for dir := range knownDirs {
		size := 0
		for k, v := range sizes {
			if strings.HasPrefix(k, dir) {
				size += v
			}
		}
		if size < 100000 {
			sum += size
		}
		if size >= needed && size < smallest {
			smallest = size
		}
	}

	fmt.Println("p1", sum)
	fmt.Println("p2", smallest)
}
