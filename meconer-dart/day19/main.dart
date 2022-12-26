import 'dart:collection';
import 'dart:math';

import '../util/util.dart';

//const String inputFile = 'day19/example.txt';
const String inputFile = 'day19/input.txt';

Future<void> main(List<String> args) async {
  var inputLines = await readInput(inputFile);

  List<Blueprint> blueprints = [];
  for (final inputLine in inputLines) {
    Blueprint blueprint = Blueprint.from(inputLine);
    blueprints.add(blueprint);
  }

  print('Part 1:');
  int resultP1 = calcResultP1(blueprints, timeLeft: 24);
  print(resultP1);

  print('Part 2:');
  print(calcResultP2(blueprints.sublist(0, 3), timeLeft: 32));
}

int calcResultP1(List<Blueprint> bluePrints, {required int timeLeft}) {
  int totalResult = 0;
  for (int bluePrintId = 1; bluePrintId <= bluePrints.length; bluePrintId++) {
    final startNode = Node(0, 0, 0, 0, 1, 0, 0, 0);
    maxGeodeSoFar = 0;
    final blueprint = bluePrints[bluePrintId - 1];

    maxOreNeededEveryMinute =
        max(blueprint.oreCostForClayRobot, blueprint.oreCostForObsidianRobot);
    maxOreNeededEveryMinute =
        max(blueprint.oreCostForGeodeRobot, maxOreNeededEveryMinute);

    maxClayNeededEveryMinute = blueprint.clayCostForObsidianRobot;

    collectCalls = 0;
    int result =
        startNode.collect(bluePrints[bluePrintId - 1], timeLeft: timeLeft);
    print(
        'Blueprint $bluePrintId ger max $result geodes efter $collectCalls anrop');
    totalResult += result * bluePrintId;
  }
  return totalResult;
}

int calcResultP2(List<Blueprint> bluePrints, {required int timeLeft}) {
  int totalResult = 1;
  for (int bluePrintId = 1; bluePrintId <= bluePrints.length; bluePrintId++) {
    final startNode = Node(0, 0, 0, 0, 1, 0, 0, 0);
    maxGeodeSoFar = 0;
    final blueprint = bluePrints[bluePrintId - 1];

    maxOreNeededEveryMinute =
        max(blueprint.oreCostForClayRobot, blueprint.oreCostForObsidianRobot);
    maxOreNeededEveryMinute =
        max(blueprint.oreCostForGeodeRobot, maxOreNeededEveryMinute);

    maxClayNeededEveryMinute = blueprint.clayCostForObsidianRobot;

    collectCalls = 0;
    int result =
        startNode.collect(bluePrints[bluePrintId - 1], timeLeft: timeLeft);
    print(
        'Blueprint $bluePrintId ger max $result geodes efter $collectCalls anrop');
    totalResult *= result;
  }
  return totalResult;
}

int maxGeodeSoFar = 0;
Set<Node> visited = HashSet<Node>();
int collectCalls = 0;
int maxOreNeededEveryMinute = 0;
int maxClayNeededEveryMinute = 0;

class Node {
  int ore;
  int clay;
  int obsidian;
  int geode;

  int oreRobots;
  int clayRobots;
  int obsidianRobots;
  int geodeRobots;

  // @override
  // bool operator ==(Object other) {
  //   if (identical(this, other)) return true;
  //   return other is Node &&
  //       (ore == other.ore &&
  //           clay == other.clay &&
  //           obsidian == other.obsidian &&
  //           geode == other.geode &&
  //           oreRobots == other.oreRobots &&
  //           clayRobots == other.clayRobots &&
  //           obsidianRobots == other.obsidianRobots &&
  //           geodeRobots == other.geodeRobots);
  // }

  // int get hashCode =>
  //     ore +
  //     clay * 100 +
  //     obsidian * 10000 +
  //     geode * 1000000 +
  //     oreRobots * 100000000 +
  //     clayRobots * 1000000000 +
  //     obsidianRobots * 10000000000 +
  //     geodeRobots * 100000000000;

  Node(this.ore, this.clay, this.obsidian, this.geode, this.oreRobots,
      this.clayRobots, this.obsidianRobots, this.geodeRobots);

