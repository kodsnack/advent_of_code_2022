import 'dart:io';

//const String inputFile = 'day4/example.txt';
const String inputFile = 'day4/input.txt';

Future<void> main(List<String> args) async {
  final lines = await readInput();
  print('Part 1:');
  print(countFullyContainedPairs(lines));
  print('Part 2:');
  print(countOverlappingPairs(lines));
}

int countFullyContainedPairs(List<String> lines) {
  int count = 0;
  for (var line in lines) {
    final elf1Range = line.split(',')[0].split('-');
    final elf2Range = line.split(',')[1].split('-');

    final elf1Start = int.parse(elf1Range.first);
    final elf1End = int.parse(elf1Range.last);

    final elf2Start = int.parse(elf2Range.first);
    final elf2End = int.parse(elf2Range.last);

    if (isContained(elf1Start, elf1End, elf2Start, elf2End)) {
      count++;
    }
  }
  return count;
}

int countOverlappingPairs(List<String> lines) {
  int count = 0;
  for (var line in lines) {
    final elf1Range = line.split(',')[0].split('-');
    final elf2Range = line.split(',')[1].split('-');

    final elf1Start = int.parse(elf1Range.first);
    final elf1End = int.parse(elf1Range.last);

    final elf2Start = int.parse(elf2Range.first);
    final elf2End = int.parse(elf2Range.last);

    if (isOverlapping(elf1Start, elf1End, elf2Start, elf2End)) {
      count++;
    }
  }
  return count;
}

bool isOverlapping(int start1, int end1, int start2, int end2) {
  // If start or end is equal they must be overlapping
  if (start1 == start2) {
    // Equal
    return true;
  }
  if (end1 == end2) {
    return true;
  }
  if (start1 < start2) {
    if (end1 >= start2) {
      return true;
    }
  }
  if (start1 > start2) {
    if (end2 >= start1) {
      return true;
    }
  }
  return false;
}

bool isContained(int start1, int end1, int start2, int end2) {
  if (start1 <= start2 && end1 >= end2) {
    // First range fully contains the second
    return true;
  }
  if (start1 >= start2 && end1 <= end2) {
    // First range fully contains the second
    return true;
  }
  return false;
}

Future<List<String>> readInput() {
  final file = File(inputFile);
  return file.readAsLines();
}
