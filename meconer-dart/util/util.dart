import 'dart:io';

Future<List<String>> readInput(String fileName) {
  final file = File(fileName);
  return file.readAsLines();
}
