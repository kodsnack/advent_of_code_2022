import 'dart:io';

//const String inputFile = 'day3/example.txt';
const String inputFile = 'day3/input.txt';

Future<void> main(List<String> args) async {
  final lines = await readInput();
  print('Part 1:');
  print(calculatePrioritySum(lines));
  print('Part 1:');
  print(calculateBadgeSum(lines));
}

int calculateBadgeSum(List<String> lines) {
  int sum = 0;
  int groupCount = 0;
  const int groupSize = 3;
  while (groupCount < lines.length ~/ groupSize) {
    int groupStart = groupCount * groupSize;
    final groupList = lines.sublist(groupStart, groupStart + groupSize);
    final badge = findBadge(groupList);
    sum += getPriorityPoint(badge);
    groupCount++;
  }
  return sum;
}

String findBadge(List<String> groupList) {
  var commonCharSet1 = findCommonChars(groupList[0], groupList[1]);
  var commonCharSet2 = findCommonChars(groupList[1], groupList[2]);
  var commonCharSet = commonCharSet1.intersection(commonCharSet2);
  return commonCharSet.first;
}

int calculatePrioritySum(List<String> lines) {
  int sum = 0;
  for (final line in lines) {
    int linePriority = getLinePriority(line);
    sum += linePriority;
  }
  return sum;
}

int getLinePriority(String line) {
  final firstHalf = line.substring(0, line.length ~/ 2);
  final secondHalf = line.substring(line.length ~/ 2);
  if (firstHalf.length != secondHalf.length)
    throw Exception('Inte jämn stringlängd');

  final commonCharSet = findCommonChars(firstHalf, secondHalf);

  int priority = 0;
  commonCharSet.forEach((char) {
    priority += getPriorityPoint(char);
  });
  return priority;
}

Set<String> findCommonChars(String s1, String s2) {
  var commonCharSet = <String>{};
  for (var charToTest in s1.split('')) {
    if (s2.contains(charToTest)) {
      commonCharSet.add(charToTest);
    }
  }
  return commonCharSet;
}

int getPriorityPoint(String char) {
  const String pointOrder =
      'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  return pointOrder.indexOf(char) + 1;
}

Future<List<String>> readInput() {
  final file = File(inputFile);
  return file.readAsLines();
}