  // Returns no of geode
  int collect(Blueprint blueprint,
      {required int timeLeft, String history = ''}) {
    int maxGeodes = 0;
    collectCalls++;
    //if (collectCalls % 100000000 == 0) print('n = $collectCalls');
    if (geode > maxGeodeSoFar) {
      maxGeodeSoFar = geode;
      print(
          'Geoderobots ${geodeRobots} , geode : ${geode}, timeLeft $timeLeft, no of calls : $collectCalls, history $history');
      //print(' oreR : $oreRobots');
      //print('clayR : $clayRobots');
      //print('obsR : $obsidianRobots');
      //print('geoR : $geodeRobots');
    }
    while (timeLeft > 0) {
      int maxPossibleGeodeRobots =
          timeLeft + geodeRobots; // If we could make one every minute
      int maxPossibleGeode =
          geode + (geodeRobots + maxPossibleGeodeRobots) * timeLeft ~/ 2 + 1;
      if (maxPossibleGeode < maxGeodeSoFar) {
        return maxGeodes;
      }
      Node? newNode = makeGeodeNode(blueprint);
      if (newNode != null) {
        newNode.collectResources();
        newNode.geodeRobots++;
        int newGeodes = newNode.collect(blueprint,
            timeLeft: timeLeft - 1, history: history + 'GeoR ');
        maxGeodes = max(maxGeodes, newGeodes);

        return maxGeodes;
      } else {
        // Try to make an obsidian robot but only if we need one
        if (obsidianRobots <= blueprint.obsidianCostForGeodeRobot) {
          newNode = makeObsidianNode(blueprint);
          if (newNode != null) {
            newNode.collectResources();
            newNode.obsidianRobots++;
            int newGeodes = newNode.collect(blueprint,
                timeLeft: timeLeft - 1, history: history + 'ObsR ');
            maxGeodes = max(maxGeodes, newGeodes);
          }
        }
        if (clayRobots <= maxClayNeededEveryMinute) {
          // Try to make a clay robot
          newNode = makeClayNode(blueprint);
          if (newNode != null) {
            newNode.collectResources();
            newNode.clayRobots++;
            int newGeodes = newNode.collect(blueprint,
                timeLeft: timeLeft - 1, history: history + 'ClayR ');
            maxGeodes = max(maxGeodes, newGeodes);
          }
        }
        // Try to make an ore robot
        if (oreRobots <= maxOreNeededEveryMinute) {
          newNode = makeOreNode(blueprint);

          if (newNode != null) {
            newNode.collectResources();
            newNode.oreRobots++;
            int newGeodes = newNode.collect(blueprint,
                timeLeft: timeLeft - 1, history: history + 'OreR ');
            maxGeodes = max(maxGeodes, newGeodes);
          }
        }

        collectResources();
        history = history + 'wait ';
        timeLeft--;
      }
    }
    return max(maxGeodes, geode);
  }

  void collectResources() {
    ore += oreRobots;
    clay += clayRobots;
    obsidian += obsidianRobots;
    geode += geodeRobots;
  }

  Node? makeOreNode(Blueprint blueprint) {
    if (ore >= blueprint.oreCostForOreRobot) {
      Node newNode = Node.copy(this);
      newNode.ore = ore - blueprint.oreCostForOreRobot;
      return newNode;
    }
    return null;
  }

  Node? makeClayNode(Blueprint blueprint) {
    if (ore >= blueprint.oreCostForClayRobot) {
      Node newNode = Node.copy(this);
      newNode.ore = ore - blueprint.oreCostForClayRobot;
      return newNode;
    }
    return null;
  }

  Node? makeObsidianNode(Blueprint blueprint) {
    if (ore >= blueprint.oreCostForObsidianRobot &&
        clay >= blueprint.clayCostForObsidianRobot) {
      Node newNode = Node.copy(this);
      newNode.ore = ore - blueprint.oreCostForObsidianRobot;
      newNode.clay = clay - blueprint.clayCostForObsidianRobot;
      return newNode;
    }
    return null;
  }

  Node? makeGeodeNode(Blueprint blueprint) {
    if (ore >= blueprint.oreCostForGeodeRobot &&
        obsidian >= blueprint.obsidianCostForGeodeRobot) {
      Node newNode = Node.copy(this);
      newNode.ore = ore - blueprint.oreCostForGeodeRobot;
      newNode.obsidian = obsidian - blueprint.obsidianCostForGeodeRobot;
      return newNode;
    }
    return null;
  }

  static Node copy(Node node) {
    return Node(node.ore, node.clay, node.obsidian, node.geode, node.oreRobots,
        node.clayRobots, node.obsidianRobots, node.geodeRobots);
  }
}

class Blueprint {
  int oreCostForOreRobot;

  int oreCostForClayRobot;

  int oreCostForObsidianRobot;
  int clayCostForObsidianRobot;

  int oreCostForGeodeRobot;
  int obsidianCostForGeodeRobot;
  Blueprint(
      this.oreCostForOreRobot,
      this.oreCostForClayRobot,
      this.oreCostForObsidianRobot,
      this.clayCostForObsidianRobot,
      this.oreCostForGeodeRobot,
      this.obsidianCostForGeodeRobot);

  factory Blueprint.from(String inputLine) {
    final lineParts = inputLine.split(' ');
    Blueprint bp = Blueprint(
        int.parse(lineParts[6]),
        int.parse(lineParts[12]),
        int.parse(lineParts[18]),
        int.parse(lineParts[21]),
        int.parse(lineParts[27]),
        int.parse(lineParts[30]));
    return bp;
  }
}
