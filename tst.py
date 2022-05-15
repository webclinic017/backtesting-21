class SymbolsGroup():
  def __init__(self):
    self._groups = dict()
    self._groups["test"] = ['ORCL', 'AAPL', 'GATEU']
    self._groups["bidon"] = ['ORCL', 'AAPL', 'GATEU']

  def __str__(self) -> str:
      print(self._groups)
      


if __name__ == '__main__':
  s = SymbolsGroup()
  tst = dict()
  tst["Key1"] = ["item1","item2","item3"]

  print(tst)
  print(s._groups)
  print(s)
