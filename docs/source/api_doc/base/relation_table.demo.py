import pandas as pd

from pyuutils.base import Relation, sym_relation, sub2super, super2sub

if __name__ == '__main__':
    vs = [Relation.DIFFERENT, Relation.SUPERSET, Relation.SUBSET, Relation.EQUAL]
    rows = []
    for f in [sym_relation, sub2super, super2sub]:
        row = [f.__name__]
        for v in vs:
            row.append(f(v).name)
        rows.append(row)

    df = pd.DataFrame(
        data=rows,
        columns=['Func', *[v.name for v in vs]],
    )
    print(df.to_markdown(headers='keys', tablefmt='rst', index=False))
