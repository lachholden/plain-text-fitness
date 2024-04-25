import datetime

from lark import Discard, Token, Transformer, v_args

import ptf.data


class PtfTransformer(Transformer):
    def scalar_str(self, toks):
        return str(toks[0][1:-1])

    def scalar_date(self, toks):
        return datetime.date.fromisoformat(toks[0])

    def tag_list(self, toks):
        return {t[1:] for t in toks if t.type != "WS"}

    def activity_type(self, toks):
        return str(toks[0])

    def data_key(self, toks):
        return str(toks[0])

    @v_args(inline=True)
    def data_pair(self, k, _, v):
        return (k, v)

    def data_pairs(self, toks):
        return dict([t for t in toks if isinstance(t, tuple)])

    @v_args(inline=True)
    def statement_activity(
        self,
        activity_date,
        _1,
        activity_type,
        _2,
        tag_list,
        _3,
        data_pairs,
    ):
        activity = ptf.data.Activity(
            date=activity_date,
            activity_type=activity_type,
        )
        if tag_list is not None:
            activity.tags = tag_list
        if data_pairs is not None:
            activity.data = data_pairs
        return activity

    def start(self, toks):
        return [t for t in toks if not (hasattr(t, "type") and t.type == "WS")]
