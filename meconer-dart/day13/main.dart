import '../util/util.dart';

//const String inputFile = 'day13/example.txt';
const String inputFile = 'day13/input.txt';

Future<void> main(List<String> args) async {
  var lines = await readInput(inputFile);
  print('Part 1:');
  print(calcResultPart1(lines));

  lines = await readInput(inputFile);
  print('Part 2:');
  print(calcResultPart2(lines));
}

int calcResultPart1(List<String> lines) {
  final pairs = buildPairs(lines);
  int sumOfPairIdx = 0;
  for (final pair in pairs) {
    if (pair.isInOrder()) sumOfPairIdx += pair.pairNo;
  }
  return sumOfPairIdx;
}

int calcResultPart2(List<String> lines) {
  List<String> packets = [];
  // Add divider packets
  String firstDividerPacket = '[[2]]';
  String secondDividerPacket = '[[6]]';
  packets.add(firstDividerPacket);
  packets.add(secondDividerPacket);
  for (final line in lines) {
    if (line.isNotEmpty) {
      packets.add(line);
    }
  }
  packets.sort((packetA, packetB) {
    final packetATokenProvider = TokenProvider(packetA);
    final packetAFirstToken = packetATokenProvider.getToken();
    assert(packetAFirstToken.tokenType == TokenType.listStart);
    final aList = buildList(packetATokenProvider) as ListItem;

    final packetBTokenProvider = TokenProvider(packetB);
    final packetBFirstToken = packetBTokenProvider.getToken();
    assert(packetBFirstToken.tokenType == TokenType.listStart);
    final bList = buildList(packetBTokenProvider) as ListItem;
    int result = aList.isInOrderWith(bList);
    return result;
  });
  int firstDividerPacketNo = 0;
  int secondDividerPacketNo = 0;
  for (int idx = 0; idx < packets.length; idx++) {
    if (packets[idx] == firstDividerPacket) {
      firstDividerPacketNo = idx + 1;
    }
    if (packets[idx] == secondDividerPacket) {
      secondDividerPacketNo = idx + 1;
    }
  }
  return firstDividerPacketNo * secondDividerPacketNo;
}

class TokenProvider {
  String tokenStr;
  TokenProvider(this.tokenStr);

  String getFirstTokenChar({bool remove = true}) {
    String oneChar = tokenStr.substring(0, 1);
    if (remove) {
      tokenStr = tokenStr.substring(1);
    }
    return oneChar;
  }

  Token getToken() {
    String firstChar = getFirstTokenChar();
    if (firstChar == '[') return Token(firstChar, 1, TokenType.listStart);
    if (firstChar == ']') return Token(firstChar, 1, TokenType.listEnd);
    if (firstChar == ',') return Token(firstChar, 1, TokenType.comma);
    // Otherwise it is a number.
    int number = 0;
    int length = 0;
    while (firstChar.isDigit()) {
      number = number * 10 + int.parse(firstChar);
      length++;
      firstChar = getFirstTokenChar(remove: false);
      if (firstChar.isDigit()) getFirstTokenChar();
    }
    final token = Token('token', length, TokenType.number);
    token.number = number;
    return token;
  }
}

class Item {}

class ValueItem extends Item {
  int value;
  ValueItem(this.value);
}

class ListItem extends Item {
  List<Item> list = [];

  int isInOrderWith(ListItem? otherList) {
    if (otherList == null) {
      // Otherlist ran out of items so it is smaller. Return out of order;
      return 1;
    }

    for (int idx = 0; idx < list.length; idx++) {
      var item = list[idx];

      if (idx >= otherList.list.length) {
        // right list ran out of items so it is smaller and therefore out of order
        return 1;
      }
      var other = otherList.list[idx];
      if (item is ValueItem && other is ValueItem) {
        if (item.value < other.value) return -1;
        if (item.value > other.value) return 1;
      }

      if (item is ValueItem && other is ListItem) {
        ListItem listItem = ListItem();
        listItem.list.add(ValueItem(item.value));
        int result = listItem.isInOrderWith(other);
        if (result != 0) return result;
      }

      if (item is ListItem && other is ValueItem) {
        ListItem listItem = ListItem();
        listItem.list.add(ValueItem(other.value));
        int result = item.isInOrderWith(listItem);
        if (result != 0) return result;
      }

      if (item is ListItem && other is ListItem) {
        int result = item.isInOrderWith(other);
        if (result != 0) return result;
      }
    }
    // Equal so far. But if the other list is longer it is larger so it is in order
    if (otherList.list.length > list.length) return -1;
    return 0;
  }
}

class Pair {
  int pairNo;
  String leftStr;
  String rightStr;
  Pair(this.leftStr, this.rightStr, this.pairNo);

  bool isInOrder() {
    final leftTokenProvider = TokenProvider(leftStr);
    final firstToken = leftTokenProvider.getToken();
    assert(firstToken.tokenType == TokenType.listStart);
    final leftList = buildList(leftTokenProvider) as ListItem;

    final rightTokenProvider = TokenProvider(rightStr);
    final firstRightToken = rightTokenProvider.getToken();
    assert(firstRightToken.tokenType == TokenType.listStart);
    final rightList = buildList(rightTokenProvider) as ListItem;

    bool isInOrder = leftList.isInOrderWith(rightList) <= 0;
    return isInOrder;
  }
}

List<Pair> buildPairs(List<String> lines) {
  List<Pair> pairList = [];
  int pairNo = 1;
  while (lines.isNotEmpty) {
    String left = lines.removeAt(0);
    String right = lines.removeAt(0);
    if (lines.isNotEmpty) lines.removeAt(0); // Remove empty line between pairs
    Pair pair = Pair(left, right, pairNo);
    pairNo++;
    pairList.add(pair);
  }
  return pairList;
}

enum TokenType { listStart, number, listEnd, comma }

class Token {
  String token;
  int? number;
  TokenType tokenType;
  int length;
  Token(this.token, this.length, this.tokenType);
}

Item? buildList(TokenProvider tokenProvider) {
  ListItem listItem = ListItem();

  var token = tokenProvider.getToken();

  while (token.tokenType != TokenType.listEnd) {
    if (token.tokenType == TokenType.number) {
      listItem.list.add(ValueItem(token.number!));
    }
    if (token.tokenType == TokenType.listStart) {
      final subItem = buildList(tokenProvider);
      if (subItem == null) return null;
      listItem.list.add(subItem);
    }
    if (token.tokenType == TokenType.comma) {
      // Comma. Do nothing
    }
    token = tokenProvider.getToken();
  }
  return listItem;
}

String removeToken(String line, Token token) => line.substring(token.length);

extension kind on String {
  bool isDigit() {
    try {
      int _ = int.parse(this);
      return true;
    } catch (e) {
      return false;
    }
  }
}

Token getToken(String line) {
  String firstChar = line.substring(0, 1);
  if (firstChar == '[') return Token(firstChar, 1, TokenType.listStart);
  if (firstChar == ']') return Token(firstChar, 1, TokenType.listEnd);
  if (firstChar == ',') return Token(firstChar, 1, TokenType.comma);
  // Otherwise it is a number.
  int number = 0;
  int length = 0;
  while (firstChar.isDigit()) {
    number = number * 10 + int.parse(firstChar);
    length++;
    line = line.substring(1);
    firstChar = line.substring(0, 1);
  }
  final token = Token('token', length, TokenType.number);
  token.number = number;
  return token;
}
