import 'dart:io';

//const String inputFile = 'day1/example.txt';
const String inputFile = 'day1/input.txt';

Future<void> main(List<String> args) async {
  final lines = await readInput();
  final elfCalorieList = makeElfList(lines);
  elfCalorieList.sort();
  print('Part 1:');
  print(elfCalorieList.last);
  print('\nPart 2:');
  print(sumOfLastThreeElfs(elfCalorieList));
}

int sumOfLastThreeElfs(List<int> elfCalorieList) {
  return elfCalorieList.reversed.take(3).fold(0, (a, b) => a + b);
}

List<int> makeElfList(List<String> lines) {
  List<int> calorieList = [];

  int calories = 0;
  for (final line in lines) {
    if (line.isEmpty) {
      calorieList.add(calories);
      calories = 0;
    } else {
      calories += int.parse(line);
    }
  }
  if (calories != 0) calorieList.add(calories);
  return calorieList;
}

Future<List<String>> readInput() {
  final file = File(inputFile);
  return file.readAsLines();
}
