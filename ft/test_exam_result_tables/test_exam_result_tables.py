import ft.exam_result_tables as module


def test_columns_to_keep_full():
    table = module.read_source_csv('full.csv')
    totals = [54, 55, 56, 57, 58, 59, 61, 66]
    cols = module.columns_to_keep(table, short_format=False)
    correct = list(range(8)) + list(range(28, 37)) + totals
    assert cols == correct

    cols = module.columns_to_keep(table, short_format=True)
    correct = [0] + totals
    assert cols == correct


def test_columns_to_keep_compressed():
    table = module.read_source_csv('compressed.csv')
    totals = [21, 22, 23, 24, 25, 26, 28, 33]
    cols = module.columns_to_keep(table, short_format=False)
    correct = list(range(11)) + list(range(15, 21)) + totals
    assert cols == correct

    cols = module.columns_to_keep(table, short_format=True)
    correct = [0] + totals
    assert cols == correct
