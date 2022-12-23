import '../util/util.dart';

//const String inputFile = 'day7/example.txt';
const String inputFile = 'day7/input.txt';

Future<void> main(List<String> args) async {
  var lines = await readInput(inputFile);
  print('Part 1:');
  print(calcResult1(lines));

  lines = await readInput(inputFile);
  print('Part 2:');
  print(calcResult2(lines));
}

enum NodeType { dir, file }

class Node {
  final String name;
  NodeType nodeType;
  Node? parent;

  Node(this.name, this.nodeType, this.parent);
}

class FileNode extends Node {
  int size;
  FileNode(String name, Node parent, this.size)
      : super(name, NodeType.file, parent);
}

class DirNode extends Node {
  List<Node> nodeList = [];
  DirNode(String name, Node? parent) : super(name, NodeType.dir, parent);

  void addFiles(List<FileNode> fileList) {
    nodeList.addAll(fileList);
  }
}

class FileSystem {
  Node rootNode = DirNode('/', null);
  late DirNode currentNode;
  List<int> dirSizes = [];

  FileSystem() {
    currentNode = rootNode as DirNode;
  }

  void changeDir(String dirToChangeTo) {
    if (dirToChangeTo == '..') {
      if (currentNode.parent != null) {
        currentNode = currentNode.parent! as DirNode;
      }
    } else {
      final nodeToChangeTo = findNode(currentNode, dirToChangeTo);
      if (nodeToChangeTo != null) currentNode = nodeToChangeTo;
    }
  }

  DirNode? findNode(DirNode currentNode, String dirToChangeTo) {
    for (final node in currentNode.nodeList) {
      if (node.name == dirToChangeTo && node.nodeType == NodeType.dir) {
        return node as DirNode;
      }
    }
    // Did not find node.
    return null;
  }

  void printFs(Node node, int level) {
    String indent = List.filled(level, '   ').join();
    if (node.nodeType == NodeType.file) {
      String name = (node as FileNode).name;
      int size = node.size;
      print('$indent- $name (file, size=$size)');
    } else {
      // DirNode.
      String name = (node as DirNode).name;
      print('$indent- $name (dir)');
      for (Node subNode in node.nodeList) {
        printFs(subNode, level + 1);
      }
    }
  }

  int calcDirSizes(Node node) {
    if (node.nodeType == NodeType.file) {
      int size = (node as FileNode).size;
      return size;
    } else {
      // DirNode.
      int size = 0;
      for (Node subNode in (node as DirNode).nodeList) {
        size += calcDirSizes(subNode);
      }
      String name = node.name;
      print('$name - $size');
      dirSizes.add(size);
      return size;
    }
  }

  int addSizesBelow(int limit) {
    int total = 0;
    for (int size in dirSizes) {
      if (size < limit) total += size;
    }
    return total;
  }

  int findSmallestDirSizeToDelete(int sizeNeededToDelete) {
    int leastFoundSoFar = dirSizes.last; // Root dir. Biggest of them all
    for (var dirSize in dirSizes) {
      if (dirSize > sizeNeededToDelete) {
        if (dirSize < leastFoundSoFar) leastFoundSoFar = dirSize;
      }
    }
    return leastFoundSoFar;
  }
}

int calcResult1(List<String> lines) {
  final fileSystem = buildFileSystem(lines);
  fileSystem.printFs(fileSystem.rootNode, 0);
  fileSystem.calcDirSizes(fileSystem.rootNode);
  return fileSystem.addSizesBelow(100000);
}

int calcResult2(List<String> lines) {
  final fileSystem = buildFileSystem(lines);
  fileSystem.printFs(fileSystem.rootNode, 0);
  fileSystem.calcDirSizes(fileSystem.rootNode);

  int totalFileSystemSize = 70000000;
  int neededSize = 30000000;
  int availableSize = totalFileSystemSize - fileSystem.dirSizes.last;
  int sizeNeededToDelete = neededSize - availableSize;
  return fileSystem.findSmallestDirSizeToDelete(sizeNeededToDelete);
}

FileSystem buildFileSystem(List<String> lines) {
  final fileSystem = FileSystem();

  while (lines.isNotEmpty) {
    var line = lines.removeAt(0).split(' ');

    if (line[0] != '\$') {
      // Must be a $. Something is wrong
      throw (Exception('Should be a \$ sign here'));
    }
    // First char is $ so it must be a command
    // cd command
    if (line[1] == 'cd') {
      fileSystem.changeDir(line[2]);
    }

    // ls command
    if (line[1] == 'ls') {
      String lsLine = lines.first;
      bool lsFinished = false;
      while (!lsFinished) {
        final lsLineParts = lsLine.split(' ');

        if (lsLineParts[0] == '\$') {
          // Next line is a new command.
          lsFinished = true;
        } else if (lsLineParts[0] == 'dir') {
          // New directory
          fileSystem.currentNode.nodeList
              .add(DirNode(lsLineParts[1], fileSystem.currentNode));
        } else {
          // Must be a file
          fileSystem.currentNode.nodeList.add(FileNode(lsLineParts[1],
              fileSystem.currentNode, int.parse(lsLineParts[0])));
        }

        if (!lsFinished) {
          lines.removeAt(0);
          if (lines.isEmpty) {
            lsFinished = true;
          } else {
            lsLine = lines.first;
          }
        }
      }
    }
  }
  return fileSystem;
}

int resultOfPart2(List<String> lines) {
  return 0;
}
