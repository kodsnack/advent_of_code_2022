import '../util/util.dart';

const String inputFile = 'day17/example.txt';
//const String inputFile = 'day17/input.txt';

Future<void> main(List<String> args) async {
  var inputLine = await readInput(inputFile);
  print('Part 1:');
  print(calcResultP1(inputLine[0]));
}

int calcResultP1(String jetStreams) {
  List<Shape> shapeList = buildShapeList();
  Grid grid = Grid();
  for (final jetStream in jetStreams.split('')) {
    print(jetStream);
  }
  return 0;
}

class Grid {
  List<String> gridLines = [];
  int shapeIndex = 0;

  int topLevel() {
    return gridLines.length;
  }
}

List<Shape> buildShapeList() {
  Shape s1 = Shape([
    ['@@@@']
  ]);
  Shape s2 = Shape([
    ['.@.'],
    ['@@@'],
    ['.@.'],
  ]);
  Shape s3 = Shape([
    ['..@'],
    ['..@'],
    ['@@@'],
  ]);
  Shape s4 = Shape([
    ['@'],
    ['@'],
    ['@'],
    ['@'],
  ]);
  Shape s5 = Shape([
    ['@@'],
    ['@@'],
  ]);
  return [s1, s2, s3, s4, s5];
}

class Shape {
  List<List<String>> shape;

  Shape(this.shape);
}
